from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from datetime import datetime
import uuid
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

# Association table for document versions
document_versions = Table(
    'document_versions',
    Base.metadata,
    Column('document_id', Integer, ForeignKey('documents.id'), primary_key=True),
    Column('version_id', Integer, primary_key=True),
    Column('content', Text),
    Column('created_at', DateTime, server_default=func.now()),
    Column('author_id', String(36), nullable=False)
)

@dataclass
class DocumentVersion:
    version_id: int
    content: str
    created_at: datetime
    author_id: str

@dataclass
class Document:
    id: str
    title: str
    content: str
    created_at: datetime
    author_id: str
    versions: List[DocumentVersion] = None

class DocumentService:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)
    
    def create_document(self, title: str, content: str, author_id: str) -> Document:
        session = self.Session()
        document = Document(
            id=str(uuid.uuid4()),
            title=title,
            content=content,
            created_at=datetime.utcnow(),
            author_id=author_id,
            versions=[]
        )
        session.add(document)
        session.commit()
        session.refresh(document)
        return document
    
    def get_document(self, document_id: str) -> Optional[Document]:
        session = self.Session()
        return session.query(Document).filter_by(id=document_id).first()
    
    def update_document(self, document_id: str, content: str, author_id: str) -> Document:
        session = self.Session()
        document = session.query(Document).filter_by(id=document_id).first()
        if not document:
            return None
        
        # Create new version
        new_version = DocumentVersion(
            version_id=len(document.versions) + 1,
            content=content,
            created_at=datetime.utcnow(),
            author_id=author_id
        )
        
        document.content = content
        document.versions.append(new_version)
        session.commit()
        session.refresh(document)
        return document
    
    def delete_document(self, document_id: str, author_id: str) -> bool:
        session = self.Session()
        document = session.query(Document).filter_by(id=document_id).first()
        if not document or document.author_id != author_id:
            return False
        
        session.delete(document)
        session.commit()
        return True
    
    def get_document_history(self, document_id: str) -> List[DocumentVersion]:
        session = self.Session()
        return session.query(DocumentVersion).filter_by(document_id=document_id).order_by(
            DocumentVersion.version_id.desc()
        ).all()
    
    def revert_to_version(self, document_id: str, version_id: int, author_id: str) -> Document:
        session = self.Session()
        document = session.query(Document).filter_by(id=document_id).first()
        if not document:
            return None
        
        # Find the version
        version = session.query(DocumentVersion).filter_by(
            document_id=document_id, 
            version_id=version_id
        ).first()
        
        if not version or version.author_id != author_id:
            return None
        
        # Apply the version content
        document.content = version.content
        session.commit()
        session.refresh(document)
        return document