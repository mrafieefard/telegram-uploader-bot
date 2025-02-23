import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart,CommandObject
from aiogram.types import Message

from utils import send_group_file
from admin import admin_router
from db import db_get_folder

from config import TOKEN

dp = Dispatcher()

@dp.message(CommandStart(deep_link=True))
async def handler(message: Message, command: CommandObject):
    link_id = command.args
    group = db_get_folder(link_id)
    if not group:
        await message.answer(f"Hello, {html.bold(message.from_user.full_name)} welcome to uploader bot")
        return
    if not group.is_enable:
        await message.answer(f"Hello, {html.bold(message.from_user.full_name)} welcome to uploader bot")
        return
    await send_group_file(message,link_id,group.file_ids)
    if group.description != "":
        await message.answer(f"{html.bold("Description")}\n\n{group.description}")

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)} welcome to uploader bot")

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_router(admin_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())