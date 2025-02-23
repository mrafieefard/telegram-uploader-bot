from aiogram.filters.callback_data import CallbackData
from enum import Enum

class FileAction(Enum):
    ENABLE = "enable"
    DISABLE = "disable"
    EDIT_CAPTION = "edit_caption"
    EDIT_FILE = "edit_file"
    DELETE_FILE = "delete_file"

class FileCallback(CallbackData, prefix="file"):
    file_id: str
    action: FileAction