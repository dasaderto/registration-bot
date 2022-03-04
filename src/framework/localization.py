import os
import re
from collections import defaultdict
from logging import getLogger
from random import choice
from threading import Lock
from typing import Optional, Dict

import yaml
import yaml.reader
from aiogram.utils.markdown import escape_md

from src.cfg.current_config import Config

logger = getLogger(__name__)

# Fix not being able to read an Emoji because of pyyaml's ReaderError
yaml.reader.Reader.NON_PRINTABLE = \
    re.compile(u'[^\x09\x0A\x0D\x20-\x7E\x85\xA0-\uD7FF\uE000-\uFFFD\U00010000-\U0010FFFF]')

# mappings of language to localization data
_localizations: Dict[str, dict] = {}
_localization_refresh_locks: Dict[str, Lock] = defaultdict(Lock)
_localizations_last_modified: Dict[str, Optional[float]] = defaultdict(lambda: None)


def check_localization():
    # load localizations on startup to parse them and check they exist and are valid
    for filename in Config.LOCALIZATIONS_PATH.glob(f"*.yaml"):
        _get_localization(os.path.basename(filename)[:-5])


def _get_localization(lang: str) -> dict:
    with _localization_refresh_locks[lang]:
        filepath = Config.LOCALIZATIONS_PATH / f"{lang}.yaml"
        current_last_modified = os.path.getmtime(filepath)
        if current_last_modified != _localizations_last_modified[lang]:
            if lang in _localizations:
                logger.info(
                    f"Localization file changed (last modified {current_last_modified} "
                    f"!= old {_localizations_last_modified[lang]}). Reloading."
                )
            else:
                logger.info(f"Loading localization from {filepath.resolve()}")

            with filepath.open("r", encoding="utf8") as f:
                _localizations[lang] = yaml.safe_load(f)
                _localizations_last_modified[lang] = current_last_modified

    return _localizations[lang]


def get_localization(key: str, escape_markdown: bool = False, raise_on_error: bool = False, **kwargs) -> str:
    # kwargs are substituted in retrieved string by str.format() as a convenience shortcut

    language = Config.DEFAULT_LANGUAGE
    current_localization = _get_localization(language)

    try:
        try:
            for keypart in key.split("."):
                current_localization = current_localization[keypart]
        except KeyError as e:
            raise ValueError(f"Bad localization key: {key}") from e

        # support random selection from list of string options if provided
        if isinstance(current_localization, list):
            current_localization = choice(current_localization)

        assert isinstance(current_localization, str), f"Bad localization key value: {key!r}"
    except (ValueError, AssertionError) as e:
        error_str = f"Missing or bad localization key encountered: {key}"
        if raise_on_error:
            raise ValueError(error_str)

        logger.exception(error_str)
        return "<ошибка локализации, разработчики были уведомлены, извините>"

    if escape_markdown:
        current_localization = escape_md(current_localization)

    if kwargs:
        current_localization = current_localization.format(**kwargs)

    return current_localization


# convenience shortcuts
L = get_localization
