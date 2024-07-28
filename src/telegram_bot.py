import os
import logging
import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import UpdateMessageReactions
import yaml
from logging.handlers import RotatingFileHandler
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

def load_config(config_path: str = 'config/config.yaml') -> Dict[str, Any]:
    """Load and return configuration settings from a YAML file."""
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)

            # Load sensitive data from environment variables
            config['telegram']['api_id'] = os.getenv('TELEGRAM_API_ID', config['telegram']['api_id'])
            config['telegram']['api_hash'] = os.getenv('TELEGRAM_API_HASH', config['telegram']['api_hash'])
            config['telegram']['bot_token'] = os.getenv('TELEGRAM_BOT_TOKEN', config['telegram']['bot_token'])
            config['telegram']['owner_id'] = os.getenv('OWNER_USER_ID', config['telegram']['owner_id'])

            # Check if the necessary environment variables are set
            if not all([config['telegram']['api_id'], config['telegram']['api_hash'],
                        config['telegram']['bot_token'], config['telegram']['owner_id']]):
                raise ValueError("Missing one or more required environment variables for Telegram API credentials.")

            return config
    except FileNotFoundError:
        logging.error("Configuration file not found!")
        raise
    except yaml.YAMLError as exc:
        logging.error(f"Error parsing YAML file: {exc}")
        raise


def setup_logging(log_file: str, level: str) -> None:
    """Setup logging configuration with rotation and structured logging."""
    os.makedirs('logs', exist_ok=True)  # Create logs directory if it doesn't exist

    # Define the format for log messages
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'

    # Configure logging
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, level.upper(), 'INFO'))

    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=5  # 5 MB per file, keep 5 backups
    )
    file_handler.setFormatter(logging.Formatter(log_format, date_format))

    # Stream handler for console output
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(log_format, date_format))

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


def create_telegram_client(session_name: str, api_id: str, api_hash: str) -> TelegramClient:
    """Initialize and return a Telegram client."""
    return TelegramClient(session_name, api_id, api_hash)


async def process_reactions(event: UpdateMessageReactions, client: TelegramClient, config: Dict[str, Any]) -> None:
    """Process reactions from a message and notify the owner."""
    message_id = event.message_id
    channel_id = event.peer.channel_id
    reactions = event.reactions.results

    for reaction in reactions[:config['advanced_settings']['max_reactions_per_message']]:
        emoji = reaction.reaction.emoticon
        count = reaction.count

        async for user in client.iter_participants(channel_id, limit=100):
            if user.bot or not config['advanced_settings']['fetch_user_data']:
                continue  # Skip bots or fetching user data if disabled
            username = user.username or "Unknown"
            user_id = user.id
            first_name = user.first_name or ""
            last_name = user.last_name or ""

            message = (
                f"User {username} (ID: {user_id}, Name: {first_name} {last_name}) "
                f"reacted with {emoji} to message ID {message_id} "
                f"in channel ID {channel_id} with a total count of {count} reactions."
            )
            logging.info(f"Processing reaction: {message}")
            await send_message_with_retry(client, config['telegram']['owner_id'], message,
                                          config['notifications']['retry_attempts'],
                                          config['notifications']['retry_delay'])


async def send_message(client: TelegramClient, chat_id: int, text: str) -> None:
    """Send a message to the specified chat ID."""
    try:
        await client.send_message(chat_id, text)
        logging.info(f"Message sent successfully to {chat_id}: {text}")
    except Exception as e:
        logging.error(f"Failed to send message to {chat_id}: {e}")


async def send_message_with_retry(client: TelegramClient, chat_id: int, text: str, retries: int = 3, delay: int = 2) -> None:
    """Send a message with retry logic on failure."""
    attempt = 0
    while attempt < retries:
        try:
            await send_message(client, chat_id, text)
            break
        except Exception as e:
            attempt += 1
            logging.warning(f"Failed to send message: {e}. Retry {attempt}/{retries}")
            await asyncio.sleep(delay)
            if attempt == retries:
                logging.error(f"Failed to send message after {retries} attempts: {text}")


async def monitor_bot_health(interval: int) -> None:
    """Log the bot's health status at regular intervals."""
    while True:
        logging.info("Bot health check: Active and running")
        await asyncio.sleep(interval)


async def main() -> None:
    """Main function to start the Telegram bot."""
    config = load_config()
    setup_logging(config['logging']['log_file'], os.getenv('LOG_LEVEL', config['logging']['level']))

    client = create_telegram_client(config['telegram']['session_name'],
                                    config['telegram']['api_id'],
                                    config['telegram']['api_hash'])

    @client.on(events.Raw)
    async def handler(event):
        if isinstance(event, UpdateMessageReactions):
            await process_reactions(event, client, config)

    await client.start()
    logging.info("Client is running...")
    asyncio.create_task(monitor_bot_health(config['health_check']['interval']))
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
