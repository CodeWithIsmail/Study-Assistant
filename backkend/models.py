# Pydantic Models for API requests and responses
from pydantic import BaseModel
from typing import List

class InitDBRequest(BaseModel):
    pdf_paths: List[str]

class InitDBResponse(BaseModel):
    status: str
    message: str
    documents_processed: int
    chunks_created: int

class AddPDFRequest(BaseModel):
    pdf_paths: List[str]

class AddPDFResponse(BaseModel):
    status: str
    message: str
    new_documents_added: int
    total_documents: int

class AskRequest(BaseModel):
    question: str

class SourceDocument(BaseModel):
    source: str
    chunk_id: str
    content_preview: str

class AskResponse(BaseModel):
    answer: str
    sources: List[SourceDocument]
    conversation_length: int
