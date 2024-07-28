# Telegram Bot Control API

This project provides a Flask-based API to control a Telegram bot. The API allows users to start, stop, and check the status of the bot. It integrates with a Telegram bot implemented using the Telethon library.

## Project Overview

The API facilitates easy management of a Telegram bot by providing HTTP endpoints. This allows seamless integration with other services or tools to control the bot's operations without directly interfacing with the Telegram API or bot logic.

## Features

- **Start Bot**: Initialize the bot in a separate thread, allowing it to run asynchronously.
- **Stop Bot**: Gracefully stop the bot, ensuring all resources are freed and processes are terminated correctly.
- **Check Status**: Verify whether the bot is currently running.
- **Logging**: Provides detailed logging for debugging and monitoring purposes.

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/bark-community/api.git
   cd api
   ```

2. **Set Up a Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**

   Create a `.env` file in the root directory with the following content:

   ```plaintext
   TELEGRAM_API_ID=your_api_id
   TELEGRAM_API_HASH=your_api_hash
   TELEGRAM_BOT_TOKEN=your_bot_token
   OWNER_USER_ID=your_owner_user_id
   LOG_LEVEL=INFO
   ```

5. **Run the Flask API**

   ```bash
   flask run
   ```

   Alternatively, for production, use a WSGI server like Gunicorn:

   ```bash
   gunicorn --workers 3 --bind 0.0.0.0:5000 api.app:create_app
   ```

## API Endpoints

- **POST `/start-bot`**

  Start the bot. Returns a status message indicating the bot is starting.

- **POST `/stop-bot`**

  Stop the bot. Returns a status message indicating the bot has stopped.

- **GET `/status`**

  Check if the bot is running. Returns a JSON response with the bot's running status.

## Usage

Once the API is running, you can use tools like `curl`, `Postman`, or any HTTP client to interact with the endpoints:

- **Start the Bot**

  ```bash
  curl -X POST http://localhost:5000/start-bot
  ```

- **Stop the Bot**

  ```bash
  curl -X POST http://localhost:5000/stop-bot
  ```

- **Check Status**

  ```bash
  curl http://localhost:5000/status
  ```

## Logging

The application logs detailed information about its operation in the `logs` directory. This includes bot start/stop actions and any errors encountered.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

The MIT License.