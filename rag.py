import os
import glob
import numpy as np
from dataclasses import dataclass
from sentence_transformers import SentenceTransformer


@dataclass
class Chunk:
    text: str
    source: str
    access: str  # "public" or "internal"


def _read_text_file(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def _chunk_text(text: str, chunk_size: int = 900, overlap: int = 150):
    """
    Minimal deterministic chunker: overlapping character windows.
    Good enough for demo RAG.
    """
    text = (text or "").strip()
    if not text:
        return []

    chunks = []
    i = 0
    step = max(1, chunk_size - overlap)
    while i < len(text):
        chunk = text[i : i + chunk_size].strip()
        if chunk:
            chunks.append(chunk)
        i += step
    return chunks


class SimpleRAG:
    def __init__(self, docs_root: str = "docs", model_name: str = "all-MiniLM-L6-v2"):
        self.docs_root = docs_root
        self.embedder = SentenceTransformer(model_name)
        self.chunks: list[Chunk] = []
        self.embeddings: np.ndarray | None = None

    def build_index(self):
        self.chunks = []

        public_paths = glob.glob(os.path.join(self.docs_root, "public_docs", "**", "*.md"), recursive=True)
        public_paths += glob.glob(os.path.join(self.docs_root, "public_docs", "**", "*.txt"), recursive=True)

        internal_paths = glob.glob(os.path.join(self.docs_root, "internal_docs", "**", "*.md"), recursive=True)
        internal_paths += glob.glob(os.path.join(self.docs_root, "internal_docs", "**", "*.txt"), recursive=True)

        for path in public_paths:
            text = _read_text_file(path)
            for c in _chunk_text(text):
                self.chunks.append(
                    Chunk(text=c, source=os.path.relpath(path, self.docs_root), access="public")
                )

        for path in internal_paths:
            text = _read_text_file(path)
            for c in _chunk_text(text):
                self.chunks.append(
                    Chunk(text=c, source=os.path.relpath(path, self.docs_root), access="internal")
                )

        if not self.chunks:
            # Safe empty index
            self.embeddings = np.zeros((0, 384), dtype=np.float32)
            return

        texts = [ch.text for ch in self.chunks]
        emb = self.embedder.encode(texts, normalize_embeddings=True, show_progress_bar=False)
        self.embeddings = np.array(emb, dtype=np.float32)

    def retrieve(self, query: str, role: str, top_k: int = 4):
        """
        role: visitor | developer | admin
        visitor/developer -> public only
        admin -> public + internal
        """
        if self.embeddings is None:
            raise RuntimeError("Index not built. Call build_index() first.")

        role = (role or "visitor").strip().lower()
        allowed_internal = role in {"admin", "maintainer"}

        allowed_idxs: list[int] = []
        for i, ch in enumerate(self.chunks):
            if ch.access == "public":
                allowed_idxs.append(i)
            elif ch.access == "internal" and allowed_internal:
                allowed_idxs.append(i)

        if not allowed_idxs:
            return []

        q_emb = self.embedder.encode([query], normalize_embeddings=True, show_progress_bar=False)
        q_emb = np.array(q_emb, dtype=np.float32)[0]

        cand_emb = self.embeddings[allowed_idxs]
        scores = cand_emb @ q_emb  # cosine similarity because normalized

        top_k = min(top_k, len(allowed_idxs))
        top_pos = np.argsort(-scores)[:top_k]

        results = []
        for p in top_pos:
            idx = allowed_idxs[int(p)]
            results.append(
                {
                    "score": float(scores[int(p)]),
                    "source": self.chunks[idx].source,
                    "access": self.chunks[idx].access,
                    "text": self.chunks[idx].text,
                }
            )
        return results
