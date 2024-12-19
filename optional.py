import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables (assumes you have your GOOGLE_API_KEY set in .env file)
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.header("Healthcare Assistant Chatbot - Powered by Gemini Pro")

# Choose a suitable model for text generation (e.g., chat models like "chat-bison-001")
healthcare_model_name = 'gemini-pro'  # Example model name; replace with available one

# Initialize session state for conversation history if not already initialized
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! Please describe your symptoms, and I will help identify possible causes."}]

# Function to handle user input and process the response
def handle_user_input(user_input):
    # Add user's message to session history
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Construct the healthcare prompt based on user input
    healthcare_prompt = f"""
    You are a healthcare assistant. The user will describe their symptoms, and you need to help identify possible causes and provide general advice. 
    Respond in a clear, empathetic, and professional tone. Do not give medical diagnoses but offer helpful advice and recommend seeing a healthcare professional for further assistance.

    User's symptoms: '{user_input}'

    Please list possible causes for these symptoms, and suggest what actions the user should take next.
    """

    try:
        # Call the appropriate method for generating a response (e.g., `generate_text()`)
        response = genai.generate_text(model=healthcare_model_name, prompt=healthcare_prompt)  # Replace with actual method
        
        # Extract the response text from the result
        bot_response = response['text']  # or adjust based on actual response structure
        
        # Append bot's response to the conversation history
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

        # Display the bot's response
        st.chat_message("assistant").write(bot_response)

    except Exception as e:
        st.write(f"An error occurred: {e}")

# Display previous chat messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Input for user prompt
if user_input := st.chat_input():
    handle_user_input(user_input)
