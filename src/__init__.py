# src/__init__.py

# Import key classes or functions to make them accessible at the package level
from .telegram_bot import create_telegram_client, create_telebot, main

# Define what is available when `import *` is used on the package
__all__ = ["create_telegram_client", "create_telebot", "main"]
