import os
import requests
from flask import Flask, render_template, request, session, redirect, url_for, jsonify

app = Flask(__name__)
app.secret_key = "super_secret_key_for_demo_only"  # Insecure for demo purposes

# Configuration
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama2:7b")
USERS_FILE = "users.txt"
RULES_FILE = "rules.txt"

def get_users():
    """Reads users from the text file."""
    users = {}
    if not os.path.exists(USERS_FILE):
        return users
    with open(USERS_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(":")
            if len(parts) == 3:
                users[parts[0]] = {"password": parts[1], "role": parts[2]}
    return users

def get_system_prompt():
    """Reads the rules from the text file."""
    if not os.path.exists(RULES_FILE):
        return "You are a helpful assistant."
    with open(RULES_FILE, "r", encoding="utf-8") as f:
        return f.read()

def call_ollama(full_prompt):
    url = f"{OLLAMA_HOST}/api/generate"
    payload = {
        "model": OLLAMA_MODEL, 
        "prompt": full_prompt, 
        "stream": False
    }
    try:
        r = requests.post(url, json=payload, timeout=120)
        r.raise_for_status()
        return r.json().get("response", "").strip()
    except Exception as e:
        return f"Error communicating with LLM: {str(e)}"

# Routes
@app.route("/")
def index():
    if "user" in session:
        role = session.get("role")
        if role == "developer":
            return redirect(url_for("developer_portal"))
        elif role == "admin":
            return redirect(url_for("admin_dashboard"))
    return render_template("portal_visitor.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        users = get_users()
        
        if username in users and users[username]["password"] == password:
            session["user"] = username
            session["role"] = users[username]["role"]
            
            if session["role"] == "developer":
                return redirect(url_for("developer_portal"))
            elif session["role"] == "admin":
                return redirect(url_for("admin_dashboard"))
            else:
                return redirect(url_for("index")) # Generic loop?
        else:
            error = "Invalid username or password"
            
    return render_template("portal_login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/portal/developer")
def developer_portal():
    if session.get("role") != "developer":
        return redirect(url_for("login"))
    return render_template("portal_developer.html")

@app.route("/portal/admin")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect(url_for("login"))
    return render_template("portal_admin.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    role = session.get("role", "visitor")
    user = session.get("user", "Guest")
    
    system_rules = get_system_prompt()
    
    # Context injection
    context = f"Current User: {user}\nCurrent Role: {role}\nContext: The user is currently viewing the {role} interface."
    
    # Vulnerable formatting preserved for demonstration
    full_prompt = f"""{system_rules}

{context}

User: {user_input}
Assistant:"""

    response = call_ollama(full_prompt)
    
    return jsonify({"answer": response})

if __name__ == "__main__":
    print(f"Starting Portal App...")
    app.run(host="0.0.0.0", port=5000, debug=True)
