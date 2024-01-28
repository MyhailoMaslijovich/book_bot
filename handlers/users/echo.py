from keyboards.default.menu1 import user
from aiogram import types
from states.steps import Book_state
from loader import dp, db
from aiogram.dispatcher import FSMContext

GOOGLE_BOOK_URL_TEMPLATE = "https://lib.com.ua/uk/book/"

user_info=[]

en = {'а':'a','б':'b','в':'v','г':'h','ґ':'g','д':'d','е':'e','є':'ie','ж':'zh','з':'z','и':'i','і':'i','ї':'i',
       'й':'i','к':'k','л':'l','м':'m','н':'n','о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f','х':'kh',
       'ц':'ts','ч':'ch','ш':'sh','щ':'shch','ь':'','ю':'iu','я':'ia',
       'А':'a','Б':'b','В':'v','Г':'h','Ґ':'g','Д':'d','Е':'e','Є':'ye','Ж':'zh','З':'z','И':'i','І':'i','Ї':'yi',
       'Й':'y','К':'k','Л':'l','М':'m','Н':'n','О':'o','П':'p','Р':'r','С':'s','Т':'t','У':'u','Ф':'f','Х':'kh',
       'Ц':'ts','Ч':'ch','Ш':'sh','Щ':'shch','Ь':'','Ю':'yu','Я':'ya',' ':'-'}
def translate_to_en(text):
    translated_text = ''.join([en[char] if char in en else char for char in text])
    return translated_text


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer('Привіт! Я бот з книгами\nЩоб мною користуватись, потрібно надіслати свій контакт', reply_markup=user)
    await Book_state.Start.set()

@dp.message_handler(content_types=types.ContentType.CONTACT, state=Book_state.Start)
async def register(message: types.Message):
    user_info.append(message.contact.user_id)
    await message.answer(f'Дякую, {message.from_user.full_name}! ')
    await message.answer('Напишіть свій улюблений жанр книг')
    await Book_state.State_1.set()

@dp.message_handler(state=Book_state.State_1)
async def zhanr(message: types.Message):
    user_info.append(message.text)
    await message.answer('Напишіть Автора книги якої будете шукати')
    await Book_state.State_2.set()


@dp.message_handler(state=Book_state.State_2)
async def genre_handler(message: types.Message):
    user_info.append(message.text)
    await message.answer('Напишіть назву книги що шукаєте')
    await Book_state.State_3.set()



@dp.message_handler(state=Book_state.State_3)
async def title_handler(message: types.Message, state: FSMContext):
    title = message.text
    user_info.append(title)
    await db.user_info(user_info[0], user_info[1], user_info[2], user_info[3])

    translated_title = translate_to_en(title)
    await state.update_data(title=translated_title)

    book_url = f"{GOOGLE_BOOK_URL_TEMPLATE}{translated_title}"

    await message.answer(f"Перейдіть за посиланням для результатів пошуку: {book_url}")
