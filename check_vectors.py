# backend/app/check_vectors.py
from services.chroma_service import collection

if __name__ == "__main__":
    print("Total vectors:", collection.count())
