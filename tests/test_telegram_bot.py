import os
import unittest
from unittest.mock import patch, MagicMock
from src.telegram_bot import (
    load_config,
    setup_logging,
    create_telegram_client,
    process_reactions,
    send_message_with_retry,
    make_api_request
)
import asyncio
from telethon.tl.types import UpdateMessageReactions, PeerChannel, Reaction
from telethon.tl.custom.reaction import ReactionEmoticon


class TestTelegramBot(unittest.IsolatedAsyncioTestCase):

    @classmethod
    def setUpClass(cls):
        """Set up environment variables and logging for tests."""
        os.environ['TELEGRAM_API_ID'] = '123456'
        os.environ['TELEGRAM_API_HASH'] = 'fake_api_hash'
        os.environ['TELEGRAM_BOT_TOKEN'] = 'fake_bot_token'
        os.environ['OWNER_USER_ID'] = '123456789'
        os.environ['LOG_LEVEL'] = 'DEBUG'

        # Ensure logs directory exists for logging tests
        os.makedirs('logs', exist_ok=True)

    def test_load_config(self):
        """Test loading the configuration file and environment variables."""
        with patch.dict(os.environ, {
            'TELEGRAM_API_ID': '123456',
            'TELEGRAM_API_HASH': 'fake_api_hash',
            'TELEGRAM_BOT_TOKEN': 'fake_bot_token',
            'OWNER_USER_ID': '123456789',
            'LOG_LEVEL': 'INFO'
        }):
            config = load_config('config/config.yaml')
            self.assertEqual(config['telegram']['api_id'], '123456')
            self.assertEqual(config['telegram']['api_hash'], 'fake_api_hash')
            self.assertEqual(config['telegram']['bot_token'], 'fake_bot_token')
            self.assertEqual(config['telegram']['owner_id'], '123456789')
            self.assertEqual(config['logging']['level'], 'INFO')

    def test_setup_logging(self):
        """Test setting up logging with the specified level."""
        setup_logging('logs/test_bot.log', 'DEBUG')
        logger = logging.getLogger()
        self.assertEqual(logger.level, logging.DEBUG)

    @patch('src.telegram_bot.TelegramClient')
    def test_create_telegram_client(self, MockTelegramClient):
        """Test creating a Telegram client."""
        client = create_telegram_client('my_session', '123456', 'fake_api_hash')
        MockTelegramClient.assert_called_once_with('my_session', '123456', 'fake_api_hash')
        self.assertIsInstance(client, MagicMock)

    @patch('src.telegram_bot.requests.get')
    def test_make_api_request(self, mock_get):
        """Test making a direct API request to the Telegram Bot API."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"ok": True, "result": {"id": 123456, "is_bot": True}}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        response = make_api_request('getMe')
        self.assertTrue(response['ok'])
        mock_get.assert_called_once()

    @patch('src.telegram_bot.TelegramClient')
    async def test_send_message_with_retry(self, MockTelegramClient):
        """Test sending a message with retry logic."""
        mock_client = MockTelegramClient.return_value
        mock_client.send_message.side_effect = [Exception("Network error"), None]

        await send_message_with_retry(mock_client, 123456789, "Test message", retries=2, delay=1)
        self.assertEqual(mock_client.send_message.call_count, 2)

    @patch('src.telegram_bot.TelegramClient.iter_participants', return_value=asyncio.sleep(0))
    async def test_process_reactions(self, mock_iter_participants):
        """Test processing reactions to a message."""
        mock_client = MagicMock()
        config = {
            'advanced_settings': {
                'max_reactions_per_message': 10,
                'fetch_user_data': True
            },
            'telegram': {
                'owner_id': 123456789
            },
            'notifications': {
                'retry_attempts': 3,
                'retry_delay': 1
            }
        }

        event = MagicMock()
        event.message_id = 1234
        event.peer = PeerChannel(channel_id=12345)
        event.reactions = UpdateMessageReactions(results=[
            Reaction(count=1, reaction=ReactionEmoticon(emoticon='👍'))
        ])

        await process_reactions(event, mock_client, config)
        mock_client.send_message.assert_called()

if __name__ == '__main__':
    unittest.main()
