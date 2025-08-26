import asyncio
import json
import logging
import sys
import cohere

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, URLInputFile, ReplyKeyboardRemove

from conf import BOT_TOKEN, ADMI_ID
from commands import (START_BOT_COMMAND, BOOKS_BOT_COMMAND, BOOKS_BOT_CREATE_COMMAND,
                      BOOKS_COMMAND, BOOKS_CREATE_COMMAND)
from keyborts import books_keyboard_markup, BookCallback
from  models import Book
from state import BookForm

# Bot token can be obtained via https://t.me/BotFather
TOKEN = BOT_TOKEN

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()

@dp.message(Command("info"))
async def info(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.id)}!")

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {html.code(message.from_user.full_name)}!")
    logging.info(f"{html.link(message.from_user.full_name)} has started")

@dp.message(Command("who_developer"))
async def link(message: Message) -> None:
    """
        This handler receives messages with `/start` command
        """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"{html.code(message.from_user.full_name)}, don't you know?! That's Yaroslav Bilovsky!")

def get_books(file_path: str = "data.json", book_id: int | None = None):
    with open(file_path, "r", encoding="utf-8") as fp:
        books = json.load(fp)
        if book_id != None and book_id < len(books):
            return books[book_id]
        return books

def add_books(book: dict, file_path: str = "data.json"):
    books = get_books()
    if books:
        books.append(book)
        with open(file_path, "w", encoding="utf-8") as fp:
            json.dump(
                books,
                fp,
                indent=4,
                ensure_ascii=False
            )


@dp.message(BOOKS_COMMAND)
async def books(message: Message) -> None:
    data = get_books()
    markup = books_keyboard_markup(book_list=data)
    await message.answer(f"Список книг. Натисніть назву для деталей",
                            reply_markup=markup)


def generate_text(prompt):
    co = cohere.ClientV2(api_key="IyueYrhWFdmD25nVm495Xc1boJEbiIx4SWEgXveY")

    res =co.chat(
        model="command-a-03-2025",
        messages=[
        {
        "role": "user",
        "content": f"{prompt}",
        }
        ],
        )
    return res.message.content[0].text


@dp.message()
async def echo_handler(messege: Message) -> None:
    await messege.answer(f"Дякую {messege.from_user.full_name} "
                         f"Генерую відповідь, зачекайте...")
    generated_text = generate_text(messege.text)
    await messege.answer(generated_text)

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await  bot.set_my_commands(
        [
            START_BOT_COMMAND,
            BOOKS_BOT_COMMAND,
            BOOKS_BOT_CREATE_COMMAND
        ]
    )

    # And the run events dispatching
    await dp.start_polling(bot)

@dp.callback_query(BookCallback.filter())
async def callback_book(callback: CallbackQuery, callback_data: BookCallback) -> None:
    print(callback)
    print()
    print(callback_data)
    book_id = callback_data.id
    book_data = get_books(book_id=book_id)
    book = Book(**book_data)
    text = f"Книга: {book.name}\n" \
           f"Опис: {book.description}\n" \
           f"Рейтинг: {book.rating}\n" \
           f"Жанр: {book.genre}\n" \
           f"Автори: {','.join(book.authors)}\n"

    try:
        await callback.message.answer_photo(
            caption=text,
            photo=URLInputFile(
                book.poster,
                filename=f"{book.name}_cover.{book.poster.split('.')[-1]}"

            )


        )
    except Exception as e:
        await callback.messege.answer(text)
        logging.error( logging.error(f"Failed to load images for book{book.name}: {str(e)}") )

@dp.message(BOOKS_CREATE_COMMAND)
async def book_create(message: Message, state: FSMContext) -> None:
    if message.from_user.id == int(ADMI_ID):
        await state.set_state(BookForm.name)
        await message.answer(f"Введіть назву книги",
                         reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(f"Тльки адмін це може зробити!")

@dp.message(BookForm.name)
async def book_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(BookForm.description)
    await message.answer(f"Введіть опис книги",
                         reply_markup=ReplyKeyboardRemove())

@dp.message(BookForm.description)
async def book_description(message: Message, state: FSMContext) -> None:
    await state.update_data(description=message.text)
    await state.set_state(BookForm.rating)
    await message.answer(f"Введіть рейтинг книги від 1 до 10",
                         reply_markup=ReplyKeyboardRemove())

@dp.message(BookForm.rating)
async def book_rating(message: Message, state: FSMContext) -> None:
    await state.update_data(rating=message.text)
    await state.set_state(BookForm.genre)
    await message.answer(f"Введіть жанр книги",
                         reply_markup=ReplyKeyboardRemove())

@dp.message(BookForm.genre)
async def book_genre(message: Message, state: FSMContext) -> None:
    await state.update_data(genre=message.text)
    await state.set_state(BookForm.authors)
    await message.answer(f"Введіть авторів книги.\n" +
                         html.bold("Обов'яскова кома та відступ після неї"),
                         reply_markup=ReplyKeyboardRemove())

@dp.message(BookForm.authors)
async def book_authors(message: Message, state: FSMContext) -> None:
    await state.update_data(authors=[x for x in message.text.split(", ")])
    await state.set_state(BookForm.poster)
    await message.answer(f"Введіть посилання на обкладинку книги.",
                         reply_markup=ReplyKeyboardRemove())

@dp.message(BookForm.poster)
async def book_poster(message: Message, state: FSMContext) -> None:
   data = await state.update_data(poster=message.text)
   book = Book(**data)
   add_books(book.model_dump())
   await state.clear()
   await message.answer(f"Книгу {book.name} успішно додано",
                        reply_markup=ReplyKeyboardRemove())




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

