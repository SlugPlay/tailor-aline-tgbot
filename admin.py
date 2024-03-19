from aiogram import types, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from stateMachine import *
from buttone.adminKB import admin_kb
import db
from aiogram.types import FSInputFile
import json
file = open("TXT.json", 'r', encoding='utf-8')
f = json.load(file)
router = Router()


@router.message(StateFilter(UserState.admin))
async def menu(message: types.Message, state: FSMContext):
    if str(message.text) == f.get("lists"):
        db.get_all_data()
        data = FSInputFile('exported_data.xlsx')
        await message.answer_document(data)
        await state.set_state(UserState.admin)
