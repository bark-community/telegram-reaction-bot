from flask import Flask, jsonify, request
import os
import asyncio
import threading
import logging
from src.telegram_bot import main as run_bot, load_config

app = Flask(__name__)

# Global variable to hold the bot state
bot_running = False
bot_loop = None
bot_thread = None

def start_bot_thread():
    """Function to run the bot in a separate thread."""
    global bot_running, bot_loop
    try:
        # Load configuration
        config = load_config()

        # Create a new event loop for the bot
        bot_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(bot_loop)

        # Run the bot asynchronously
        bot_loop.run_until_complete(run_bot())

        bot_running = True
    except Exception as e:
        bot_running = False
        app.logger.error(f"Failed to start bot: {e}")

@app.route('/start-bot', methods=['POST'])
def start_bot():
    global bot_running, bot_thread

    if bot_running:
        return jsonify({'status': 'Bot is already running.'})

    try:
        # Start the bot in a separate thread
        bot_thread = threading.Thread(target=start_bot_thread, daemon=True)
        bot_thread.start()

        return jsonify({'status': 'Bot is starting...'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stop-bot', methods=['POST'])
def stop_bot():
    global bot_running, bot_loop

    if not bot_running:
        return jsonify({'status': 'Bot is not running.'})

    try:
        # Stop the bot gracefully
        if bot_loop:
            bot_loop.stop()

        bot_running = False
        return jsonify({'status': 'Bot stopped successfully.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    return jsonify({'bot_running': bot_running})

def create_app():
    """Factory function to create and configure the Flask app."""
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)

    # Any additional configuration or setup can be done here

    return app

if __name__ == '__main__':
    # For production, use a WSGI server like Gunicorn
    create_app()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
