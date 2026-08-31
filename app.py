from dotenv import load_dotenv
import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent

load_dotenv()

st.set_page_config(page_title="Research Agent", page_icon="🔍")
st.title("🔍 Research Agent with Memory")
st.caption("Ask me anything — I'll search the web and synthesize an answer.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

@st.cache_resource
def get_agent():
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )
    tools = [TavilySearch(max_results=3)]
    return create_react_agent(llm, tools)

agent = get_agent()

prompt = st.chat_input("What do you want to research?")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Researching..."):
            result = agent.invoke({
                "messages": [{"role": "user", "content": prompt}]
            })
            print(result)  # debug
            response = result["messages"][-1].content
            if isinstance(response, list):
                response = response[0].get("text", str(response))
        st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})