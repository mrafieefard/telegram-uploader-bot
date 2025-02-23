from aiogram import Router,F,html
from aiogram.types import Message,ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.utils.deep_linking import create_start_link

from ..buttons import admin_main_menu_markup
from ..filters import IsAdmin,HasFile,AnyStateFilter
from ..states import CreateFile,AdminState
from db import db_create_file,db_create_folder,db_check_filename
from utils import get_uploaded_file_id,FileType
from pydantic import BaseModel
from typing import Optional
import random
router = Router()

class File(BaseModel):
    file_id: str
    file_type: FileType
    caption : Optional[str]

@router.message(Command(commands="cancel"),IsAdmin(),AnyStateFilter(CreateFile.filename,CreateFile.description,CreateFile.files))
async def on_cancel(message : Message,state : FSMContext):
    await state.set_state(AdminState.main)

    await message.reply('Cancelled', reply_markup=admin_main_menu_markup())

@router.message(F.text == admin_main_menu_markup().keyboard[0][0].text,IsAdmin(),AdminState.main)
async def filename_state(message : Message,state : FSMContext):
    await state.set_state(CreateFile.filename)
    await message.answer("Select a name for your file",reply_markup=ReplyKeyboardRemove())

@router.message(F.text,IsAdmin(),CreateFile.filename)
async def caption_state(message : Message,state : FSMContext):
    is_name = db_check_filename(message.text)
    if is_name:
        await message.answer("This name exist use different name")
        return
    
    await state.update_data(filename=message.text)
    await state.set_state(CreateFile.description)
    await message.answer("Write a description ( if you don't need use /skip )",reply_markup=ReplyKeyboardRemove())

@router.message(Command(commands="skip"),IsAdmin(),CreateFile.description)
async def skip_caption(message : Message,state : FSMContext):
    await message.answer("Skiped description")
    await state.set_state(CreateFile.files)
    await message.answer("Forward or upload your files here when it finish send /finish",reply_markup=ReplyKeyboardRemove())

@router.message(F.text,IsAdmin(),CreateFile.description)
async def files_state(message : Message,state : FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(CreateFile.files)
    await message.answer("Forward or upload your files here when it finish send /finish",reply_markup=ReplyKeyboardRemove())

@router.message(HasFile(),IsAdmin(),CreateFile.files)
async def process_files(message : Message,state : FSMContext):

    file_type,file_id = await get_uploaded_file_id(message)

    if file_id:
        data = await state.get_data()
        files : list[File] = data.get("files",[])
        files.append(File(file_id=file_id,file_type=file_type,caption=message.caption if message.caption else None))
        await state.update_data(files=files)

        await message.answer(f"Added to files\nUse /finish to complete \n\n{html.expandable_blockquote(f"File Id: {html.code(file_id)}\nFile type : {file_type.value}\nCaption : {message.caption}")}",reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Faild to add file",reply_markup=ReplyKeyboardRemove())

@router.message(Command(commands="finish"),IsAdmin(),CreateFile.files)
async def finish_files(message : Message,state : FSMContext):
    data = await state.get_data()
    files : list[File] = data["files"]
    link_id = "".join([random.choice("abcde1234567890") for _ in range(24)])
    file_ids = []
    for file in files:
        file_db = db_create_file(file.file_id,file.file_type.value,file.caption)
        if file_db : file_ids.append(file_db.id)

    db_create_folder(link_id,data["filename"],data.get("description",""),file_ids)
    

    link = await create_start_link(message.bot, link_id)
    await message.answer(f"Group file created \nYou can share {html.link("this link",link)} to get files")

