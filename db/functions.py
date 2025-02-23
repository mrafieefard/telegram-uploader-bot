from sqlalchemy import or_, select, desc, and_
from .base import *
from db.models import Base, User,File,Folder
from sqlalchemy.orm.attributes import flag_modified
from datetime import datetime, timezone,timedelta
from typing import Literal
import random
import traceback
Base.metadata.create_all(bind=engine)


def db_get_user(user_id) -> User:
    try:
        user_id = str(user_id)
        stmt = select(User).where(User.user_id == user_id)
        user = session.scalars(stmt)
        return user.first()
    except:
        session.rollback()
        
def db_get_admins() -> list[User]:
    try:
        stmt = select(User).where(User.is_admin == True)
        user = session.scalars(stmt)
        return user.all()
    except : 
        session.rollback()

def db_create_admin(user_id):
    user = db_get_user(user_id)
    if user:
        user.is_admin = True
    else:
        user = User(user_id=user_id,is_admin = True)
        session.add(user)

    try:
        session.commit()
        return user
    except:
        session.rollback()
        return False
    
def db_create_file(file_id,file_type,caption):
    file = File(id="".join([random.choice("abcde1234567890") for _ in range(24)]),file_id = file_id,file_type=file_type,caption=caption)
    session.add(file)

    try:
        session.commit()
        return file
    except:
        traceback.print_exc()
        session.rollback()
        return False
    
def db_create_folder(link_id,name,description,file_ids):
    folder = Folder(link_id = link_id,name=name,description=description,file_ids=file_ids)
    session.add(folder)

    try:
        session.commit()
        return folder
    except:
        traceback.print_exc()
        session.rollback()
        return False
    
def db_check_filename(name):
    try:
        stmt = select(Folder).where(Folder.name == name)
        user = session.scalars(stmt)
        return user.first() != None
    except : 
        session.rollback()

def db_get_folder(link_id):
    try:
        stmt = select(Folder).where(Folder.link_id == link_id)
        user = session.scalars(stmt)
        return user.first()
    except : 
        session.rollback()

def db_get_folder_name(name):
    try:
        stmt = select(Folder).where(Folder.name == name)
        user = session.scalars(stmt)
        return user.first()
    except : 
        session.rollback()

def db_get_folders():
    try:
        stmt = select(Folder)
        folders = session.scalars(stmt)
        return folders.all()
    except : 
        session.rollback()

def db_get_file(id):
    try:
        stmt = select(File).where(File.id == id)
        user = session.scalars(stmt)
        return user.first()
    except : 
        session.rollback()

def db_delete_file(id):
    file = db_get_file(id)
    if not file:
        return True

    session.delete(file)

    try:
        session.commit()
        return True
    except:
        session.rollback()
        return False

def db_update_folder_file_ids(link_id,file_ids):
    folder = db_get_folder(link_id)

    if not folder:
        return False
    
    folder.file_ids = file_ids
    flag_modified(folder,"file_ids")
    try:
        session.commit()
        return folder
    except Exception as e:
        session.rollback()
        return False

def db_update_file_enable(id,status):
    file = db_get_file(id)
    if not file:
        return False
    
    file.is_enable = status

    try:
        session.commit()
        return file
    except Exception as e:
        session.rollback()
        return False
    
def db_update_file_caption(id,caption : None | str):
    file = db_get_file(id)
    if not file:
        return False
    
    file.caption = caption

    try:
        session.commit()
        return file
    except Exception as e:
        session.rollback()
        return False