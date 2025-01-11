"""
Utilities for configuration management.
"""
import os

from dotenv import load_dotenv
from loguru import logger

def load_envs(package_dir: str) -> None:
    """
    Use dotenv to load environment variables from multiple .env files.
    Reads the default .env file and overwrites any variables with the contents
    of .env.{ENVIRONMENT}

    Args:
        package_dir (str): The directory of the package.
    """
    environment = os.getenv("ENVIRONMENT", "DUMMY")
    load_base = load_dotenv(os.path.join(package_dir, ".env"))
    load_environment = load_dotenv(
        os.path.join(package_dir, f".env.{environment}"), override=True
    )

    if load_base and load_environment:
        logger.info(
            f"Loaded environment variables from .env and .env.{environment}"
        )
    elif load_base:
        logger.info("Loaded environment variables from .env")
    elif load_environment:
        logger.info(
            f"Loaded environment variables from .env.{environment} only"
        )
    else:
        logger.warning("No environment variables loaded")
    