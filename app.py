import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables (assumes you have your GOOGLE_API_KEY set in .env file)
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
st.header("Gemini Pro LLM chatbot Application")

# Initialize chat session with Gemini Pro model
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

# Initialize session state for conversation history if not already initialized
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you today?"}]

# Display chat messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Input for user prompt
if prompt := st.chat_input():
    # Add user's message to session history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    # Get the response from Gemini Pro API
    response = chat.send_message(prompt, stream=True)
    
    # Combine all chunks into the full response text
    bot_response = ''
    for chunk in response:
        bot_response += chunk.text
    
    # Append bot's response to the conversation history
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    
    # Display the bot's response
    st.chat_message("assistant").write(bot_response)
