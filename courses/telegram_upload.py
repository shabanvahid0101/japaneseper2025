from telegram import Bot
from django.conf import settings

async def send_to_telegram(file_path, caption, bot_token, chat_id):
    bot = Bot(token=bot_token)
    if file_path.endswith(('.jpg', '.jpeg', '.png')):
        with open(file_path, 'rb') as file:
            await bot.send_photo(chat_id=chat_id, photo=file, caption=caption)
    elif file_path.endswith(('.mp4', '.mov')):
        with open(file_path, 'rb') as file:
            await bot.send_video(chat_id=chat_id, video=file, caption=caption)
    return True