from aiogram.types import Message
from db import db_get_file,db_update_folder_file_ids
from enum import Enum


class FileType(str, Enum):
    DOCUMENT = "document"
    PHOTO = "photo"
    VIDEO = "video"
    AUDIO = "audio"
    VOICE = "voice"
    ANIMATION = "animation"
    STICKER = "sticker"
    VIDEO_NOTE = "video_note"




async def send_file(message : Message,file_id,caption,type,**kargs):
    match type:
        case "document":
            await message.answer_document(file_id,caption=caption,**kargs)
        case "photo":
            await message.answer_photo(file_id,caption=caption,**kargs)
        case "video":
            await message.answer_photo(file_id,caption=caption,**kargs)
        case "audio":
            await message.answer_audio(file_id,caption=caption,**kargs)
        case "voice":
            await message.answer_voice(file_id,caption=caption,**kargs)
        case "animation":
            await message.answer_animation(file_id,caption=caption,**kargs)
        case "sticker":
            sticker = await message.answer_sticker(file_id,**kargs)
            if caption:
                await sticker.reply(text=caption)
        case "video_note":
            video_note = await message.answer_video_note(file_id,caption=caption,**kargs)
            if caption:
                await video_note.reply(text=caption)

async def send_group_file(message : Message,link_id : str,files : list[str],show_disable = False,**kargs):
    for file_id in files:
        file = db_get_file(file_id)
        if not file:
            files.remove(file_id)
            continue
        if show_disable:
            await send_file(message,file.file_id,file.caption,file.file_type,**kargs)
        else:
            if file.is_enable:
                await send_file(message,file.file_id,file.caption,file.file_type,**kargs)

    db_update_folder_file_ids(link_id,files)


async def get_uploaded_file_id(message: Message):
    file_id = None
    file_type : FileType = None

    if message.document:
        file_id = message.document.file_id
        file_type = FileType.DOCUMENT
    elif message.photo:
        file_id = message.photo[-1].file_id
        file_type = FileType.PHOTO
    elif message.video:
        file_id = message.video.file_id
        file_type = FileType.VIDEO
    elif message.audio:
        file_id = message.audio.file_id
        file_type = FileType.AUDIO
    elif message.voice:
        file_id = message.voice.file_id
        file_type = FileType.VOICE
    elif message.animation:
        file_id = message.animation.file_id
        file_type = FileType.ANIMATION
    elif message.sticker:
        file_id = message.sticker.file_id
        file_type = FileType.STICKER
    elif message.video_note:
        file_id = message.video_note.file_id
        file_type = FileType.VIDEO_NOTE

    return file_type,file_id