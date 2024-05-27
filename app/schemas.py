from pydantic import BaseModel
from datetime import datetime

class PDFDocumentBase(BaseModel):
    filename: str

class PDFDocumentCreate(PDFDocumentBase):
    text_content: str

class PDFDocument(PDFDocumentBase):
    id: int
    upload_date: datetime

    class Config:
        orm_mode = True

class AskQuestion(BaseModel):
    pdf_id: int
    question: str
