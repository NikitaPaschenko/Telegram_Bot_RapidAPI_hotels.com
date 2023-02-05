from typing import Callable
import time
import functools
from loguru import logger


def func_logger(func: Callable) -> Callable:
    """
    Декоратор функций для логирования работы чат-бота
    :param func: функция
    :return: задекорированная функция
    """

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        try:
            logger.debug(f'{func.__name__} начала работу')
            start = time.time()
            value = func(*args, **kwargs)
            work_time = time.time() - start
            logger.debug(f'{func.__name__} завершила работу '
                         f'(время - {work_time:.5f} с)')
            return value
        except Exception as exc:
            logger.error(exc)

    return wrapped
