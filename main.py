import logging
from datetime import time
from logging.handlers import TimedRotatingFileHandler

from aiogram import Bot, Dispatcher, executor

from cfg.current_config import Config
from framework.bot import bot
from framework.localization import check_localization
from handlers.start_handler import start_command


def initialize_logging(logging_level: int = Config.DEFAULT_LOGGING_LEVEL):
    logging.basicConfig(
        level=logging_level,
        format=Config.LOGS_FORMAT
    )

    Config.LOGS_PATH.mkdir(parents=True, exist_ok=True)
    logfile_path = Config.LOGS_PATH / f'app.log'

    # noinspection PyTypeChecker
    file_handler = TimedRotatingFileHandler(
        filename=logfile_path.resolve(),
        # when='s',  # testing
        # interval=10,
        when='w0',  # every monday
        atTime=time(4, 20, 0),  # 4:20:00
        backupCount=40,  # 40 weeks, 10 month ~ 8 GB of logs at max
        encoding='utf8'
    )

    file_handler.setFormatter(logging.Formatter(fmt=Config.LOGS_FORMAT))
    file_handler.setLevel(Config.DEFAULT_LOGGING_LEVEL)
    logging.getLogger('').addHandler(file_handler)
    logging.getLogger('pika').setLevel(logging.INFO)


def connect_to_database():
    pass


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands="start", state="*")


def start_app():
    initialize_logging()
    connect_to_database()
    check_localization()

    bot.set_instances(Bot(token=Config.BOT_TOKEN))
    dp = Dispatcher(bot)
    register_handlers(dp=dp)
    logging.getLogger(__name__).debug("Start polling ...")
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    start_app()
