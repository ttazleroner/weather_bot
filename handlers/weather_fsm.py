from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from services.weather_api import WeatherService
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state 
from lexicon.lexicon import LEXICON
from config. config import load_config

config = load_config()

weather_service = WeatherService(api_key=config.api.api)

class WeatherFSM(StatesGroup):
    waiting_city = State()
    
router = Router()
    
@router.message(F.text == LEXICON ['pogoda_button'])
async def start_fsm(message: Message, state: FSMContext):
    await message.answer('🌍Напишите название вашего города:')
    await state.set_state(WeatherFSM.waiting_city)

@router.message(WeatherFSM.waiting_city)
async def change_city(message: Message, state:FSMContext):
    city_name = message.text
    weather_response = await weather_service.get_weather(city_name)
    
    if weather_response is None:
        await message.answer('Сбой связи. Попробуй позже.')
        await state.clear()
        return

    if not weather_response.get("ok"):
        await message.answer('Такого города нет. Проверьте название и напишите еще раз.')
        return
    actual_weather = weather_response["data"]
    
    try:
        user_city = actual_weather['name']
        temp = actual_weather['main']['temp']
        yeat_on_tha_line = actual_weather['weather'][0]['description'].capitalize()
        text = (
            f"☁️ <b>Погода в городе {user_city}</b>\n\n"
            f"🌡 Температура: <b>{temp}°C</b>\n"
            f"🏙 На улице: {yeat_on_tha_line}"
        )
        await message.answer(text, parse_mode="HTML")
        await state.clear()

    except KeyError as e:
        print(f'Не парсит сайтик (кривой JSON от API): {e}')
        await message.answer('🛠 Произошла ошибка при сборе данных о погоде. Попробуйте позже.')
        await state.clear()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # weather_data = await weather_service.get_weather(city_name)
    # if weather_data is None:
    #     await message.answer('Такого города нет. Проверьте название и напишите еще раз.')
    #     return
    # try:
    #     user_city = weather_data['name']
    #     temp = weather_data['main']['temp']
    #     yeat_on_tha_line = weather_data['weather'][0]['description'].capitalize()
        
    #     text = (
    #         f"🌤 <b>Погода в городе {user_city}</b>\n\n"
    #         f"🌡 Температура: <b>{temp}°C</b>\n"
    #         f"🏙️ На улице: {yeat_on_tha_line}"
    #     )
        
    #     await message.answer(text)
        
    #     await state.clear()
        
    # except KeyError as e:
    #     print(f'Не парсит сайтик: {e}')
    #     await message.answer('🛠 Произошла ошибка при сборе данных о погоде. Попробуйте позже.')
    #     await state.clear()