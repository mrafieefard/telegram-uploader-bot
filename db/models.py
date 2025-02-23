from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Column, String, Text, Integer, Boolean, ForeignKey,DateTime,Enum,JSON,func,event
from datetime import timezone,datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    user_id = Column(String,primary_key=True,unique=True)
    is_admin = Column(Boolean)

class File(Base):
    __tablename__ = "files"

    id = Column(String, primary_key=True,unique=True)
    file_id = Column(String)
    file_type = Column(Enum("document","photo","video","audio","voice","animation","sticker","video_note",name="file_types"))
    caption = Column(String,nullable=True)
    is_enable = Column(Boolean,default=True)

class Folder(Base):
    __tablename__ = "folders"

    link_id = Column(String,primary_key=True)
    name = Column(String,unique=True)
    description = Column(String)
    file_ids = Column(JSON)
    is_enable = Column(Boolean,default=True)