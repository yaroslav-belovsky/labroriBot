import asyncio
import json
import logging
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from conf import BOT_TOKEN
from commands import (START_BOT_COMMAND, BOOKS_BOT_COMMAND, BOOKS_BOT_CREATE_COMMAND,
                      BOOKS_COMMAND, BOOKS_CREATE_COMMAND)

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


@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        books_list = get_books()
        print(books_list)
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


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


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
