# langmem/tool.py
import os
from .memory_store import LangMemStore
from .llm_client import ask_llm

class LangMemTool:
    def __init__(self, user_id: str, base_folder="memory_data"):
        self.user_id = user_id
        self.memory_file = os.path.join(base_folder, f"memory_{user_id}.pkl")
        os.makedirs(base_folder, exist_ok=True)
        self.store = LangMemStore()
        self._load()


    def _load(self):
        try:
            self.store.load_from_file(self.memory_file)
            print("✅ Memory loaded.")
        except FileNotFoundError:
            print("🆕 No existing memory found. Starting fresh.")

    def save(self):
        self.store.save_to_file(self.memory_file)
        print("💾 Memory saved.")

    def add(self, text: str, tags: list[str] = None):
        self.store.add(text, tags)
        print(f"➕ Added: {text[:60]}...")

    def batch_add(self, texts: list[str], tags: list[str] = None):
        for text in texts:
            self.add(text, tags)
        self.save()

    def add_memory_object(self, memory: dict):
        self.store.add(
            text=memory["text"],
            tags=memory.get("tags", []),
            metadata=memory.get("metadata", {})
        )

    def summarize(self, question: str, k: int = 10, model: str = "gpt-4o", filter_by_url: str = None) -> str:
        results = self.store.search(question, k)
        if filter_by_url:
            results = [r for r in results if r[0].get("metadata", {}).get("hotel_url") == filter_by_url]
        context = "\n".join([f"- {m['text']}" for m, _ in results])
        prompt = f"""
        You are an AI assistant with access to structured hotel memory.
        
        Context: {context}
        
        Question: {question}
        
        Answer:"""
        return ask_llm(prompt, model=model)
    
    def generate_reply_to_comment(self, metadata: dict, comment: str, model: str = "gpt-4o") -> str:
        hotel_name = metadata.get("hotel_name", "the hotel")
        prompt = f"""
        You are the assistant manager of {hotel_name}. A guest left the following comment:

        "{comment}"
        Rules:
        
        -- Write a polite and concise reply on behalf of the hotel.
        -- Write a short Thanks reply.
        -- Ask a visitor to give a start from 0 to 5.

        """
        return ask_llm(prompt, model=model)

    def llm(self, prompt: str, model: str = "gpt-4o") -> str:
        return ask_llm(prompt, model=model)


