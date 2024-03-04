from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Меню'),
            KeyboardButton(text='Залишити відгук'),
        ],

        [
            KeyboardButton(text='Варіанти доставки'),
            KeyboardButton(text='Варіанти оплати'),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder='Що вас цікавить?'
)


del_kdb = ReplyKeyboardRemove()


start_kb2 = ReplyKeyboardBuilder()
start_kb2.add(
    KeyboardButton(text='Меню'),
    KeyboardButton(text='Залишити відгук'),
    KeyboardButton(text='Варіанти доставки'),
    KeyboardButton(text='Варіанти оплати'),
)
start_kb2.adjust(2,2)


# start_kb3 = ReplyKeyboardBuilder()
# start_kb3.attach(start_kb2)
# start_kb3.add(
#     KeyboardButton(text='Відгук'),
# )
#


test_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Відправити номер телефону', request_contact=True),
            KeyboardButton(text='Відправити локацію', request_location=True),
            KeyboardButton(text='Повернутись на головну'),

        ]
    ],
    resize_keyboard=True,
)


admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Добавити товар'),
            KeyboardButton(text='Змінити товар'),
            KeyboardButton(text='Видалити товар'),
            KeyboardButton(text='Я тільки подивитись'),

        ]
    ],
    resize_keyboard=True,
)