import loguru
from aiogram import (
    Router,
    Dispatcher,
)

LOGGER = loguru.logger
LOGGER.add(
    "debug.log", format="{time} {level} {message}",
    level="DEBUG", rotation="1 GB", compression='zip'
)


# это хранится обычно в .env, но я оставил это для простоты тестирования
API_KEY = '1e680be530ac4f696004c15468c12700'
BOT_TOKEN = '7675726398:AAFsAU1nUu-GT_7XhmzzM9lqywi_yd5fN1E'

router: Router = Router()
dp: Dispatcher = Dispatcher()
