

import os
import shutil
import hashlib
import streamlit as st

from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq

from docx import Document as WordDocument
from pptx import Presentation


# ==========================================
# 1. LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv(override=True)

if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

VECTORSTORE_PATH = "/tmp/enterprise_vectorstore"
DOCUMENT_PATH = "/tmp/enterprise_documents"


# ==========================================
# 2. STREAMLIT CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Enterprise Document Intelligence",
    page_icon="📚",
    layout="wide"
)

st.title("Enterprise Document Intelligence using RAG")

st.write(
    "Upload PDF, Word and PowerPoint documents "
    "and ask questions using AI-powered document search."
)


# ==========================================
# 3. LOAD HUGGING FACE EMBEDDINGS
# ==========================================

@st.cache_resource
def load_embeddings():

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


try:

    embeddings = load_embeddings()

except Exception as e:

    st.error("Unable to load the embedding model.")
    st.exception(e)
    st.stop()


# ==========================================
# 4. SESSION STATE
# ==========================================

if "db" not in st.session_state:
    st.session_state.db = None

if "processed_files" not in st.session_state:
    st.session_state.processed_files = []


# ==========================================
# 5. DOCUMENT EXTRACTION FUNCTION
# ==========================================

def extract_documents(uploaded_files):

    documents = []

    os.makedirs(DOCUMENT_PATH, exist_ok=True)

    for file in uploaded_files:

        file_path = os.path.join(
            DOCUMENT_PATH,
            file.name
        )

        # Save uploaded document
        with open(file_path, "wb") as f:

            f.write(file.getvalue())

        extension = file.name.lower().split(".")[-1]

        # PDF EXTRACTION
        if extension == "pdf":

            loader = PyPDFLoader(file_path)

            pages = loader.load()

        # WORD EXTRACTION
        elif extension == "docx":

            word_file = WordDocument(file_path)

            text = "\n".join(
                paragraph.text
                for paragraph in word_file.paragraphs
            )

            pages = [
                Document(
                    page_content=text,
                    metadata={
                        "source": file.name,
                        "page": 0
                    }
                )
            ]

        # POWERPOINT EXTRACTION
        elif extension == "pptx":

            presentation = Presentation(file_path)

            pages = []

            for slide_number, slide in enumerate(
                presentation.slides,
                start=1
            ):

                slide_text = "\n".join(
                    shape.text
                    for shape in slide.shapes
                    if shape.has_text_frame
                )

                pages.append(
                    Document(
                        page_content=slide_text,
                        metadata={
                            "source": file.name,
                            "page": slide_number - 1
                        }
                    )
                )

        else:

            continue

        # Add source metadata
        for page in pages:

            page.metadata["source"] = file.name

        documents.extend(pages)

    return documents


# ==========================================
# 6. DOCUMENT UPLOAD
# ==========================================

st.subheader("1. Upload Documents")

uploaded_files = st.file_uploader(
    "Choose your documents",
    type=["pdf", "docx", "pptx"],
    accept_multiple_files=True
)


# ==========================================
# 7. PROCESS DOCUMENTS
# ==========================================

if st.button("Process Documents", type="primary"):

    if not uploaded_files:

        st.warning("Please upload at least one document.")

    else:

        try:

            with st.spinner(
                "Reading and processing documents..."
            ):

                # Extract document text
                documents = extract_documents(uploaded_files)

                # Remove empty pages
                documents = [
                    doc for doc in documents
                    if doc.page_content.strip()
                ]

                if not documents:

                    st.error(
                        "No readable text was found "
                        "in the uploaded documents."
                    )

                else:

                    # Split documents into chunks
                    splitter = RecursiveCharacterTextSplitter(
                        chunk_size=1000,
                        chunk_overlap=200,
                        add_start_index=True
                    )

                    chunks = splitter.split_documents(documents)

                    # Remove duplicate chunks
                    unique_chunks = {}

                    for chunk in chunks:

                        key = hashlib.md5(
                            chunk.page_content.encode("utf-8")
                        ).hexdigest()

                        unique_chunks[key] = chunk

                    chunks = list(unique_chunks.values())

                    if not chunks:

                        st.warning("No text chunks were generated.")

                    else:

                        # Delete previous vector database
                        if os.path.exists(VECTORSTORE_PATH):

                            shutil.rmtree(VECTORSTORE_PATH)

                        # Create fresh Chroma database
                        st.session_state.db = Chroma.from_documents(
                            documents=chunks,
                            embedding=embeddings,
                            ids=[
                                hashlib.md5(
                                    (
                                        doc.metadata.get("source", "")
                                        + str(doc.metadata.get("page", 0))
                                        + str(doc.metadata.get("start_index", 0))
                                        + doc.page_content
                                    ).encode("utf-8")
                                ).hexdigest()
                                for doc in chunks
                            ],
                            collection_name="enterprise_documents",
                            persist_directory=VECTORSTORE_PATH
                        )

                        st.session_state.processed_files = [
                            file.name for file in uploaded_files
                        ]

                        st.success(
                            "Documents processed successfully!"
                        )

                        st.write(
                            "Total uploaded files:",
                            len(uploaded_files)
                        )

                        st.write(
                            "Total pages / slides / sections:",
                            len(documents)
                        )

                        st.write(
                            "Total unique text chunks:",
                            len(chunks)
                        )

        except Exception as e:

            st.error("Document processing failed.")

            st.exception(e)


