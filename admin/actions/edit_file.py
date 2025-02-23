from aiogram import Router,F,html
from aiogram.types import CallbackQuery

from admin.callbacks import FileAction,FileCallback
from db import db_delete_file,db_update_file_enable
from admin.buttons import edit_file_inline

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
        await query.message.edit_reply_markup(reply_markup=edit_file_inline(callback_data.file_id,is_enable.is_enable))
        await query.answer("File disabled successfully")
        
    else:
        await query.answer("Faild to disable file")


@router.callback_query(FileCallback.filter(F.action == FileAction.DISABLE))
async def disable_file_action(query: CallbackQuery, callback_data: FileCallback):
    is_enable = db_update_file_enable(callback_data.file_id,True)
    if is_enable:
        await query.message.edit_reply_markup(reply_markup=edit_file_inline(callback_data.file_id,is_enable.is_enable))
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