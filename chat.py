# Q&A Chatbot with Person and Bot Simulation

from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

load_dotenv()  # take environment variables from .env.

# Load API key from environment
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the Gemini model and chat session
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

# Function to get Gemini response
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Streamlit UI setup
st.set_page_config(page_title="Q&A Chatbot")

st.header("Chatbot Conversation between Person and Bot")

# Initialize conversation history
if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = []

# Display conversation history
def display_conversation():
    for message in st.session_state['conversation_history']:
        if message['role'] == 'person':
            st.markdown(f"**Person:** {message['text']}")
        elif message['role'] == 'bot':
            st.markdown(f"**Bot:** {message['text']}")

# Input field for user question
input_text = st.text_input("Person: Ask your question here...", key="input")

# Button to submit the question
submit_button = st.button("Ask the question")

# If the submit button is clicked
if submit_button:
    # Add person’s question to conversation history
    st.session_state['conversation_history'].append({'role': 'person', 'text': input_text})
    
    # Get bot's response
    response = get_gemini_response(input_text)
    
    # Process and display bot's response
    bot_response = ''
    for chunk in response:
        bot_response += chunk.text  # Accumulate chunks for the complete response
    
    # Add bot's response to conversation history
    st.session_state['conversation_history'].append({'role': 'bot', 'text': bot_response})
    
    # Display updated conversation
    st.subheader("Conversation")
    display_conversation()

