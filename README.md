# Telegram Reaction Bot

The Telegram Reaction Bot is designed to monitor message reactions in Telegram channels and notify the channel owner with detailed information about the users who reacted. Built using the Telethon and Telebot libraries, this bot is configurable, efficient, and easy to maintain.

## Features

- **Monitor Reactions**: Tracks and records reactions to messages in specified Telegram channels.
- **User Notifications**: Sends detailed notifications to the channel owner about users who reacted.
- **Error Handling**: Implements robust error handling and retry mechanisms to ensure reliability.
- **Logging**: Logs events and errors for easy debugging and monitoring.
- **Configurable**: Allows configuration through environment variables and a YAML configuration file for flexibility.

## Architecture

The bot is structured with a modular design to efficiently manage Telegram message reactions. Key components include:

- **Telethon Client**: Handles communication with the Telegram API to receive and process events.
- **Telebot API**: Utilized for sending messages that notify the channel owner of reactions.
- **Configuration Management**: Employs YAML files for non-sensitive settings and environment variables for sensitive data, enhancing security and manageability.
- **Logging**: Provides detailed logs that assist in debugging and monitoring the bot's operations.
- **Asynchronous Processing**: Uses asynchronous programming to handle events efficiently, preventing blocking operations and improving performance.

## Project Structure

```
telegram-reaction-bot/
│
├── config/
│   └── config.yaml           # Configuration file for non-sensitive settings
│
├── logs/
│   └── bot.log               # Log file for the bot's activities
│
├── src/
│   ├── __init__.py           # Makes the src directory a package
│   └── telegram_bot.py       # Main script containing bot logic
│
├── tests/
│   └── test_telegram_bot.py  # Test script for unit tests
│
├── .gitignore                # Git ignore file
├── requirements.txt          # Lists Python dependencies
└── README.md                 # Documentation file for the GitHub repo
```

## Installation

### Prerequisites

- **Python 3.12 or Higher**: Make sure you have Python installed. [Download Python](https://www.python.org/downloads/).

### Required Packages

The `requirements.txt` file includes all necessary packages:

```plaintext
telethon==1.36.0
pyTelegramBotAPI==4.21.0
PyYAML==6.0.1
```

### Steps

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/telegram-reaction-bot.git
   cd telegram-reaction-bot
   ```

2. **Set Up a Virtual Environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:

   ```bash
   export TELEGRAM_API_ID='your_api_id'
   export TELEGRAM_API_HASH='your_api_hash'
   export TELEGRAM_BOT_TOKEN='your_bot_token'
   export OWNER_USER_ID='owner_user_id'
   ```

   On Windows:

   ```cmd
   set TELEGRAM_API_ID=your_api_id
   set TELEGRAM_API_HASH=your_api_hash
   set TELEGRAM_BOT_TOKEN=your_bot_token
   set OWNER_USER_ID=owner_user_id
   ```

5. **Edit `config/config.yaml`**:

   Update the file with your settings:

   ```yaml
   telegram:
     session_name: 'my_session'

   logging:
     log_file: 'logs/bot.log'

   health_check:
     interval: 300
   ```

6. **Run the Bot**:

   ```bash
   python src/telegram_bot.py
   ```

7. **Check Logs**:

   View `logs/bot.log` for activity details.

## Usage

- **Start the Bot**: Ensure all configurations are set and execute the main script.
- **Monitor Reactions**: The bot will log reactions and send notifications to the channel owner.

## Testing

Run tests using `pytest`:

```bash
pytest tests/
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request. Ensure your code adheres to the existing style and passes all tests.

## License

The MIT License. See the LICENSE file for details.

## Support

For issues or questions, open an issue in the GitHub repository.

## References

- [Telethon on PyPI](https://pypi.org/project/Telethon/)
- [PyTelegramBotAPI on PyPI](https://pypi.org/project/pyTelegramBotAPI/)
- [PyYAML on PyPI](https://pypi.org/project/PyYAML/)