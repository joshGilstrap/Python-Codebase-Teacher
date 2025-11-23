# Codebase Teacher: Local AI RAG Agent

Codebase Teacher is a fully local RAG (Retrieval-Augmented Generation) application designed to help you understand, refactor, and document your own code.

Unlike cloud tools, this runs 100% offline using Ollama and FAISS. You simply paste the path to your local project, and the AI scans your files, allowing you to ask questions like "How does the authentication logic work?" or "Where is the user data stored?" without your proprietary code ever leaving your machine.

Demo

<img width="1919" height="993" alt="Screenshot 2025-11-22 220035" src="https://github.com/user-attachments/assets/c3bca63d-8d23-4806-89bf-07606ead3390" />

## Tech Stack

App Framework: Streamlit

LLM Orchestration: LangChain (Classic & Community)

Local Inference: Ollama (llama3.2)

Vector Store: FAISS

Embeddings: HuggingFace (all-MiniLM-L6-v2)

Data Processing: Custom os.walk loader + TextLoader

## Installation & Setup

1. Prerequisites

- Python 3.10+ installed.

- Ollama installed and running.

2. Pull the Model

- Open terminal and pull the Llama 3.2 model:

- `ollama pull llama3.2`

3. Clone & Install
```
git clone [https://github.com/YOUR_USERNAME/codebase-teacher.git](https://github.com/YOUR_USERNAME/codebase-teacher.git)
cd codebase-teacher

# Create Virtual Environment
- python -m venv venv

# Activate Environment
- venv\Scripts\activate (Windows) or source venv/bin/activate (Mac/Linux)

# Install Dependencies
- pip install -r requirements.txt
```
4. Run the App
- `streamlit run app.py`


## How It Works

The user pastes a local codebase directory and the app walks through each file looking for only certain files (.py, .md, .json, .txt). LangChain
provides the RecursiveCharacterTextSplitter that can be specifically configured to process a certain programming language, we choose Python here.
The splitter tries to group functions and classes together to prevent cut-offs. The all-MiniLM-L6-v2 model is leveraged to convert the chunks of code
into vectors for processing, this process happens completely offline. FAISS is then used to store the vectors in RAM as Windows likes to block multiple
programs from touching the same temp file on hard disk. When a user asks a question relevant code chunks are sent to Llama 3.2 via Ollama and is prompted
to answer the question based solely on the context given.

## Troubleshooting

requirements.txt not installing:  
If you get install errors follow these steps:
1. Paste this in you virtual environment console:  
   ```pip install streamlit langchain langchain-community langchain-text-splitters langchain-huggingface python-dotenv sentence-transformers```
2. Now install an earlier version of pytorch:  
   ```pip install torch==2.8.0```  
If you run into anymore loading errors just install as they pop up, there's a lot in this project

"Load a directory first" Warning:  
If you see this warning, make sure you have entered a valid absolute path in the sidebar and clicked the "Load Directory" button.

Memory Usage:  
If the app crashes during "Reading Directory...", try loading a smaller specific subfolder rather than the entire project root, or increase the chunk_size in the code to reduce the total number of vectors.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
