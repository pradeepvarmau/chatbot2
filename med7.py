import streamlit as st
import spacy

# Load the pre-trained Med7 model
nlp = spacy.load("en_core_med7_lg")

# Streamlit app layout
st.title("Med7 Symptom Checker Chatbot")

# Sidebar for user information (age, sex)
st.sidebar.header("Patient Information")
age = st.sidebar.number_input("Age", min_value=1, max_value=120, value=30)
sex = st.sidebar.selectbox("Sex", ["Male", "Female"])

# Collect symptoms from user as a free text input
st.header("Describe your symptoms:")
symptom_input = st.text_area("Enter your symptoms here...")

# Process text input to extract medical entities (symptoms, diseases, etc.)
if st.button("Check Symptoms"):
    if symptom_input:
        # Process the input using Med7 NLP model
        doc = nlp(symptom_input)
        
        # Extract the recognized medical entities
        symptoms = []
        for ent in doc.ents:
            if ent.label_ in ["SYMPTOM", "DISEASE"]:  # Looking for symptoms or diseases
                symptoms.append(ent.text)
        
        # Display the extracted symptoms or conditions
        if symptoms:
            st.write("Recognized Symptoms/Conditions:")
            for symptom in symptoms:
                st.write(f"- {symptom}")
            
            # Example recommendation based on simple rules
            if "fever" in [s.lower() for s in symptoms]:
                st.write("- You might have a viral infection. Consider resting and drinking fluids.")
            if "cough" in [s.lower() for s in symptoms]:
                st.write("- A cough can be caused by various conditions. If persistent, consult a doctor.")
        else:
            st.write("No symptoms recognized. Please provide more details.")
    else:
        st.warning("Please enter your symptoms to check.")
