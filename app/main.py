import os
import openai
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import fitz  # PyMuPDF

# Database setup
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class PDFDocument(Base):
    __tablename__ = "pdfdocuments"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    text_content = Column(String)

Base.metadata.create_all(bind=engine)

# Schemas
class PDFDocumentBase(BaseModel):
    filename: str
    text_content: str

class PDFDocumentCreate(PDFDocumentBase):
    pass

class PDFDocumentResponse(PDFDocumentBase):
    id: int

    class Config:
        orm_mode = True

class AskQuestion(BaseModel):
    pdf_id: int
    question: str

# CRUD operations
def create_pdf(db: Session, pdf: PDFDocumentCreate):
    db_pdf = PDFDocument(**pdf.dict())
    db.add(db_pdf)
    db.commit()
    db.refresh(db_pdf)
    return db_pdf

def get_pdf(db: Session, pdf_id: int):
    return db.query(PDFDocument).filter(PDFDocument.id == pdf_id).first()

# PDF text extraction service
def extract_text_from_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# FastAPI app setup
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust allowed origins for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload", response_model=PDFDocumentResponse)
async def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_location = f"files/{file.filename}"
    os.makedirs(os.path.dirname(file_location), exist_ok=True)
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    text_content = extract_text_from_pdf(file_location)
    pdf = PDFDocumentCreate(filename=file.filename, text_content=text_content)
    db_pdf = create_pdf(db=db, pdf=pdf)
    return db_pdf

@app.post("/ask")
async def ask_question(request: AskQuestion, db: Session = Depends(get_db)):
    pdf_document = get_pdf(db, pdf_id=request.pdf_id)
    if not pdf_document:
        raise HTTPException(status_code=404, detail="PDF document not found")

    pdf_text = pdf_document.text_content

    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Here is a document: {pdf_text}\nQuestion: {request.question}"}
            ],
            max_tokens=150,
            temperature=0.7,
        )
        answer = response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error processing question: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your question.")

    return {"answer": answer}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
