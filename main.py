import asyncio
from os import getenv

from aiogram import Bot, types, Dispatcher
from dotenv import load_dotenv

from tasks import download_youtube_video

load_dotenv()
TELEGRAM_TOKEN = getenv('TELEGRAM_TOKEN')

known_tg_id = list(map(lambda id_: int(id_), getenv('TELEGRAM_ADMINS_ID', '').split(',')))
bot = Bot(token=TELEGRAM_TOKEN, parse_mode=types.ParseMode.HTML)


async def start_handler(event: types.Message):
    await event.answer(
        text="<b>Home Bot</b>\n\nСейчас я умею только скачивать видео с ютуба "
             "и загружать их для просмотра через домашний медиа-сервер. Пришли ссылку на видео, которое надо скачать.")


async def message_handler(message: types.Message):
    if message.from_user.id not in known_tg_id:
        await message.answer(text="<b>Доступ запрещен</b>\n\nТолько привилегированные пользователи могут загружать "
                                  "видео на домашний медиа-сервер.")
        return

    if not (message.text.startswith("https://youtube.com/")
            or message.text.startswith("https://www.youtube.com/")
            or message.text.startswith("https://youtu.be/")
            or message.text.startswith("https://www.youtu.be/")):
        await message.answer(
            text="<b>Неизвестная ссылка</b>\n\nВ данный момент я умею скачивать видео <b>только</b> с ютуба.")
        return

    download_youtube_video.delay(link=message.text.strip(), chat_id=message.chat.id)


async def main():
    try:
        disp = Dispatcher(bot=bot)
        disp.register_message_handler(start_handler, commands={"start"})
        disp.register_message_handler(message_handler)
        await disp.start_polling()
    finally:
        await bot.close()


if __name__ == '__main__':
    asyncio.run(main())
