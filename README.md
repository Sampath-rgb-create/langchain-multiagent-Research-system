# 🔬 AI Multi-Agent Research System

An autonomous, collaborative multi-agent research pipeline built with **LangChain**, **OpenRouter**, and **Streamlit**. 

This system deploys a team of four specialized AI agents that autonomously query the live web, extract in-depth content from primary sources, draft a cohesive, well-structured research report, and critically review the final output.

---

## 📑 Table of Contents
- [Architecture & How It Works](#-architecture--how-it-works)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [API Keys Setup](#api-keys-setup)
- [How to Use](#-how-to-use)
  - [1. Streamlit Web UI (Recommended)](#1-streamlit-web-ui-recommended)
  - [2. Command-Line Interface (CLI)](#2-command-line-interface-cli)
- [Visitor API Key Support (BYOK)](#-visitor-api-key-support-byok)
- [License](#-license)

---

## 🤖 Architecture & How It Works

The system operates as a sequential multi-agent pipeline where each agent specializes in a distinct stage of the research workflow:

```
[ User Input: Topic ]
          │
          ▼
┌──────────────────┐
│  1. Search Agent │ ──► Queries Tavily Search API for authoritative sources
└──────────────────┘
          │ (Search Snippets + URLs)
          ▼
┌──────────────────┐
│  2. Reader Agent │ ──► Selects the top source & extracts clean article text
└──────────────────┘
          │ (Deep Scraped Web Content)
          ▼
┌──────────────────┐
│  3. Writer Agent │ ──► Synthesizes research into a structured 3-part report
└──────────────────┘
          │ (Drafted Report)
          ▼
┌──────────────────┐
│  4. Critic Agent │ ──► Evaluates coherence, structure, citations & feedback
└──────────────────┘
          │
          ▼
[ Final Deliverables: Report + Critique + Scraped Evidence ]
```

### The 4 Specialized Agents:
1. **🔍 Search Agent (`build_search_agent`)**:
   - Equipped with the `web_search` tool (powered by Tavily API).
   - Formulates targeted search queries to retrieve the latest reliable sources, URLs, and summaries.
2. **🌐 Reader Agent (`build_scrape_agent`)**:
   - Equipped with the `scrape_url` tool.
   - Evaluates search results to pick the most informative URL and scrapes the full article text, removing HTML noise, scripts, and navigation clutter.
3. **✍️ Writer Agent (`writer_chain`)**:
   - Combines the raw search hits and deep scraped text.
   - Generates a detailed, plagiarism-free research article structured with an *Introduction*, *Main Body*, and *Conclusion*.
4. **🧐 Critic Agent (`critic_chain`)**:
   - Acts as an editorial reviewer, analyzing the drafted report for clarity, factual cohesion, and depth, while providing constructive recommendations.

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Agent Framework** | [LangChain](https://github.com/langchain-ai/langchain) (`langchain`, `langchain-core`) | Agent orchestration, tool integration, and prompt chaining |
| **LLM Provider** | [OpenRouter](https://openrouter.ai/) (`langchain-openrouter`) | Flexible access to state-of-the-art open models (e.g. `liquid/lfm-2.5-2.6b:free`) |
| **Local LLM Support** | [Ollama](https://ollama.com/) (`langchain-ollama`) | Optional local inference execution |
| **Web Search API** | [Tavily](https://tavily.com/) (`tavily-python`) | Real-time, AI-optimized web search results |
| **Web Scraping** | `BeautifulSoup4`, `readability-lxml`, `trafilatura`, `requests` | High-fidelity HTML parsing, article body extraction, and text cleaning |
| **Frontend UI** | [Streamlit](https://streamlit.io/) | Interactive web interface with real-time agent progress tracking |
| **Environment** | Conda + Python 3.11 + `python-dotenv` | Isolated dependencies and environment configuration |

---

## 📁 Project Structure

```text
langchain-multiagent-Research-system/
├── app.py                     # Streamlit frontend application
├── main.py                    # CLI entry point to run pipeline directly
├── requirements.txt           # Python dependencies
├── .env.example               # Template for API keys
├── .gitignore                 # Git ignore rules (.env, cache, etc.)
├── README.md                  # Project documentation
└── src/
    ├── __init__.py
    ├── agents/
    │   ├── __init__.py
    │   └── agent.py           # Search, Scrape, Writer, and Critic agent definitions
    ├── pipeline/
    │   ├── __init__.py
    │   └── pipeline.py        # Pipeline orchestrator with live status callbacks
    └── tools/
        ├── __init__.py
        └── tools.py           # Web search and URL scraping tools
```

---

## 🚀 Getting Started

### Prerequisites
- [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/)
- An **OpenRouter API Key** (Free tier available at [openrouter.ai/keys](https://openrouter.ai/keys))
- A **Tavily API Key** (Free tier available at [tavily.com](https://tavily.com))

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Sampath-rgb-create/langchain-multiagent-Research-system.git
   cd langchain-multiagent-Research-system
   ```

2. **Create and activate the Conda environment:**
   ```bash
   conda create -n langagent python=3.11 -y
   conda activate langagent
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### API Keys Setup

Create a `.env` file in the root directory (or rename `.env.example` if available):

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

*(Note: If using the Streamlit Web UI, you and your visitors can also paste API keys directly into the frontend without modifying `.env`).*

---

## 💻 How to Use

### 1. Streamlit Web UI (Recommended)

Launch the interactive web application:

```bash
streamlit run app.py
```

- Opens automatically at `http://localhost:8501`.
- **Sidebar**: Paste your OpenRouter and Tavily API keys (securely stored in session memory only).
- **Quick Topics**: Click preset buttons (e.g. *AI in Healthcare*, *Quantum Computing*) or enter any custom research query.
- **Live Progress**: Watch the 4 agents collaborate in real-time with visual status cards.
- **Output Tabs**:
  - 📄 **Synthesized Report** (with a single-click Markdown `.md` download button)
  - 🧐 **Critic Review & Recommendations**
  - 🌐 **Deep Scraped Web Content**
  - 🔍 **Raw Search Hits**

### 2. Command-Line Interface (CLI)

You can also run the research pipeline directly via Python:

```bash
python main.py
```

To research a custom topic via CLI, edit the `topic` variable in `main.py`:

```python
from src.pipeline.pipeline import run_research_pipeline

topic = "Latest advancements in solid-state batteries for electric vehicles"
result = run_research_pipeline(topic)
```

---

## 🔐 Visitor API Key Support (BYOK)

The Streamlit frontend is designed with **Bring Your Own Key (BYOK)** principles:
- **No Shared Keys**: Visitors to your deployed application provide their own API keys via password-masked input fields in the sidebar.
- **Session Isolation**: Keys are stored exclusively in Streamlit's `st.session_state` in-memory storage for that user's active session.
- **Data Protection**: API keys are never written to disk, committed to Git, or exposed to other users.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).