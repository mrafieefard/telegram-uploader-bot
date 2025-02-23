from aiogram.filters import Filter
from aiogram.types import Message
from aiogram.filters.state import State
from aiogram.fsm.context import FSMContext

from db import db_get_user

class IsAdmin(Filter):
    
    async def __call__(self, message: Message):
        user = db_get_user(message.from_user.id)
        if user and user.is_admin:
            return True
        
class HasFile(Filter):
    async def __call__(self,message : Message):
            return message.document or message.photo or message.video or message.audio or message.voice or message.animation or message.sticker or message.video_note

class AnyStateFilter(Filter):
    def __init__(self, *states):
        self.states = states
    
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        current_state = await state.get_state()
        return current_state in self.states