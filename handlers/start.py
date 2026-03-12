from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram import Router, F
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon.lexicon import LEXICON
from infrastructure.database.request_start import add_user_to_db, check_users
from psycopg import AsyncConnection
from aiogram.fsm.context import FSMContext


router = Router()

button_pogoda = KeyboardButton(text=LEXICON['pogoda_button'])
button_help = KeyboardButton(text=LEXICON['help_button'])

builder = ReplyKeyboardBuilder()

builder.add(button_pogoda, button_help)

builder.adjust(1,1)

main_kb=builder.as_markup(resize_keyboard=True)

@router.message(CommandStart())
async def start_message(message: Message, conn: AsyncConnection, state: FSMContext):
    await state.clear()
    user = message.from_user
    try:
        await add_user_to_db(
            conn=conn,
            user_id=user.id,
            username=user.username
        )
        count = await check_users(conn)
        print(f'Юзеров в базе: {count}.')
    except Exception as e:
        print(f'Не получилось записать юзера в БД: {e}')
    await message.answer(text=LEXICON['/start'], reply_markup=main_kb)

@router.message(F.text == LEXICON['help_button'])
async def help_message(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['/help'])
    await state.clear()










