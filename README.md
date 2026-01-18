```markdown
# 📰 Hacker News Topic Analyzer (LangGraph)

A simple **LangGraph-powered AI pipeline** that scrapes **Hacker News**, filters articles by a given topic, analyzes trends using an LLM, and produces a concise news summary.

Built with **Python**, **LangGraph**, **BeautifulSoup**, and **Requests**.

---

## ✨ Features

- 🔎 Scrape latest Hacker News front page
- 🎯 Filter articles by user-defined topic (e.g., AI, Security, Open Source)
- 🧠 AI-powered analysis of trends and sentiment
- 📰 Clean, readable news summary
- 🧩 Modular LangGraph architecture (easy to extend)

---

## 🏗️ Architecture

```

User Topic
↓
Scraper Node (requests + bs4)
↓
Filter Node (keyword matching)
↓
Analysis Node (LLM)
↓
Summarizer Node (LLM)
↓
Final Summary

````

---

## 📦 Tech Stack

- **Python 3.10+**
- **LangGraph**
- **LangChain**
- **OpenAI-compatible LLM**
- **BeautifulSoup4**
- **Requests**

---

## 🚀 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/charithmadhuranga/langgraph-hn-analyzer.git
cd langgraph-hn-analyzer
````

### 2️⃣ Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### 3️⃣ Install dependencies

```bash
pip install langgraph langchain langchain-openai requests beautifulsoup4
```

---

## 🔐 Environment Variables

Set your LLM API key:

```bash
export OPENAI_API_KEY="your-api-key"
```

(Windows PowerShell)

```powershell
setx OPENAI_API_KEY "your-api-key"
```

---

## ▶️ Usage

Run the main script:

```bash
python main.py
```

Example input:

```python
result = hn_graph.invoke({
    "topic": "AI",
    "raw_articles": [],
    "filtered_articles": [],
    "analysis": "",
    "summary": ""
})
```

Example output:

```
🔍 Analysis:
Hacker News discussions around AI focus on open-source models,
agent frameworks, and real-world deployment challenges.

📰 Summary:
AI-related Hacker News posts highlight strong interest in
practical agent systems and cost-efficient inference.
```

---

## 🧠 LangGraph State Schema

```python
class HNState(TypedDict):
    topic: str
    raw_articles: List[Dict]
    filtered_articles: List[Dict]
    analysis: str
    summary: str
```

---

## 🛠️ Common Issues

### ❗ `AttributeError: 'str' object has no attribute 'content'`

LangChain may return a string instead of an AIMessage.

✅ Fix:

```python
state["analysis"] = (
    response.content if hasattr(response, "content") else response
)
```

---

## 🔜 Future Improvements

* 🔄 Multi-page scraping (HN pagination)
* 📊 Trend scoring and ranking
* 🧠 RAG with historical Hacker News data
* 🌐 FastAPI API endpoint
* 🧪 Auto-evaluation and confidence scoring
* 🤖 Multi-agent debate using LangGraph

---

## ⚠️ Disclaimer

This project scrapes publicly available data from Hacker News.
Use responsibly and respect the website’s terms of service.

---

## 📄 License

MIT License

---

## ⭐ Acknowledgements

* Hacker News
* LangGraph
* LangChain
* BeautifulSoup

---

Happy hacking 🚀

```
```
