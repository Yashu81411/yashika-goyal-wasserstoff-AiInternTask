# Chatbot Theme Identifier – RAG Agent System

This project is a lightweight Retrieval-Augmented Generation (RAG) backend system built with FastAPI. It allows users to upload documents (PDFs), extract and embed their contents, and store them in ChromaDB for semantic search and retrieval.

---

## Features Implemented

### ✅ FastAPI Backend Setup
- Basic FastAPI app with asynchronous endpoints.
- Hosted on `localhost:5050`.

### ✅ File Upload Endpoint (`/upload/`)
- Accepts PDF files via POST.
- Saves file to local storage.
- Extracts text from the uploaded PDF.
- Chunks the extracted text into small segments for embedding.

### ✅ Document Chunking
- Long documents are split into smaller chunks.
- Each chunk is used to create an embedding.

### ✅ Embedding with Local LLM/Ollama
- Each document chunk is converted into an embedding using a locally running embedding model.
- Embedding vectors (length 384) are logged with debug statements.

### ✅ Vector Storage with ChromaDB
- Embedded vectors are stored in a ChromaDB collection.
- Currently using in-memory DB (persistence is optional, can be re-enabled later).
- Chunks are added to the collection in one operation.
- Handles empty input and embedding failures safely.

### ✅ Logging
- Step-by-step logging from file upload to vector storage.
- Useful for debugging and tracking each process stage.

---

## Folder Structure

chatbot_theme_identifier/
├── backend/
│ └── app/
│ ├── init.py
│ ├── main.py # FastAPI app
│ ├── check_vectors.py # Utility to print vector count
│ ├── services/
│ │ ├── init.py
│ │ ├── chroma_service.py # Handles vector DB logic
│ │ └── embed_service.py # Embedding logic
│ └── uploads/ # Folder where PDFs are stored
├── data/
├── requirements.txt
└── .env

## Requirements

Install Python dependencies: pip install -r requirements.txt

(Make sure you have Tesseract OCR installed on your machine if you plan to upload scanned images:

macOS: brew install tesseract

Ubuntu/Linux: sudo apt-get install tesseract-ocr)

# If you are using a local embedding model, you may not need an API key.
# Example for future OpenAI or Groq usage:
# OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# GROQ_API_KEY=gsk_live_XXXXXXXXXXXXXXXXXXXX

## Run the App

cd backend/app
uvicorn main:app --reload --port 5050
http://localhost:5050/docs


## Testing
[UPLOAD] 1. Received request to /upload/
[UPLOAD] 2. Saving file to disk...
[UPLOAD] 3. File saved: resume_02-05-25.pdf (80330 bytes)
[UPLOAD] 4. Extracting text from file...
[UPLOAD] 5. Extracted text length: 3024
[UPLOAD] 6. Stored raw text in memory (documents_store).
[UPLOAD] 7. Calling ingest_document()...
[DEBUG][ingest_document] Generated 3 chunks for 'resume_02-05-25.pdf'
[DEBUG][ingest_document] Computing embedding for chunk 0 of 'resume_02-05-25.pdf' …
[DEBUG][ingest_document] Embedding complete for chunk 0 (length 384)
[DEBUG][ingest_document] Computing embedding for chunk 1 of 'resume_02-05-25.pdf' …
[DEBUG][ingest_document] Embedding complete for chunk 1 (length 384)
[DEBUG][ingest_document] Computing embedding for chunk 2 of 'resume_02-05-25.pdf' …
[DEBUG][ingest_document] Embedding complete for chunk 2 (length 384)
[INFO][ingest_document] Adding 3 embeddings to in-memory ChromaDB for 'resume_02-05-25.pdf' …
[INFO][ingest_document] Successfully added 3 embeddings to in-memory ChromaDB.
[UPLOAD] 8. ingest_document() returned successfully.
[UPLOAD] 9. Returning response to client.

## Verify Chromadb stored:
cd backend/app
python check_vectors.py

output: Total vectors: 3


