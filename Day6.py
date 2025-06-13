# Make sure to install the required packages first:
# pip install langchain langchain-google-genai

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import os

# ✅ 1. Set your API key (IMPORTANT: keep it secure in real applications)
os.environ["GOOGLE_API_KEY"] = "AIzaSyCRbS_ZD2SvZTkPHnwH52Nrjc_xZGmXwik"

# ✅ 2. Create the LLM with a valid Gemini model name
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")  # Or use "gemini-2.0-flash" if available

# ✅ 3. Create a prompt template for translation
prompt = ChatPromptTemplate.from_template("Translate the following English sentence to Hindi:\n{text}")

# ✅ 4. Input text to translate
input_text = "Hello, how are you?"

# ✅ 5. Format the prompt with your input
formatted_prompt = prompt.format(text=input_text)

# ✅ 6. Call the Gemini model to get the response
response = llm.invoke(formatted_prompt)

# ✅ 7. Display the translation
print("Hindi Translation:", response.content)
