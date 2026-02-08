import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Configuration
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:3b")
RULES_FILE = "rules.txt"

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
        print(f"DEBUG: sending request to {url} with model {OLLAMA_MODEL}")
        r = requests.post(url, json=payload, timeout=120)
        r.raise_for_status()
        return r.json().get("response", "").strip()
    except Exception as e:
        print(f"ERROR: {e}")
        return f"Error communicating with LLM: {str(e)}"

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", role="demo_user")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    system_rules = get_system_prompt()
    
    # VULNERABILITY: Direct concatenation allows easy Prompt Injection
    # The user input comes *after* instructions, giving it high precedence in some models,
    # or allowing "Ignore previous instructions" attacks.
    full_prompt = f"""{system_rules}

User: {user_input}
Assistant:"""

    response = call_ollama(full_prompt)
    
    return jsonify({
        "answer": response,
        "sources": [{"source": "rules.txt", "access": "system", "score": 1.0}] 
    })

if __name__ == "__main__":
    print(f"Starting VULNERABLE demo app...")
    print(f"Rules loaded from: {os.path.abspath(RULES_FILE)}")
    app.run(host="0.0.0.0", port=5001, debug=True)
