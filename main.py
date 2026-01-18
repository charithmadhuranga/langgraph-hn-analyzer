import requests
from bs4 import BeautifulSoup
from typing import List, Dict, TypedDict
from langchain_google_genai import GoogleGenerativeAI
from langgraph.graph import StateGraph, END

from dotenv import load_dotenv

load_dotenv(verbose=True)

class HNState(TypedDict):
    topic: str
    raw_articles: List[Dict]
    filtered_articles: List[Dict]
    analysis: str
    summary: str

def scrape_hackernews(state: HNState) -> HNState:
    url = "https://news.ycombinator.com/"
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []

    for item in soup.select(".athing"):
        title = item.select_one(".titleline a")
        if not title:
            continue

        articles.append({
            "title": title.text.strip(),
            "link": title["href"]
        })

    state["raw_articles"] = articles
    return state

def filter_articles(state: HNState) -> HNState:
    topic = state["topic"].lower()

    filtered = [
        article for article in state["raw_articles"]
        if topic in article["title"].lower()
    ]

    state["filtered_articles"] = filtered
    return state



llm = GoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0.3)

def analyze_articles(state: HNState) -> HNState:
    if not state["filtered_articles"]:
        state["analysis"] = "No relevant articles found."
        return state

    titles = "\n".join(
        f"- {a['title']}" for a in state["filtered_articles"]
    )

    prompt = f"""
Analyze the following Hacker News article titles about "{state['topic']}".

Tasks:
- Identify key trends
- Assess technical relevance
- Note overall sentiment

Articles:
{titles}
"""

    response = llm.invoke(prompt)

    state["analysis"] = (
        response.content if hasattr(response, "content") else response
    )
    return state



def summarize_analysis(state: HNState) -> HNState:
    response = llm.invoke(
        f"Summarize the following analysis in 5–6 lines:\n\n{state['analysis']}"
    )

    state["summary"] = (
        response.content if hasattr(response, "content") else response
    )
    return state





graph = StateGraph(HNState)

graph.add_node("scrape", scrape_hackernews)
graph.add_node("filter", filter_articles)
graph.add_node("analyze", analyze_articles)
graph.add_node("summarize", summarize_analysis)

graph.set_entry_point("scrape")

graph.add_edge("scrape", "filter")
graph.add_edge("filter", "analyze")
graph.add_edge("analyze", "summarize")
graph.add_edge("summarize", END)

hn_graph = graph.compile()


if '__main__' == __name__:
    result = hn_graph.invoke({
        "topic": "AI",
        "raw_articles": [],
        "filtered_articles": [],
        "analysis": "",
        "summary": ""
    })

    print("🔍 Analysis:\n", result["analysis"])
    print("\n📰 Summary:\n", result["summary"])

