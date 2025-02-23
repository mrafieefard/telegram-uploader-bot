from aiogram import Router,html,F
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from db import db_get_admins,db_create_admin,db_get_user
from .buttons import admin_main_menu_markup

from .filters import IsAdmin
from .actions import *
from .states import AdminState

router = Router()

router.include_routers(create_group_file_router,group_file_list_router,edit_file_router)

@router.message(Command(commands="admin"))
async def on_message(message : Message,state : FSMContext):
    admins = db_get_admins()
    if not len(admins):
        is_admin = db_create_admin(message.from_user.id)
        if is_admin : await message.answer("You are admin")
        await state.set_state(AdminState.main)
    else:
        user = db_get_user(message.from_user.id)
        if user and user.is_admin:
            await message.answer(f"Welcome back, {html.bold(message.from_user.full_name)}\n\nConfigure your bot here",reply_markup=admin_main_menu_markup())
            await state.set_state(AdminState.main)


