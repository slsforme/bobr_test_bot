import aiohttp
from urllib.parse import urlencode
from typing import Dict

from settings import (
    API_KEY,
    LOGGER
)
from exceptions import HTTPError


async def get_data(city: str) -> str:
    BASE_URL: str = 'https://api.openweathermap.org/data/2.5/weather?'
    params: Dict = {
        'q': city,
        'lang': 'ru',
        'units': 'metric',
        'appid': API_KEY
    }

    final_url: str = BASE_URL + urlencode(params)

    async with aiohttp.ClientSession() as session:
        async with session.get(final_url) as response:
            if response.status == 200:
                data: str = await response.json()
                LOGGER.info(
                    f'Got data from API for city: {city}, '
                    f'data: {data}'
                    )
                return data

            elif response.status == 404:
                data: str = await response.json()
                LOGGER.error(
                    'Error occurred while parsing data '
                    f'from API: {data}'
                )
                raise HTTPError(404, "Город не был найден")
                return None

            else:
                data: str = await response.json()
                LOGGER.error(
                    'Error occurred while parsing data '
                    f'from API: {data}'
                )
                return None
