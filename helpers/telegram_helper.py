from telegram import Bot
from django.conf import settings


async def send_telegram_message(message):
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    await bot.send_message(chat_id=settings.TELEGRAM_CHAT_ID, text=message)
