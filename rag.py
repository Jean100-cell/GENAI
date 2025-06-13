import streamlit as st
import os

# === 🔐 API Key for Gemini (hardcoded - TEMP use only)
os.environ["GOOGLE_API_KEY"] = "AIzaSyCRbS_ZD2SvZTkPHnwH52Nrjc_xZGmXwik"

# === 🧠 Imports for RAG
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from langchain_core.runnables import RunnableMap, RunnableLambda, RunnablePassthrough

# === 🧠 Init LLM (Gemini Flash)
llm = init_chat_model("gemini-2.0-flash", model_provider="google_genai", temperature=0.3)

# === 🌐 Embedding Model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# === 🚀 Streamlit UI
st.set_page_config(page_title="📄 RAG with Gemini", layout="wide")
st.title("📄 RAG App using LangChain + Gemini + FAISS")

# === 📄 File upload
uploaded_file = st.file_uploader("Upload a PDF document:", type="pdf")

# === 🔍 Ask a question
question = st.text_input("Ask a question based on the document:")

if uploaded_file and question:
    with st.spinner("Processing document and answering..."):
        try:
            # === 1. Load PDF
            loader = PyPDFLoader(uploaded_file.name)
            pages = loader.load()
            st.success(f"✅ Loaded {len(pages)} pages")

            # === 2. Split into chunks
            splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            docs = splitter.split_documents(pages)
            st.success(f"✅ Split into {len(docs)} chunks")

            # === 3. Embed and store in FAISS
            vectorstore = FAISS.from_documents(docs, embedding_model)

            # === 4. Retriever
            retriever = vectorstore.as_retriever(search_type="similarity", k=4)

            # === 5. Prompt Template
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are an expert AI assistant. Use the following context to answer the question."),
                ("human", "Context:\n{context}\n\nQuestion: {question}")
            ])

            # === 6. RAG Chain
            rag_chain = (
                RunnableMap({
                    "context": lambda x: retriever.invoke(x["question"]),
                    "question": RunnablePassthrough()
                })
                | RunnableLambda(lambda x: {
                    "context": "\n\n".join([doc.page_content for doc in x["context"]]),
                    "question": x["question"]
                })
                | prompt
                | llm
            )

            # === 7. Run chain
            response = rag_chain.invoke({"question": question})
            st.success("✅ Answer generated:")
            st.write(response.content)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
