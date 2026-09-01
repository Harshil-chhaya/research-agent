from dotenv import load_dotenv
import os
import json
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import ToolMessage
from memory import save_message, load_history, clear_history

load_dotenv()

st.set_page_config(page_title="Nexus — AI Research Agent", page_icon="🔍")
st.title("🔍 Nexus")
st.caption("An AI agent that searches the web, synthesizes information, and remembers your research.")

if st.button("🗑️ Clear History"):
    clear_history()
    st.session_state.messages = []
    st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = load_history()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "sources" in msg and msg["sources"]:
            with st.expander("📚 Sources"):
                for s in msg["sources"]:
                    st.markdown(f"- [{s}]({s})")

@st.cache_resource
def get_agent():
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )
    tools = [TavilySearch(max_results=3)]
    return create_react_agent(
        llm,
        tools,
        prompt="You are a research assistant. You MUST always use the search tool to find current information before answering. Never answer from memory alone."
    )

agent = get_agent()

prompt = st.chat_input("What do you want to research?")

if prompt:
    save_message("user", prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Researching..."):
            result = agent.invoke({
                "messages": [{"role": "user", "content": prompt}]
            })

            raw = result["messages"][-1].content
            if isinstance(raw, list):
                response = " ".join([item.get("text", "") for item in raw if isinstance(item, dict)])
            else:
                response = raw

            sources = []
            for msg in result["messages"]:
                if isinstance(msg, ToolMessage):
                    try:
                        content = msg.content
                        if isinstance(content, str):
                            tool_results = json.loads(content)
                            if isinstance(tool_results, dict) and "results" in tool_results:
                                for item in tool_results["results"]:
                                    if isinstance(item, dict) and "url" in item:
                                        sources.append(item["url"])
                        elif isinstance(content, list):
                            for item in content:
                                if isinstance(item, dict) and "url" in item:
                                    sources.append(item["url"])
                    except:
                        pass

        st.write(response)
        if sources:
            with st.expander("📚 Sources"):
                for s in sources:
                    st.markdown(f"- [{s}]({s})")

        save_message("assistant", response)
        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "sources": sources
        })