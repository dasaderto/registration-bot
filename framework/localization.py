import os
import re
from collections import defaultdict
from logging import getLogger
from random import choice
from threading import Lock
from typing import Optional, Dict, Iterable

import yaml
import yaml.reader
from aiogram.utils.markdown import escape_md

from cfg.current_config import Config

logger = getLogger(__name__)

# Fix not being able to read an Emoji because of pyyaml's ReaderError
yaml.reader.Reader.NON_PRINTABLE = \
    re.compile(u'[^\x09\x0A\x0D\x20-\x7E\x85\xA0-\uD7FF\uE000-\uFFFD\U00010000-\U0010FFFF]')

# mappings of language to localization data
_localizations: Dict[str, dict] = {}
_localization_refresh_locks: Dict[str, Lock] = defaultdict(Lock)
_localizations_last_modified: Dict[str, Optional[float]] = defaultdict(lambda: None)
COMMON_LOCALIZATION_LANGUAGE = "common"
RU_LOCALIZATION_LANGUAGE = "ru"


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


def get_known_languages() -> Iterable[str]:
    return _localizations.keys()


def get_localization(key: str, escape_markdown: bool = False, raise_on_error: bool = False,
                     language: Optional[str] = None, **kwargs) -> str:
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


def get_common_localization(*args, **kwargs):
    """ Shorthand for specifying language=COMMON_LOCALIZATION_LANGUAGE to get_localization. """
    if "language" in kwargs:
        logger.warning(f"'language' kwarg present in {get_common_localization.__name__} ('{kwargs['language']}'), "
                       f"overriding it to 'common'")
        kwargs["language"] = COMMON_LOCALIZATION_LANGUAGE
    return get_localization(*args, **kwargs, language=COMMON_LOCALIZATION_LANGUAGE)


def append_number_with_string(number: int, key: str, string_only: bool = False, language: Optional[str] = None) \
        -> Optional[str]:
    """
    Makes a string like {number} {lclz_string}, where `lclz_string` is a localization string
    in a form, matching to the number.
    """
    one, two, many = [s.strip() for s in L(key, language=language).split("|")]

    result = [number]

    number = abs(number) % 100
    if number >= 20:
        number %= 10

    if number >= 5 or number == 0:
        result.append(many)
    elif number == 1:
        result.append(one)
    elif number >= 2 or number <= 4:
        result.append(two)
    else:
        result.append(many)

    if string_only:
        return result[1]
    else:
        return " ".join(map(str, result))


class DeferredLocalizationString:
    """
    Sometimes it's convenient to set a localization string in a particular place outside messaging context where
    the final text cannot be resolved immediately since user language is unknown (menu buttons text, for example).

    This problem can be solved in two ways:
    1. Pass localization keys instead of resolved strings produced by L("...").
    2. Use means deferred strings resolution.

    The first approach works, but it's limited since you can't pass any kwargs to fill in the template.
    The second approach is implemented by this function. It returns an object to resolve to string later. Resolve it
    when you need the string (= you know current user language = you're in the messaging context).
    """

    def __init__(self, key: str, *args, **kwargs):
        """
        Accepts the same arguments as common.framework.localization.get_localization.
        :returns an object that allows to resolve the localization string inside messaging context in a deferred way.
        """
        self.key = key
        self.args = args
        self.kwargs = kwargs

    def resolve(self) -> str:
        return L(self.key, *self.args, **self.kwargs)


class OverriddenDeferredLocalizationString(DeferredLocalizationString):
    """
    To use in cases where LD object is needed by general component's API but a pre-defined string is known
    beforehand.
    """

    # noinspection PyMissingConstructor
    def __init__(self, string: str):
        self.key = "<overridden string, no key>"
        self.args = ()
        self.kwargs = {}
        self.string = string

    def resolve(self) -> str:
        return self.string


# convenience shortcuts
L = get_localization
LC = get_common_localization
LN = append_number_with_string
