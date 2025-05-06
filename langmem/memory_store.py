# langmem/memory_store.py

import faiss
import numpy as np
from datetime import datetime
from .embedder import get_embedding
import pickle

class LangMemStore:
    def __init__(self, dim=1536):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.memories = []

    def add(self, text: str, tags: list[str] = None, metadata: dict = None):
        embedding = np.array([get_embedding(text)], dtype='float32')
        self.index.add(embedding)
        memory = {
            "text": text,
            "timestamp": datetime.now().isoformat(),
            "tags": tags or [],
            "metadata": metadata or {}
        }
        self.memories.append(memory)

    def search(self, query: str, k: int = 5):
        embedding = np.array([get_embedding(query)], dtype='float32')
        distances, indices = self.index.search(embedding, k)
        return [(self.memories[i], float(distances[0][j])) for j, i in enumerate(indices[0])]

    def save_to_file(self, path="memory.pkl"):
        embeddings = [get_embedding(m["text"]) for m in self.memories]
        with open(path, "wb") as f:
            pickle.dump((self.memories, embeddings), f)

    def load_from_file(self, path="memory.pkl"):
        with open(path, "rb") as f:
            self.memories, embeddings = pickle.load(f)
            self.index.add(np.array(embeddings, dtype='float32'))
