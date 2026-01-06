from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Integer)

class AuditLog(Base):
    __tablename__ = "auditlog"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String)
    table_name = Column(String)
    target_id = Column(Integer)
    old_value = Column(Text)
    new_value = Column(Text)

    summary = Column(Text, nullable=True)
    
    timestamp = Column(DateTime(timezone=True), server_default=func.now())