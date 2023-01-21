import asyncio
from os import getenv

from aiogram import Bot, types
from celery import Celery
from dotenv import load_dotenv
from pytube import YouTube

load_dotenv()
TELEGRAM_TOKEN = getenv('TELEGRAM_TOKEN')

app = Celery('tasks', broker=getenv('CELERY_BROKER', 'redis://localhost:6379/0'))
bot = Bot(token=TELEGRAM_TOKEN, parse_mode=types.ParseMode.HTML)


@app.task
def download_youtube_video(link: str, chat_id: int) -> None:
    async def process():
        video = YouTube(link)
        sent_message = await bot.send_message(chat_id=chat_id,
                                              text=f"<b>Скачиваю файл</b>\n\nНачинаю скачивать файл <code>{video.title}</code>")

        mp4_files = video.streams.filter(file_extension="mp4").order_by("resolution").desc()

        video_name = None
        resolution = None
        file_to_download = None
        for file in mp4_files:
            if file.resolution == "1440p":
                video_name = video.title
                resolution = file.resolution
                file_to_download = file

            if file_to_download is None and file.resolution == "1080p":
                video_name = video.title
                resolution = file.resolution
                file_to_download = file

        if not file_to_download:
            video_name = mp4_files[0].title
            resolution = mp4_files[0].resolution
            file_to_download = mp4_files[0]

        if file_to_download is not None:
            file_to_download.download(output_path="downloads")
            await bot.edit_message_text(chat_id=chat_id, message_id=sent_message.message_id,
                                        text=f"<b>Файл загружен</b>\n\nВидео <code>{video_name}</code> в качестве <code>{resolution}</code> "
                                             "успешно сохранено и через пару минут появится на домашнем медиа-сервере.")
        else:
            await bot.edit_message_text(chat_id=chat_id, message_id=sent_message.message_id,
                                        text="<b>Неизвестная ошибка</b>\n\nНе получается скачать данное видео. "
                                             "Попробуй еще раз позже.")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(process())


if __name__ == '__main__':
    app.start()
