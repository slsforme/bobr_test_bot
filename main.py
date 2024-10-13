from aiogram import Bot
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

import asyncio

from settings import (
    LOGGER,
    BOT_TOKEN,
    router,
    dp,
    )
from exceptions import HTTPError
from parser import get_data


class Form(StatesGroup):
    city_name = State()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    try:
        await state.set_state(Form.city_name)
        await message.answer(
            text=(
                "Добрый день! Напишите название города, "
                "для которого хотите получить текущую погоду."
            )
        )

    except Exception as e:
        LOGGER.error(
            "Error occured while asking user"
            f"about city: {e}"
        )


@router.message(Form.city_name)
async def send_weather_data(message: Message, state: FSMContext) -> None:
    try:
        await state.update_data(city_name=message.text)
        weather_data: str = await get_data(message.text)

        msg: str = (
            f"Текущая погода в городе {message.text}:\n"
            f"<u>{weather_data['weather'][0]['description']}</u>\n"
            f"<u>Текущая температура: {weather_data['main']['temp']}</u>\n"
            f"<u>Ощущается как: {weather_data['main']['feels_like']}</u>\n"
            f"<u>Скорость ветра: {weather_data['wind']['speed']} м/с</u>\n"
            f"<u>Влажность: {weather_data['main']['humidity']}%</u>\n"
        )

        if weather_data.get('rain') is not None:
            msg += (
                f'<u>Осадки (дождь): {weather_data['rain']['1h']} мм.</u>'
            )
        elif weather_data.get('snow') is not None:
            msg += (
                f'<u>Осадки (снег): {weather_data['snow']['1h']} мм.</u>'
            )

        await message.answer(msg)
        await state.clear()
    except HTTPError:
        LOGGER.error(
            f"Error occurred while getting data for city {message.text} - "
            "city was not found."
        )
        await message.answer(
            "Произошла ошибка при получении данных о погоде."
            " Проверьте название города."
        )

    except Exception as e:
        LOGGER.error(
            "Error occured while sending data about "
            f"data about weather: {e}"
        )
        await message.answer(
            "Произошла ошибка при получении данных"
            " о погоде на стороне сервера. Попробуйте ещё раз."
        )


async def main():
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp.include_router(router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
