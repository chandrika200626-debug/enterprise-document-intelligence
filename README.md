
# Enterprise Document Intelligence using RAG

An AI-powered document question-answering application built using Retrieval-Augmented Generation (RAG).

## Features
- Upload PDF, DOCX and PPTX files
- Extract document text
- Split text into smaller chunks
- Generate embeddings using Hugging Face
- Store embeddings in ChromaDB
- Retrieve relevant information using similarity search
- Generate answers using Groq LLM
- Display document source references

## Tech Stack
- Python
- Streamlit
- LangChain
- Hugging Face Sentence Transformers
- ChromaDB
- Groq API

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file and add:

```text
GROQ_API_KEY=your_groq_api_key
```

Run the application:

```bash
streamlit run app.py
```

## Architecture

Document Upload → Text Extraction → Chunking → Embeddings → ChromaDB → Retrieval → Groq LLM → Answer

## Author
Chandrika Adadala

