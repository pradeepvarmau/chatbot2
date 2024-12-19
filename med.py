import streamlit as st
import google.generativeai as genai
import os

# Configure the API key for Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # You can also directly set the key here

# Start a new chat session with MedPaLM (hypothetical model)
model = genai.GenerativeModel("medpalm-model")
chat = model.start_chat(history=[])

# Streamlit App Setup
st.set_page_config(page_title="Medical Chatbot", page_icon=":hospital:", layout="wide")
st.title("Medical Chatbot powered by MedPaLM")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Input for the user to type the question
user_input = st.text_input("Ask a medical question:", key="user_input")

# Button to submit the input
submit_button = st.button("Ask")

# If the button is pressed and there is input, send the message to the model
if submit_button and user_input:
    # Get response from MedPaLM (hypothetical)
    response = chat.send_message(user_input, stream=True)
    
    # Add the user input to the chat history
    st.session_state['chat_history'].append(("You", user_input))
    
    # Display the response and add it to the chat history
    st.subheader("Response:")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))

# Display the chat history so far
st.subheader("Chat History:")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
