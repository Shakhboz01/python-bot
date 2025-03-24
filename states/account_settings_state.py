from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from database import CYRILLIC_NAME_REGEX, PHONE_REGEX, update_full_name, update_phone_number, get_user
from aiogram import Router

from keyboards.main_keyboard import main_menu


class AccountSettingsState(StatesGroup):
    full_name = State()
    phone_number = State()

router = Router()
@router.message(AccountSettingsState.full_name)
async def edit_full_name(message: Message, state: FSMContext):
    if not full_name_regex_matches(message.text):
        await message.answer(text='incorrect full +7name')
        return
    await update_full_name(message.from_user.id, message.text)
    await state.set_state(AccountSettingsState.phone_number)
    await state.clear()
    await message.answer("✅ Full name is changed!", reply_markup=main_menu())


@router.message(AccountSettingsState.phone_number)
async def edit_phone_number(message: Message, state: FSMContext):
    if not phone_number_regex_matches(message.text):
        await message.answer(text='incorrect phone number')
        return
    await update_phone_number(message.from_user.id, message.text)
    await state.clear()
    await message.answer("✅ Phone number is changed!", reply_markup=main_menu())


def full_name_regex_matches(name: str) -> bool:
    return bool(CYRILLIC_NAME_REGEX.match(name))

def phone_number_regex_matches(phone_number: str) -> bool:
    return bool(PHONE_REGEX.match(phone_number))
