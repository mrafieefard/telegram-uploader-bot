from aiogram import Router,F,html
from aiogram.types import Message,ReplyKeyboardRemove,InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.utils.deep_linking import create_start_link

from admin.buttons import admin_main_menu_markup,page_markup,edit_folder_markup,edit_file_inline
from admin.filters import IsAdmin,HasFile,AnyStateFilter
from admin.states import ViewFolder,AdminState

from db import db_get_folders,db_get_folder_name,db_get_file,db_update_folder_file_ids,db_create_file
from utils import send_file,get_uploaded_file_id

router = Router()

@router.message(Command(commands="cancel"),IsAdmin(),ViewFolder.add_file)
async def on_cancel(message : Message,state : FSMContext):
    await state.set_state(ViewFolder.action)

    await message.reply('Cancelled', reply_markup=edit_folder_markup())

@router.message(F.text == admin_main_menu_markup().keyboard[0][1].text,IsAdmin(),AdminState.main)
async def view_group_files(message : Message,state : FSMContext):
    folders = db_get_folders()

    if not len(folders):
        await message.answer("There is no group exist")
        return
    await state.set_state(ViewFolder.foldername)
    await state.update_data(page=1)
    await message.answer("Select your group file to edit it",reply_markup=page_markup([group.name for group in folders],1,6))

@router.message(F.text == "➡️",IsAdmin(),ViewFolder.foldername)
async def view_group_files_next(message : Message,state : FSMContext):
    folders = db_get_folders()

    if not len(folders):
        await message.answer("There is no group exist")
        return
    data = await state.get_data()
    page = data["page"]
    await state.update_data(page=page + 1)
    await message.answer("Select your group file to edit it",reply_markup=page_markup([group.name for group in folders],page + 1,6))

@router.message(F.text == "⬅️",IsAdmin(),ViewFolder.foldername)
async def view_group_files_prev(message : Message,state : FSMContext):
    folders = db_get_folders()

    if not len(folders):
        await message.answer("There is no group exist")
        return
    await state.set_state(ViewFolder.foldername)

    data = await state.get_data()
    page = data["page"]
    await state.update_data(page=page - 1)

    await message.answer("Select your group file to edit it",reply_markup=page_markup([group.name for group in folders],page - 1,6))

@router.message(lambda F: F.text in [folder.name for folder in db_get_folders()],ViewFolder.foldername,IsAdmin())
async def select_group_files(message : Message,state : FSMContext):
    await state.update_data(foldername=message.text)
    await state.set_state(ViewFolder.action)
    await message.answer(f"Editing {html.bold(message.text)}\n\n{html.bold("View files")}\nView all files you uploaded and manage them\n\n{html.bold("Add new file")}\nAdd new file to this group file\n\n{html.bold("Edit description")}\nEdit group file description",reply_markup=edit_folder_markup())

@router.message(F.text == edit_folder_markup().keyboard[0][0].text,ViewFolder.action,IsAdmin())
async def action_view_files(message : Message,state : FSMContext):
    data = await state.get_data()
    group = db_get_folder_name(data["foldername"])
    file_ids : list[str] = group.file_ids
    for file_id in file_ids:
        file = db_get_file(file_id)
        if not file:
            file_ids.remove(file_id)
            continue
        await send_file(message,file.file_id,file.caption,file.file_type,reply_markup=edit_file_inline(file_id,file.is_enable))
    if not len(file_ids):
        await message.answer("There is no file exist on this folder")
    db_update_folder_file_ids(group.link_id,file_ids)

@router.message(F.text == edit_folder_markup().keyboard[0][1].text,ViewFolder.action,IsAdmin())
async def action_add_new_file(message : Message,state : FSMContext):
    await state.set_state(ViewFolder.add_file)
    await message.answer("Send your file ( you'll be able to edit it in view files )",reply_markup=ReplyKeyboardRemove())

@router.message(HasFile(),IsAdmin(),ViewFolder.add_file)
async def action_add_file_to_folder(message : Message,state : FSMContext):

    file_type,file_id = await get_uploaded_file_id(message)
    await state.set_state(ViewFolder.action)
    if file_id:
        data = await state.get_data()
        file_db = db_create_file(file_id,file_type,message.caption)
        folder = db_get_folder_name(data["foldername"])
        file_ids : list[str] = folder.file_ids
        file_ids.append(file_db.id)

        db_update_folder_file_ids(folder.link_id,file_ids)

        await message.answer(f"Added to folder \n\n{html.expandable_blockquote(f"File Id: {html.code(file_id)}\nFile type : {file_type.value}\nCaption : {message.caption}")}",reply_markup=edit_folder_markup())
    else:
        await message.answer("Faild to add file",reply_markup=edit_folder_markup())

@router.message(F.text == edit_folder_markup().keyboard[2][0].text,ViewFolder.action,IsAdmin())
async def back_view_files(message : Message,state : FSMContext):
    folders = db_get_folders()
    data = await state.get_data()
    if not len(folders):
        await message.answer("There is no group exist")
        return
    await state.set_state(ViewFolder.foldername)
    await message.answer("Select your group file to edit it",reply_markup=page_markup([folder.name for folder in folders],data["page"],6))