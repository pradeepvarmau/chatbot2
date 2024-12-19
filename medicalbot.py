import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables (assumes you have your GOOGLE_API_KEY set in .env file)
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.header("HealthCare - Chatbot")

# List available models in the Google Generative AI API
models = genai.list_models()

# Print available models to check what models are available
for model in models:
    print(model)
# Initialize chat session with PaLM model (assuming the model name is 'palm')
    model = genai.GenerativeModel()  # Use the correct model name (check for availability)
    chat = model.start_chat(history=[])

# Initialize session state for conversation history if not already initialized
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! Please describe your symptoms, and I will help identify possible causes."}]

# Display chat messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Input for user prompt
if prompt := st.chat_input():
    # Add user's message to session history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    # Construct healthcare-specific prompt with the user input
    healthcare_prompt = f"""
    You are a healthcare assistant. Your goal is to help users identify potential causes for their symptoms and give appropriate advice or recommendations.
    Respond politely, empathetically, and responsibly. Always encourage users to seek a healthcare professional for a proper diagnosis.
    Here's the user's symptom description:
    {prompt}

    Your response:
    """
    # Get the response from PaLM API (for symptom identification)
    response = chat.send_message(healthcare_prompt, stream=True)
    
    # Combine all chunks into the full response text
    bot_response = ''
    for chunk in response:
        bot_response += chunk.text
    
    # Append bot's response to the conversation history
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    
    # Display the bot's response
    st.chat_message("assistant").write(bot_response)
