import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("OPENAI_API_KEY")

# Create OpenAI client
client = OpenAI(api_key=api_key)

# Streamlit page settings
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖"
)

# Title
st.title("🤖 AI Chatbot")

st.write("Ask me anything!")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:

    # Save user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate assistant response
    with st.chat_message("assistant"):

        message_placeholder = st.empty()

        full_response = ""

        try:
            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages,
                stream=True
            )

            for chunk in stream:

                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

        except Exception as e:
            st.error(f"Error: {e}")

    # Save assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )

from openai import OpenAI

client = OpenAI(
    api_key="sk-xxxxxxxxxxxxxxxx"
)
