import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
import os

# Fix your Google Gemini API Key directly in the code
GOOGLE_API_KEY = "AIzaSyCRbS_ZD2SvZTkPHnwH52Nrjc_xZGmXwik"  # 🔐 Replace with your real key
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Streamlit UI setup
st.set_page_config(page_title="English to French Translator", layout="centered")
st.title("🌍 English to French Translator")
st.markdown("Enter an English sentence and get a **French translation** using Google Gemini via LangChain.")

# Input field
user_input = st.text_input("✍️ Enter an English sentence:", placeholder="e.g., Hello, how are you?")
translate_button = st.button("🔁 Translate")

try:
    # Initialize Gemini LLM
    llm = ChatGoogleGenerativeAI(model="gemini- 2.0-flash", temperature=0.3)

    # Define the translation prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a professional English-to-French translator."),
        ("user", "Translate the following sentence to French:\n{sentence}")
    ])

    # Create the chain: prompt -> LLM
    chain: Runnable = prompt | llm

    # On button click, process the input
    if translate_button and user_input.strip():
        with st.spinner("Translating..."):
            try:
                # Run the chain with the user input
                response = chain.invoke({"sentence": user_input})
                french_output = response.content.strip()

                # Display result
                st.success("✅ Translation Successful!")
                st.markdown(f"**🇫🇷 French Translation:** `{french_output}`")

            except Exception as e:
                st.error(f"❌ An error occurred while translating:\n{str(e)}")

except Exception as e:
    st.error("❌ Failed to initialize Gemini model. Check your API key or model name.")
