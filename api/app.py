# api/app.py

from flask import Flask, jsonify, request
import os
import asyncio
import threading
import logging
from src.telegram_bot import main as run_bot, load_config

app = Flask(__name__)

# Global variables to manage the bot state and threading
bot_running = False
bot_thread = None

def start_bot():
    """Function to run the bot in a separate thread."""
    global bot_running

    if bot_running:
        app.logger.info("Bot is already running.")
        return

    try:
        # Load configuration
        config = load_config()

        # Create and start a new event loop for the bot
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Run the bot asynchronously
        loop.run_until_complete(run_bot())

        bot_running = True
        app.logger.info("Bot started successfully.")
    except Exception as e:
        bot_running = False
        app.logger.error(f"Failed to start bot: {e}")

@app.route('/start-bot', methods=['POST'])
def start_bot_endpoint():
    global bot_running, bot_thread

    if bot_running:
        return jsonify({'status': 'Bot is already running.'}), 200

    try:
        # Start the bot in a separate thread
        bot_thread = threading.Thread(target=start_bot, daemon=True)
        bot_thread.start()

        return jsonify({'status': 'Bot is starting...'}), 202
    except Exception as e:
        app.logger.error(f"Error starting bot: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/stop-bot', methods=['POST'])
def stop_bot():
    global bot_running

    if not bot_running:
        return jsonify({'status': 'Bot is not running.'}), 200

    try:
        # Stop the bot by interrupting the event loop
        if bot_thread and bot_thread.is_alive():
            bot_running = False
            app.logger.info("Bot stopped successfully.")
            return jsonify({'status': 'Bot stopped successfully.'}), 200
        else:
            return jsonify({'status': 'Bot is not running.'}), 200
    except Exception as e:
        app.logger.error(f"Error stopping bot: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    return jsonify({'bot_running': bot_running})

def create_app():
    """Factory function to create and configure the Flask app."""
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)

    # Additional configuration or setup can be done here

    return app

if __name__ == '__main__':
    # For production, use a WSGI server like Gunicorn
    create_app()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
