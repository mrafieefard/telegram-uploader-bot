from aiogram.types import ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup
from admin.callbacks import FileCallback,FileAction

def admin_main_menu_markup():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Add new file"),KeyboardButton(text="View uploaded files")],
    ],resize_keyboard=True)

def page_markup(items: list[str], page: int, max_items_per_page: int, items_in_row: int = 2):
    start_index = (page - 1) * max_items_per_page
    end_index = start_index + max_items_per_page

    max_page = (len(items) + max_items_per_page - 1) // max_items_per_page
    
    selected_items = items[start_index:end_index]

    selected_items = [KeyboardButton(text=str(item)) for item in selected_items]

    buttons = [selected_items[i:i + items_in_row] for i in range(0, len(selected_items), items_in_row)]
    nav_buttons = []
    if page > 1:
        nav_buttons.append(KeyboardButton(text="⬅️"))
    if page < max_page:
        nav_buttons.append(KeyboardButton(text="➡️"))
    
    buttons.append(nav_buttons)

    return ReplyKeyboardMarkup(keyboard=buttons,resize_keyboard=True)

def edit_folder_markup():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="View files"),KeyboardButton(text="Add new file")],
        [KeyboardButton(text="Edit description")],
        [KeyboardButton(text="Back")]
    ],resize_keyboard=True)

def edit_file_inline(file_id,enable):
    return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🟢 Enabled",callback_data=FileCallback(file_id=file_id,action=FileAction.ENABLE).pack()) if enable else InlineKeyboardButton(text="🔴 Disabled",callback_data=FileCallback(file_id=file_id,action=FileAction.DISABLE).pack())],
            [InlineKeyboardButton(text="Edit caption",callback_data=FileCallback(file_id=file_id,action=FileAction.EDIT_CAPTION).pack()),InlineKeyboardButton(text="Edit file",callback_data=FileCallback(file_id=file_id,action=FileAction.EDIT_FILE).pack())],
            [InlineKeyboardButton(text="Delete File",callback_data=FileCallback(file_id=file_id,action=FileAction.DELETE_FILE).pack())]
        ])