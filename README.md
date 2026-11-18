
# Enterprise Document Intelligence using RAG

An AI-powered document question-answering system that uses Retrieval-Augmented Generation (RAG) to help users extract information and obtain context-aware answers from their documents.

## Live Demo

**Try the application here:**

https://enterprise-document-intelligencerag.streamlit.app/

## GitHub Repository

https://github.com/chandrika200626-debug/enterprise-document-intelligence

---

## Project Overview

Enterprise Document Intelligence is a document-based question-answering application built using Retrieval-Augmented Generation (RAG).

The application allows users to upload PDF, Word, and PowerPoint documents and ask questions based on their content.

Instead of relying only on the language model's existing knowledge, the system retrieves relevant information from uploaded documents and uses that information to generate answers.

It also displays source document names and page references to help users identify where the information came from.

## Features

- Upload multiple PDF, DOCX, and PPTX documents.
- Extract text from uploaded documents.
- Split large documents into smaller text chunks.
- Generate vector embeddings using Hugging Face.
- Store document embeddings in ChromaDB.
- Retrieve relevant document chunks using semantic similarity search.
- Generate context-grounded responses using Groq LLM.
- Display source document names and page references.
- View retrieved document text for transparency.
- Interactive web interface built using Streamlit.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application interface |
| LangChain | RAG pipeline orchestration |
| Hugging Face | Text embedding generation |
| Sentence Transformers | Semantic text embeddings |
| ChromaDB | Vector database |
| Groq API | Large Language Model inference |
| PyPDF | PDF document extraction |
| python-docx | Word document extraction |
| python-pptx | PowerPoint document extraction |

## System Architecture

The application follows a Retrieval-Augmented Generation pipeline.

```text
              Document Upload
                     |
                     v
              Text Extraction
                     |
                     v
              Text Chunking
                     |
                     v
             Embedding Generation
                     |
                     v
                 ChromaDB
               Vector Storage
                     |
                     |
              User Question
                     |
                     v
             Question Embedding
                     |
                     v
             Similarity Search
                     |
                     v
          Relevant Document Chunks
                     |
                     v
             Context Construction
                     |
                     v
                 Groq LLM
                     |
                     v
             Answer Generation
                     |
                     v
             Answer with Sources
```

## How It Works

### 1. Document Upload

Users upload PDF, DOCX, or PPTX files through the Streamlit interface.

### 2. Text Extraction

The application extracts text from uploaded documents using document-specific extraction libraries.

### 3. Text Chunking

Extracted text is divided into smaller chunks using LangChain's RecursiveCharacterTextSplitter.

This makes document retrieval more efficient and helps the language model process relevant information.

### 4. Embedding Generation

The Hugging Face Sentence Transformer model:

`sentence-transformers/all-MiniLM-L6-v2`

converts text chunks into numerical vector representations called embeddings.

### 5. Vector Storage

The generated embeddings are stored in ChromaDB, which acts as the vector database.

### 6. Semantic Retrieval

When a user submits a question, the system searches ChromaDB for the most relevant document chunks using similarity search.

### 7. Answer Generation

The retrieved document content is passed as context to the Groq-hosted language model.

The model generates an answer based on the retrieved information.

### 8. Source References

The application displays the source document name and page references associated with the retrieved information.

## Project Structure

```text
enterprise-document-intelligence/
│
├── app.py
│
├── requirements.txt
│
├── README.md
│
├── .gitignore
│
├── documents/
│
├── vectorstore/
│
└── .env
```

**Note:** The documents folder, vectorstore, virtual environment, and `.env` file are excluded from GitHub using `.gitignore`. They are created or used locally or during application execution as needed.

## Installation and Setup

### Prerequisites

- Python 3.10 or later
- pip
- Git
- Groq API key

### Step 1: Clone the Repository

```bash
git clone https://github.com/chandrika200626-debug/enterprise-document-intelligence.git
```

### Step 2: Navigate to the Project

```bash
cd enterprise-document-intelligence
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on macOS or Linux:

```bash
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Configure the API Key

Create a `.env` file in the project root directory.

Add your Groq API key:

```text
GROQ_API_KEY=your_groq_api_key
```

Replace the placeholder with your actual API key.

**Important:** Never upload your API key or `.env` file to GitHub.

### Step 6: Run the Application

```bash
streamlit run app.py
```

The application will open in your local browser.

## Deployment

The application is deployed using Streamlit Community Cloud.

Deployment process:

1. Push the project source code to GitHub.
2. Connect the GitHub repository to Streamlit Community Cloud.
3. Configure the Groq API key using Streamlit Secrets.
4. Deploy the application.
5. Access the application through its public URL.

## Example Use Case

A user uploads a research paper and asks:

**Question:** What is Moshi and how does its architecture work?

The application retrieves relevant sections from the uploaded research paper and generates an answer using the Groq language model.

The answer includes source document names and page references.

## Future Enhancements

- Support additional document formats.
- Improve document retrieval accuracy.
- Add conversation history.
- Implement hybrid search using keyword and vector retrieval.
- Add document-level metadata filtering.
- Support persistent vector storage.
- Improve answer evaluation and retrieval performance.

## Author

**Chandrika Adadala**

B.Tech Artificial Intelligence

Mahindra University

GitHub: https://github.com/chandrika200626-debug

---

**Built using Python, LangChain, ChromaDB, Hugging Face, Groq, and Streamlit.**

