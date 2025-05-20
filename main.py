import os
import fitz
import pytesseract
from PIL import Image
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Import from your services folder
from services.chroma_service import ingest_document

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "backend/app/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
documents_store = {}

def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    try:
        pdf = fitz.open(file_path)
        for page in pdf:
            text += page.get_text()
    except Exception as e:
        print(f"[ERROR] PDF extraction error: {e}")
    return text

def extract_text_from_image(file_path: str) -> str:
    try:
        img = Image.open(file_path)
        return pytesseract.image_to_string(img)
    except Exception as e:
        print(f"[ERROR] OCR error: {e}")
        return ""

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    print("\n[UPLOAD] 1. Received request to /upload/")

    # 1) Save the file to disk
    print("[UPLOAD] 2. Saving file to disk...")
    file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_location, "wb") as f:
        data = await file.read()
        f.write(data)
    print(f"[UPLOAD] 3. File saved: {file.filename} ({len(data)} bytes)")

    # 2) Extract text
    print("[UPLOAD] 4. Extracting text from file...")
    if file.filename.lower().endswith(".pdf"):
        extracted_text = extract_text_from_pdf(file_location)
    elif file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        extracted_text = extract_text_from_image(file_location)
    else:
        print("[UPLOAD] 4.a Unsupported file type")
        return JSONResponse(status_code=400, content={"error": "Unsupported file type"})

    if not extracted_text.strip():
        print("[UPLOAD] 5. No text extracted (empty or failed OCR).")
        preview = "[No text extracted]"
    else:
        preview = extracted_text[:300]
        print(f"[UPLOAD] 5. Extracted text length: {len(extracted_text)}")

    # 3) Store raw text (in memory)
    documents_store[file.filename] = extracted_text
    print(f"[UPLOAD] 6. Stored raw text in memory (documents_store).")

    # 4) Ingest into ChromaDB
    print("[UPLOAD] 7. Calling ingest_document()...")
    try:
        ingest_document(file.filename, extracted_text)
        print("[UPLOAD] 8. ingest_document() returned successfully.")
    except Exception as e:
        print(f"[UPLOAD] 8.a ingest_document() raised an exception: {e}")

    # 5) Return response
    print("[UPLOAD] 9. Returning response to client.\n")
    return JSONResponse({
        "message": "File uploaded, text extracted (if any), and ingestion attempted.",
        "filename": file.filename,
        "text_preview": preview
    })
