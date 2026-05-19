"""
优化后的投资者模型，增强验证和数据库集成能力
"""

import json
import os
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, validator
from sqlalchemy import create_engine, Column, String, Boolean, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Investor(BaseModel):
    """
    投资者数据模型
    """
    id: str = Field(..., description="唯一标识符")
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(..., regex=r"^\+?[1-9]\d{1,14}$")
    linkedin_url: Optional[str] = Field(
        None, description="LinkedIn个人主页URL"
    )
    investment_focus: List[str] = Field(
        default_factory=list,
        description="投资兴趣领域列表"
    )
    verified: bool = Field(False, description="验证状态")
    
    @validator("linkedin_url")
    def validate_linkedin(cls, v):
        if v and not v.startswith("https://www.linkedin.com/in/"):
            raise ValueError("LinkedIn URL必须以 https://www.linkedin.com/in/ 开头")
        return v
    
    @validator("investment_focus", each_item=True)
    def validate_focus(cls, v):
        if not v or not v.strip():
            raise ValueError("投资兴趣项不能为空")
        return v.strip()

class InvestorDB(Base):
    """数据库模型映射"""
    __tablename__ = "investors"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)
    investment_focus = Column(Text, nullable=True)
    verified = Column(Boolean, default=False)

class InvestorService:
    """投资者服务层"""
    def __init__(self, db_url: str = "sqlite:///investors.db"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def create_investor(self, investor_data: dict) -> dict:
        """创建新投资者"""
        session = self.Session()
        try:
            investor = Investor(**investor_data)
            
            # 验证邮箱唯一性
            existing = session.query(InvestorDB).filter(
                InvestorDB.email == investor.email
            ).first()
            if existing:
                raise ValueError(f"邮箱 {investor.email} 已被使用")
            
            db_investor = InvestorDB(
                id=investor.id,
                name=investor.name,
                email=investor.email,
                phone=investor.phone,
                linkedin_url=investor.linkedin_url,
                investment_focus=", ".join(investor.investment_focus),
                verified=investor.verified
            )
            session.add(db_investor)
            session.commit()
            return db_investor.dict()
        except Exception as e:
            session.rollback()
            raise ValueError(str(e))
        finally:
            session.close()
    
    def search_investors(self, **kwargs) -> List[dict]:
        """搜索投资者"""
        session = self.Session()
        try:
            query = session.query(InvestorDB)
            
            if "name" in kwargs:
                query = query.filter(InvestorDB.name.contains(kwargs["name"]))
            if "sector" in kwargs:
                query = query.filter(InvestorDB.investment_focus.contains(kwargs["sector"]))
            if "verified" in kwargs:
                query = query.filter(InvestorDB.verified == kwargs["verified"])
            
            return [i.dict() for i in query.all()]
        finally:
            session.close()