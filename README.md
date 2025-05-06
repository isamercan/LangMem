# 🧠 LangMem API — AI Memory for Hotel Reviews (Multi-User + GPT)

LangMem API is a minimal and extensible AI memory system that supports structured hotel reviews, semantic search, GPT-4o summarization, and polite auto-replies — per user. No database required.

---

## 🚀 Features

- 🔹 Multi-user memory (`user_id`)
- 🏨 Structured hotel review format
- 🔍 Semantic search via FAISS + OpenAI Embeddings
- 🧠 GPT-4o powered summaries (short & detailed)
- 💬 GPT-based auto-replies per review
- 📅 Memory stored as `.pkl` files (per user)

---

## 💪 Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-your-openai-key
```

> ✅ Make sure `.env` is added to `.gitignore`

---

## ▶️ Run the API

```bash
uvicorn app.main:app --reload
```

Visit the Swagger docs at:

📍 http://127.0.0.1:8000/docs

---

## 🥪 Example Usage (via Swagger)

### ➕ `POST /memories/add`

Adds a structured hotel review to a specific user’s memory:

```json
{
  "user_id": "isa",
  "metadata": {
    "hotel_id": "HTL007",
    "hotel_name": "Ocean Breeze",
    "location": "İzmir",
    "hotel_url": "https://example.com/oceanbreeze"
  },
  "comment": "The pool was dirty but the staff were great.",
  "tags": ["pool", "staff"],
  "auto_reply": true
}
```

Response:

```json
{
  "status": "added",
  "reply": "Thank you for your feedback. We're sorry about the pool and will improve it promptly."
}
```

---

### 🔍 `GET /memories/search`

```http
/memories/search?user_id=isa&q=pool&hotel_url=https://example.com/oceanbreeze
```

Returns relevant reviews matching the search.

---

### 🧠 `POST /summarize`

Summarizes the reviews for a hotel using GPT-4o.

```json
{
  "user_id": "isa",
  "question": "What do people say?",
  "hotel_url": "https://example.com/oceanbreeze",
  "style": "short"
}
```

Response:

```json
{
  "hotel": "Ocean Breeze",
  "style": "short",
  "answer": "Guests loved the staff but complained about pool cleanliness."
}
```

> `style` can be `"short"` or `"detailed"`

---

### 🥵 `POST /reset`

```http
/reset?user_id=isa
```

Clears memory for a given user.

---

## 📂 Memory Storage

All memory is stored under:

```
memory_data/memory_<user_id>.pkl
```

Each user gets their own file.

---

## 📄 Sample Data

To load 20 hotel reviews for testing:

```bash
python scripts/load_sample_reviews.py
```

Make sure `sample_hotel_reviews.json` exists in root.

---

## 💫 Ideas to Expand

- [ ] Add `user language` or `tone` to customize replies
- [ ] Push notifications when new auto-reply is generated
- [ ] Add frontend/iOS app integration
- [ ] Extend to restaurant reviews or other domains

---

## 👨‍💻 Author

Built by [isa mercan](https://github.com/isamercan)