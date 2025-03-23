from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from database import add_user, CYRILLIC_NAME_REGEX, PHONE_REGEX
from keyboards.main_keyboard import main_menu

class RegistrationState(StatesGroup):
    full_name = State()
    phone_number = State()

router = Router()
@router.message(RegistrationState.full_name)
async def process_full_name_registration(message: Message, state: FSMContext) -> None:
    if not CYRILLIC_NAME_REGEX.match(message.text):
        await message.answer('name mismatch')
        return
    await state.update_data(full_name = message.text)
    await state.set_state(RegistrationState.phone_number)
    await message.answer('Now, share your phone number')

@router.message(RegistrationState.phone_number)
async def process_phone_number_registration(message: Message, state: FSMContext) -> None:
    if not PHONE_REGEX.match(message.text):
        await message.answer('phone number mismatch')
        return
    await state.update_data(phone_number = message.text)
    await state.set_state(RegistrationState.phone_number)
    data = await state.get_data()
    await add_user(message.from_user.id, data['full_name'], data['phone_number'])
    await state.clear()
    await message.answer("✅ Registration completed!", reply_markup=main_menu())
