from functools import wraps
from typing import Union

from aiogram.bot import Bot


class BotWrapper:
    __instance: Bot = None

    def __init__(self):
        pass

    def set_instances(self, bot_: Bot):
        self.__instance = bot_

    def _send_wrapper(self, wrapped):
        @wraps(wrapped)
        def wrapper(*args, **kwargs):
            result = wrapped(*args, **kwargs)
            return result

        return wrapper

    def __getattr__(self, item):
        attr = getattr(self.__instance, item)
        if item.startswith("send_"):
            attr = self._send_wrapper(attr)

        return attr


bot: Union[Bot, BotWrapper] = BotWrapper()
