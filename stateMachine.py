from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    centr = State()
    newUser = State()
    ageUser = State()
    admin = State()


class UserSize(StatesGroup):
    step1 = State()
    step2 = State()
    step3 = State()
    step3_5 = State()
    step4 = State()
    step5 = State()
    step6 = State()
    step7 = State()
    step8 = State()
    step9 = State()
    step10 = State()
    step11 = State()
    step12 = State()
    step13 = State()
    step14 = State()
    step15 = State()
    step16 = State()
    step17 = State()
    step18 = State()
    step19 = State()
    step20 = State()
    step21 = State()
    step22 = State()
    step23 = State()
    step24 = State()
    step25 = State()
    step26 = State()
    step27 = State()
    step28 = State()
    step29 = State()
    step30 = State()
    step31 = State()
    step32 = State()


class UserReg(StatesGroup):
    name = State()
    lastName = State()
    age = State()
    region = State()
    regionAnother = State()
    clothingSize = State()
    photoFront = State()
    photoBack = State()
    photoProfile = State()
    problem = State()
    problem1 = State()
    order = State()


class UserAdmin(StatesGroup):
    menu = State()


class UserMenu(StatesGroup):
    menu = State()
    meneg = State()
    registration_again = State()
    underSkirt = State()
    underTrousers = State()
    top = State()
    orderTopVse = State()
    orderSkirt = State()
    orderTrousers = State()
    orderUnderTrousers = State()
    orderUnderSkirt = State()
    orderTop = State()
