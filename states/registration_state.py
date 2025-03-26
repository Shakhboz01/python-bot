from aiogram.fsm.state import State, StatesGroup
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from database import add_user, CYRILLIC_NAME_REGEX, PHONE_REGEX
from keyboards.keyboards import main_menu

class RegistrationState(StatesGroup):
    full_name = State()
    phone_number = State()

welcome_message_text = "✈️ <b>Добро пожаловать</b> в главное меню чат-бота Управляющей компании \"УЭР-ЮГ\". " \
                        "Здесь Вы можете оставить заявку для управляющей компании или направить свое предложение " \
                        "по управлению домом. Просто воспользуйтесь кнопками <b>меню</b>, чтобы взаимодействовать " \
                        "с функциями бота:"
full_name_mismatch_error = "⛔👑 <b>Имя</b> и <b>Фамилия</b> должны быть введены через один пробел, и должны быть " \
                           "написаны через кириллицу. Также должны быть заглавные буквы. <b>Учтите формат и попробуйте снова:</b>"

phone_number_mismatch_error = "⛔👑⛔ <b>Номер телефона</b> должен содержать 11 цифр и должен обязательно " \
                              "содержать в начале <b>+7. Учтите формат и попробуйте снова:</b>"
router = Router()
@router.message(RegistrationState.full_name)
async def process_full_name_registration(message: Message, state: FSMContext) -> None:
    if not CYRILLIC_NAME_REGEX.match(message.text):
        await message.answer(full_name_mismatch_error, parse_mode="HTML")
        return
    await state.update_data(full_name = message.text)
    await state.set_state(RegistrationState.phone_number)
    text = "📞 Теперь отправьте Ваш <b>номер телефона</b> через <b>+7</b> следующим сообщением:"
    await message.answer(text, parse_mode="HTML")

@router.message(RegistrationState.phone_number)
async def process_phone_number_registration(message: Message, state: FSMContext) -> None:
    if not PHONE_REGEX.match(message.text):
        await message.answer(phone_number_mismatch_error, parse_mode="HTML")
        return
    await state.update_data(phone_number = message.text)
    await state.set_state(RegistrationState.phone_number)
    data = await state.get_data()
    await add_user(message.from_user.id, data['full_name'], data['phone_number'])
    await state.clear()
    await message.answer(welcome_message_text, reply_markup=main_menu(), parse_mode="HTML")
