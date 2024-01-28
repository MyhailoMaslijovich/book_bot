from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user = ReplyKeyboardMarkup(keyboard=[[KeyboardButton('Надіслати контакт',
                                    request_contact=True)]],
                            resize_keyboard=True,
                            one_time_keyboard=True )

