from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
import json
import os

HISTORY_FILE = "chat_history.json"

def save_message(role, content):
    history = load_history()
    history.append({"role": role, "content": content})
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)

def clear_history():
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)