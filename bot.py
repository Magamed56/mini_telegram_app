from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
import logging

# Загрузка переменных из .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL", "").strip()

# Логи
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if not TOKEN:
    logger.error("Ошибка: BOT_TOKEN не задан!")
    raise SystemExit("BOT_TOKEN не задан!")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Старт
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    if WEBAPP_URL:
        btn = types.InlineKeyboardButton(
            text="Открыть мини‑приложение",
            web_app=types.WebAppInfo(url=WEBAPP_URL)
        )
        keyboard.add(btn)
        await message.answer("Нажмите кнопку, чтобы открыть мини‑приложение:", reply_markup=keyboard)
    else:
        await message.answer("WEBAPP_URL не задан.")

# Фолбек
@dp.message_handler()
async def fallback(message: types.Message):
    await message.answer("Отправьте /start чтобы получить кнопку Web App.")

# Удаляем webhook, чтобы polling точно работал
async def on_startup(dp):
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Webhook удалён (если был).")
    except Exception as e:
        logger.warning("Не удалось удалить webhook: %s", e)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