# ==========================================
# 8. DISPLAY PROCESSED DOCUMENTS
# ==========================================

if st.session_state.processed_files:

    st.subheader("Processed Documents")

    for filename in st.session_state.processed_files:

        st.write("📄", filename)


# ==========================================
# 9. QUESTION INPUT
# ==========================================

st.divider()

st.subheader("2. Ask Questions")

question = st.text_input(
    "Enter your question about the uploaded documents",
    placeholder="What is Moshi and what problem does it solve?"
)


# ==========================================
# 10. GENERATE ANSWER USING RAG
# ==========================================

if st.button("Get Answer", type="primary"):

    if st.session_state.db is None:

        st.warning(
            "Please upload and process documents first."
        )

    elif not question.strip():

        st.warning("Please enter a question.")

    elif not os.getenv("GROQ_API_KEY"):

        st.error(
            "Groq API key is missing. "
            "Please check your .env file."
        )

    else:

        try:

            with st.spinner(
                "Searching documents and generating your answer..."
            ):

                # Retrieve relevant document chunks
                retriever = st.session_state.db.as_retriever(
                    search_type="similarity",
                    search_kwargs={
                        "k": 5
                    }
                )

                relevant_docs = retriever.invoke(question)

                # Remove duplicate retrieved chunks
                seen = set()

                filtered_docs = []

                for doc in relevant_docs:

                    content = doc.page_content.strip()

                    if content and content not in seen:

                        seen.add(content)

                        filtered_docs.append(doc)

                if not filtered_docs:

                    st.warning(
                        "No relevant information was found "
                        "in the uploaded documents."
                    )

                else:

                    # Build document context
                    context_parts = []

                    for doc in filtered_docs:

                        source = doc.metadata.get(
                            "source",
                            "Unknown"
                        )

                        page = doc.metadata.get(
                            "page",
                            0
                        )

                        context_parts.append(
                            f"""
Source: {source}
Page: {page + 1}

Content:
{doc.page_content}
"""
                        )

                    context = "\n\n".join(context_parts)

                    # Initialize Groq LLM
                    llm = ChatGroq(
                        model="openai/gpt-oss-120b",
                        temperature=0
                    )

                    # Focused RAG prompt
                    prompt = f"""
You are an enterprise document intelligence assistant.

Your task is to answer the user's exact question
using only the retrieved document context.

STRICT INSTRUCTIONS:

1. Answer only the topic asked in the question.
2. Do not introduce unrelated research papers,
   projects, models, or topics.
3. Do not summarize the entire context.
4. Ignore references unrelated to the question.
5. Use only facts supported by the retrieved context.
6. Do not invent information.
7. If the answer is unavailable in the context,
   respond with:
   Information not available in the uploaded documents.
8. Give a clear, structured and informative answer.
9. Explain technical terms simply when useful.

DOCUMENT CONTEXT:

{context}

USER QUESTION:

{question}

ANSWER:
"""

                    # Generate answer
                    response = llm.invoke(prompt)

                    # Display answer
                    st.subheader("Answer")

                    st.write(response.content)

                    # Display source references
                    st.subheader("Source References")

                    displayed_sources = set()

                    for doc in filtered_docs:

                        source = doc.metadata.get(
                            "source",
                            "Unknown"
                        )

                        page = doc.metadata.get(
                            "page",
                            0
                        )

                        source_reference = (
                            source,
                            page
                        )

                        if source_reference not in displayed_sources:

                            displayed_sources.add(source_reference)

                            st.write(
                                f"📄 {source} - Page {page + 1}"
                            )

                    # Show retrieved text
                    with st.expander(
                        "View Retrieved Document Text"
                    ):

                        for index, doc in enumerate(
                            filtered_docs,
                            start=1
                        ):

                            st.write(f"Chunk {index}")

                            st.write(doc.page_content)

                            st.write("---")

        except Exception as e:

            st.error(
                "Unable to generate an answer. "
                "Please check your API key, model availability "
                "and internet connection."
            )

            st.exception(e)


# ==========================================
# 11. FOOTER
# ==========================================

st.divider()

st.caption(
    "Enterprise Document Intelligence | "
    "Powered by Retrieval-Augmented Generation (RAG)"
)

