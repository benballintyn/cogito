import asyncio
import random
from functools import wraps
from typing import Callable, Tuple, Type

from loguru import logger


def async_retry(
    max_retries: int = 3,
    backoff_factor: float = 1.0,
    max_delay: float = 10.0,
    exceptions: Tuple[Type[BaseException], ...] = (Exception,),
    jitter: bool = True,
) -> Callable:
    """
    A decorator for retrying an async function with exponential backoff.

    Args:
        max_retries (int): Maximum number of retry attempts.
        backoff_factor (float): Base delay between retries (in seconds).
        max_delay (float): Maximum delay between retries.
        exceptions (tuple): A tuple of exception classes to retry on.
        jitter (bool): Whether to add random jitter to the delay.

    Returns:
        Callable: The wrapped async function with retry logic.
    """

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            attempt = 0
            while attempt <= max_retries:
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    if attempt > max_retries:
                        raise

                    # Calculate exponential backoff
                    delay = min(backoff_factor * (2 ** (attempt - 1)), max_delay)
                    if jitter:
                        delay *= random.uniform(0.8, 1.2)  # Add jitter

                    # Log the retry attemp
                    logger.debug(
                        f"Retrying {func.__name__} in {delay:.2f}s due to {e.__class__.__name__}: {str(e)}"
                    )
                    await asyncio.sleep(delay)

        return wrapper

    return decorator
