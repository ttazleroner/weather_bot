import aiohttp
from typing import Optional

class WeatherService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    async def get_weather(self, city: str) -> Optional[dict]:
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric',
            'lang': 'ru'
        }
        
        try:
            timeout = aiohttp.ClientTimeout(total=10)

            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(self.base_url, params=params) as response:
                    status = response.status
                    try:
                        payload = await response.json()
                    except Exception:
                        payload = {"message": await response.text()}
                    if status == 200:
                        return {"ok": True, "data": payload}
                    msg = payload.get("message", "unknown error")
                    if status == 401:
                        return {"ok": False, "status": status, "error": "unauthorized", "message": msg}
                    if status == 404:
                        return {"ok": False, "status": status, "error": "city_not_found", "message": msg}
                    if status == 429:
                        return {"ok": False, "status": status, "error": "rate_limited", "message": msg}
                    
                    return {"ok": False, "status": status, "error": "api_error", "message": msg}
        except aiohttp.ClientError as e:
            return {"ok": False, "error": "network_error", "message": str(e)}
        except Exception as e:
            return {"ok": False, "error": "unknown_error", "message": str(e)}
        
        
        
        
        
        
        
        
        
        
        
        
        # async with aiohttp.ClientSession() as session:
        #     try:
        #         async with session.get(self.base_url, params=params) as response:
        #             if response.status == 200:
        #                 data = await response.json()
        #                 # Тут мы возвращаем чистые данные, 
        #                 # а логику текста выносим в хендлеры
        #                 return data
        #             return None
        #     except Exception as e:
        #         print(f"Ошибка при запросе к API: {e}")
        #         return None





























import aiohttp
import logging
import asyncio
import sys

logger = logging.getLogger(__name__)

async def get_json(city:str, api_key:str) -> str | None:
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    my_parasm={
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "ru"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url, params=my_parasm) as response:
                if response.status == 200:
                    data = await response.json()
                    city = data['name']
                    temp = data['main']['temp']
                    wind = data['wind']['speed']
                    desc = data['weather'][0]['description']
                    text_to_send = (
        f"🌍 <b>Погода в городе {city}</b>\n"
        f"🌡 Температура: {temp}°C\n"
        f"☁️ Небо: {desc}"
    )
                    return data
                else:
                    logger.error(f'Ошибка api {response.status}')
                    return None
    except Exception as e:
        logger.exception(f"Запрос к погоде: {e}")
        return None

if __name__ == "__main__":
    import asyncio
    # Подставь свой токен для теста
    TOKEN = "88415bb52f90bdc1bf04f2a421e1859a"
    
    async def test():
        res = await get_json("Москва", TOKEN)
        print("Ответ от API:", res)
        
    asyncio.run(test())