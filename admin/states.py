from aiogram.filters.state import State, StatesGroup

class CreateFile(StatesGroup):
    filename = State()
    description = State()
    files = State()

class ViewFolder(StatesGroup):
    foldername = State()
    action = State()
    add_file = State()


class AdminState(StatesGroup):
    main = State()