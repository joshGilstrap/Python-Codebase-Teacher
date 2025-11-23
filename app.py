import streamlit as st
import os

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

st.set_page_config("Coding Teacher", layout="wide")
st.title("Codebase Teacher")

def load_project_files(root_path):
    documents = []
    IGNORE_DIRS = {'venv', '.git', '__pycache__', 'node_modules', '.idea', '.vscode', 'build', 'dist', 'env'}
    ALLOWED_EXTENSIONS = {'.py', '.md', '.txt', '.json'}
    
    for dirpath, dirnames, filenames in os.walk(root_path):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        
        for f in filenames:
            file_extension = os.path.splitext(f)[1]
            if file_extension in ALLOWED_EXTENSIONS:
                full_path = os.path.join(dirpath, f)
                try:
                    loader = TextLoader(full_path, encoding="utf-8")
                    docs = loader.load()
                    for doc in docs:
                        doc.metadata["file_name"] = f
                        doc.metadata["file_path"] = full_path
                        documents.append(doc)
                except Exception as e:
                    print(e)
    return documents
                        
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

with st.sidebar:
    st.header("1. Upload Files")
    directory = st.text_input("Path To Codebase")
    if directory and st.button("Load Directory"):
        with st.spinner("Reading Directory..."):
            docs = load_project_files(directory)
            splitter = RecursiveCharacterTextSplitter.from_language('python')
            splits = splitter.split_documents(docs)
            embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            st.session_state.vectorstore = FAISS.from_documents(
                documents=splits,
                embedding=embeddings
            )

st.header("2. Ask Questions")
user_input = st.text_input("What do you want to know about this codebase?")

if user_input:
    if st.session_state.vectorstore is None:
        st.warning("Load a directory first")
    else:
        llm = ChatOllama(model="llama3.2")
        prompt = ChatPromptTemplate.from_template("""
            Answer the following question based only on provided context:
            
            <context>
            {context}
            </context>
            
            Question: {input}
            """
        )
        
        document_chain = create_stuff_documents_chain(llm, prompt)
        retriever = st.session_state.vectorstore.as_retriever()
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        
        with st.spinner("Thinking..."):
            response = retrieval_chain.invoke({"input": user_input})
            st.write(response["answer"])
            
            # with st.expander("View Source Context"):
            #     for i, doc in enumerate(response["context"]):
            #         st.write(f"Chunk {i+1}: {doc.page_content}")
        
