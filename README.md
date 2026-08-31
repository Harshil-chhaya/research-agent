# 🔍 Research Agent with Memory

An AI agent that autonomously searches the web, synthesizes information, and returns structured summaries using LangGraph and Gemini.

## 🚀 Demo
> Ask any research question → Agent searches the web → Returns a structured, synthesized answer

## 🧠 How It Works
1. User submits a research question
2. LangGraph agent decides to use the Tavily web search tool
3. Agent reads and synthesizes search results
4. Gemini LLM generates a structured, comprehensive answer
5. Response is displayed in a clean chat interface

## 🛠️ Tech Stack
| Component | Technology |
|-----------|------------|
| LLM | Google Gemini (gemini-3.6-flash) |
| Agent Framework | LangGraph |
| Web Search | Tavily API |
| Interface | Streamlit |
| Language | Python |

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/Harshil-chhaya/research-agent.git
cd research-agent
```

### 2. Install dependencies
```bash
pip install langchain langchain-google-genai langgraph langchain-tavily streamlit python-dotenv google-genai
```

### 3. Set up environment variables
Create a `.env` file in the root directory:

GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key

### 4. Run the app
```bash
streamlit run app.py
```

## 📁 Project Structure
research-agent/
├── app.py # Main Streamlit application
├── agent.py # LangGraph agent configuration
├── .env # API keys (not tracked by git)
├── .gitignore # Git ignore rules
└── README.md # Project documentation

## 🔑 Getting API Keys
- **Gemini API**: [Google AI Studio](https://aistudio.google.com/apikey)
- **Tavily API**: [Tavily](https://tavily.com)

## 🚧 Roadmap
- [x] Web search integration
- [x] LangGraph agent loop
- [x] Streamlit chat interface
- [ ] Persistent memory across sessions
- [ ] Source citations with URLs
- [ ] Deploy to Render