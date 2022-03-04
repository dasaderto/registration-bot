import logging
from datetime import time
from logging.handlers import TimedRotatingFileHandler

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from src.cfg.current_config import Config
from src.framework.bot import bot
from src.framework.localization import check_localization
from src.handlers.user_handlers import user_phone_number_handler, user_role_setup_handler, start_command
from src.states.user_states import UserState


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


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands="start", state="*")
    dp.register_message_handler(user_phone_number_handler,
                                state=UserState.phone_number, content_types=types.ContentTypes.CONTACT)
    dp.register_message_handler(user_role_setup_handler, state=UserState.user_role)


def start_app():
    initialize_logging()
    check_localization()

    bot.set_instances(Bot(token=Config.BOT_TOKEN))
    dp = Dispatcher(bot.get_instance(), storage=MemoryStorage())
    register_handlers(dp=dp)
    logging.getLogger(__name__).debug("Start polling ...")
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    start_app()
