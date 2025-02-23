from aiogram import Router,F,html
from aiogram.types import CallbackQuery,Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from admin.callbacks import FileAction,FileCallback
from db import db_delete_file,db_update_file_enable,db_update_file_caption
from admin.buttons import edit_file_inline,edit_folder_markup
from admin.states import FileEdit,ViewFolder
from admin.filters import IsAdmin

router = Router()

@router.callback_query(FileCallback.filter(F.action == FileAction.DELETE_FILE))
async def delete_file_action(query: CallbackQuery, callback_data: FileCallback):
    is_delete = db_delete_file(callback_data.file_id)
    if is_delete:
        await query.answer("File deleted successfully")
        await query.message.delete()
    else:
        await query.answer("Faild to delete file")

@router.callback_query(FileCallback.filter(F.action == FileAction.ENABLE))
async def disable_file_action(query: CallbackQuery, callback_data: FileCallback):
    is_enable = db_update_file_enable(callback_data.file_id,False)
    if is_enable:
        await query.message.edit_reply_markup(reply_markup=edit_file_inline(callback_data.file_id,callback_data.folder_name,is_enable.is_enable))
        await query.answer("File disabled successfully")
        
    else:
        await query.answer("Faild to disable file")


@router.callback_query(FileCallback.filter(F.action == FileAction.DISABLE))
async def disable_file_action(query: CallbackQuery, callback_data: FileCallback):
    is_enable = db_update_file_enable(callback_data.file_id,True)
    if is_enable:
        await query.message.edit_reply_markup(reply_markup=edit_file_inline(callback_data.file_id,callback_data.folder_name,is_enable.is_enable))
        await query.answer("File enabled successfully")
        
    else:
        await query.answer("Faild to enable file")

@router.callback_query(FileCallback.filter(F.action == FileAction.DISABLE))
async def disable_file_action(query: CallbackQuery, callback_data: FileCallback):
    is_enable = db_update_file_enable(callback_data.file_id,True)
    if is_enable:
        await query.message.edit_reply_markup(reply_markup=edit_file_inline(callback_data.file_id,is_enable.is_enable))
        await query.answer("File enabled successfully")
        
    else:
        await query.answer("Faild to enable file")

@router.callback_query(FileCallback.filter(F.action == FileAction.EDIT_CAPTION))
async def edit_caption_action(query: CallbackQuery, callback_data: FileCallback,state : FSMContext):
    await state.set_state(FileEdit.caption)
    await state.update_data(file_id=callback_data.file_id,folder_name=callback_data.folder_name)
    await query.answer()
    await query.message.answer("Send caption for this file\n\nUse /empty to remove caption")

@router.message(Command(commands="cancel"),IsAdmin(),FileEdit.caption)
async def on_cancel(message : Message,state : FSMContext):
    await state.set_state(ViewFolder.action)
    data = await state.get_data()
    await message.answer("Canceled.")
    await message.answer(f"Editing {data["folder_name"]}\n\n{html.bold("View files")}\nView all files you uploaded and manage them\n\n{html.bold("Add new file")}\nAdd new file to this group file\n\n{html.bold("Edit description")}\nEdit group file description",reply_markup=edit_folder_markup())


@router.message(Command(commands="empty"),IsAdmin(),FileEdit.caption)
async def remove_caption_state(message : Message,state : FSMContext):
    data = await state.get_data()
    is_remove = db_update_file_caption(data["file_id"],None)
    if is_remove:
        await message.answer("Caption removed")
    else:
        await message.answer("Faild to remove caption")
    
    await state.update_data(foldername=data["folder_name"])
    await state.set_state(ViewFolder.action)
    await message.answer(f"Editing {data["folder_name"]}\n\n{html.bold("View files")}\nView all files you uploaded and manage them\n\n{html.bold("Add new file")}\nAdd new file to this group file\n\n{html.bold("Edit description")}\nEdit group file description",reply_markup=edit_folder_markup())


@router.message(F.text,IsAdmin(),FileEdit.caption)
async def edit_caption_state(message : Message,state : FSMContext):
    data = await state.get_data()
    is_edit = db_update_file_caption(data["file_id"],message.text)
    if is_edit:
        await message.answer("Caption changed")
    else:
        await message.answer("Faild to change caption")

    await state.update_data(foldername=data["folder_name"])
    await state.set_state(ViewFolder.action)
    await message.answer(f"Editing {data["folder_name"]}\n\n{html.bold("View files")}\nView all files you uploaded and manage them\n\n{html.bold("Add new file")}\nAdd new file to this group file\n\n{html.bold("Edit description")}\nEdit group file description",reply_markup=edit_folder_markup())
