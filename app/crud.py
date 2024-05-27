from sqlalchemy.orm import Session
from . import models, schemas

def get_pdf(db: Session, pdf_id: int):
    return db.query(models.PDFDocument).filter(models.PDFDocument.id == pdf_id).first()

def create_pdf(db: Session, pdf: schemas.PDFDocumentCreate):
    db_pdf = models.PDFDocument(**pdf.dict())
    db.add(db_pdf)
    db.commit()
    db.refresh(db_pdf)
    return db_pdf
