import streamlit as st
import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"


def ollama_chat(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload),
        timeout=60
    )

    if response.status_code == 200:
        return response.json().get("response", "")
    else:
        return "⚠️ AI assistant is unavailable."


def ai_assistant(context: str, username: str = ""):
    st.sidebar.divider()
    st.sidebar.subheader("🤖 AI Assistant")

    st.sidebar.caption(
        "Ask questions about this dashboard, its data, or how to use it."
    )

    if "ai_history" not in st.session_state:
        st.session_state.ai_history = []

    user_input = st.sidebar.text_input(
        "Ask me something:",
        placeholder="e.g. How do I create a ticket?"
    )

    if user_input:
        system_prompt = f"""
You are an AI assistant helping users navigate a dashboard.

Dashboard context: {context}
User: {username}

Your job:
- Explain features clearly
- Guide users step-by-step
- Do NOT hallucinate data
- Keep answers concise and helpful
"""

        full_prompt = system_prompt + "\nUser question: " + user_input

        with st.spinner("🤖 AI is thinking..."):
            answer = ollama_chat(full_prompt)

        st.session_state.ai_history.append((user_input, answer))

    # Display conversation
    for q, a in reversed(st.session_state.ai_history[-5:]):
        st.sidebar.markdown(f"**You:** {q}")
        st.sidebar.info(a)
