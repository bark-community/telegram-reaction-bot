# api/__init__.py

# Importing the Flask app to make it accessible when importing the package
from .app import app

# Define what is available when importing *
__all__ = ['app']
