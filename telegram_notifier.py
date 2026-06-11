"""
Telegram Notifier Module
Handles sending notifications to Telegram users/channels
"""

import logging
import asyncio
from typing import Optional, Dict, Any
import aiohttp

logger = logging.getLogger(__name__)


class TelegramNotifier:
    """
    Sends messages and alerts to Telegram chat
    Supports both direct messages and channel/group notifications
    """
    
    BASE_URL = "https://api.telegram.org"
    
    def __init__(self, bot_token: str, chat_id: str):
        """
        Initialize Telegram notifier
        
        Args:
            bot_token: Telegram bot token from @BotFather
            chat_id: Target chat/channel/user ID
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def send_message(
        self,
        text: str,
        parse_mode: str = 'HTML',
        disable_web_page_preview: bool = True,
        retry: int = 3
    ) -> bool:
        """
        Send a message to Telegram
        
        Args:
            text: Message text (supports HTML formatting)
            parse_mode: Message formatting ('HTML', 'Markdown', 'MarkdownV2')
            disable_web_page_preview: Disable link previews
            retry: Number of retries on failure
            
        Returns:
            True if successful, False otherwise
        """
        
        url = f"{self.BASE_URL}/bot{self.bot_token}/sendMessage"
        
        payload = {
            'chat_id': self.chat_id,
            'text': text,
            'parse_mode': parse_mode,
            'disable_web_page_preview': disable_web_page_preview
        }
        
        session = await self._get_session()
        
        for attempt in range(retry):
            try:
                async with session.post(url, json=payload, timeout=10) as response:
                    
                    if response.status == 200:
                        logger.info("Telegram message sent successfully")
                        return True
                    
                    elif response.status == 429:
                        # Rate limited
                        retry_after = int(response.headers.get('Retry-After', 30))
                        logger.warning(f"Telegram rate limited. Waiting {retry_after}s...")
                        await asyncio.sleep(retry_after)
                        continue
                    
                    else:
                        error_data = await response.json()
                        logger.error(f"Telegram API error: {error_data}")
                        
                        if attempt < retry - 1:
                            await asyncio.sleep(2 ** attempt)
                            continue
                        return False
                        
            except asyncio.TimeoutError:
                logger.error(f"Timeout sending message (attempt {attempt + 1}/{retry})")
                if attempt < retry - 1:
                    await asyncio.sleep(2 ** attempt)
            
            except Exception as e:
                logger.error(f"Error sending Telegram message: {str(e)}")
                if attempt < retry - 1:
                    await asyncio.sleep(2 ** attempt)
        
        return False
    
    async def send_photo(
        self,
        photo_url: str,
        caption: str = "",
        parse_mode: str = 'HTML'
    ) -> bool:
        """
        Send a photo message to Telegram
        
        Args:
            photo_url: URL or file ID of photo
            caption: Photo caption (optional)
            parse_mode: Caption formatting
            
        Returns:
            True if successful
        """
        
        url = f"{self.BASE_URL}/bot{self.bot_token}/sendPhoto"
        
        payload = {
            'chat_id': self.chat_id,
            'photo': photo_url,
            'parse_mode': parse_mode
        }
        
        if caption:
            payload['caption'] = caption
        
        session = await self._get_session()
        
        try:
            async with session.post(url, json=payload, timeout=10) as response:
                
                if response.status == 200:
                    logger.info("Photo sent to Telegram successfully")
                    return True
                else:
                    error_data = await response.json()
                    logger.error(f"Telegram photo error: {error_data}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error sending photo: {str(e)}")
            return False
    
    async def send_alert(
        self,
        title: str,
        message: str,
        alert_type: str = 'info'
    ) -> bool:
        """
        Send a formatted alert message
        
        Args:
            title: Alert title
            message: Alert message
            alert_type: 'info', 'warning', 'success', 'error'
            
        Returns:
            True if successful
        """
        
        # Format based on alert type
        emojis = {
            'info': 'ℹ️',
            'warning': '⚠️',
            'success': '✅',
            'error': '❌',
            'hot': '🔥',
            'new': '🆕'
        }
        
        emoji = emojis.get(alert_type, 'ℹ️')
        
        formatted_message = f"{emoji} <b>{title}</b>\n\n{message}"
        
        return await self.send_message(formatted_message)
    
    async def send_pool_alert(self, pool_data: Dict[str, Any]) -> bool:
        """
        Send a formatted pool alert
        
        Args:
            pool_data: Pool information dictionary
            
        Returns:
            True if successful
        """
        
        message = self._format_pool_message(pool_data)
        return await self.send_message(message)
    
    def _format_pool_message(self, pool: Dict[str, Any]) -> str:
        """Format pool data for Telegram"""
        
        analysis = pool.get('analysis', {})
        metrics = analysis.get('metrics', {})
        
        message = f"""
🎯 <b>New Good Pool Found!</b>

📍 <b>Pool Address:</b>
<code>{pool.get('address', 'N/A')}</code>

💰 <b>Liquidity:</b> ${metrics.get('liquidity_usd', 0):,.2f}
📊 <b>24h Volume:</b> ${metrics.get('volume_24h', 0):,.2f}
🔄 <b>Fee Tier:</b> {metrics.get('fee_tier', 'N/A')}%

📈 <b>Score:</b> {analysis.get('score', 0)}/100
✅ <b>Meets Criteria:</b> {', '.join(analysis.get('criteria_met', []))}

🔗 View on Solscan: https://solscan.io/account/{pool.get('address')}
"""
        return message
    
    async def send_status_update(self, status_message: str) -> bool:
        """
        Send a bot status update
        
        Args:
            status_message: Status message
            
        Returns:
            True if successful
        """
        
        formatted = f"<b>🤖 Bot Status Update</b>\n\n{status_message}"
        return await self.send_message(formatted)
    
    async def send_test_message(self) -> bool:
        """
        Send a test message to verify bot is working
        
        Returns:
            True if successful
        """
        
        test_message = """
✅ <b>Meteora Pool Bot Started!</b>

Your bot is now monitoring Meteora pools and will send you alerts when good pools are found.

<b>Configuration:</b>
• Minimum Liquidity: $10,000
• Minimum 24h Volume: $5,000
• Minimum Score: 70/100
• Check Interval: 5 minutes

📊 Bot will notify you when eligible pools are discovered!
"""
        return await self.send_message(test_message)
    
    async def verify_chat(self) -> bool:
        """
        Verify that the chat ID is valid and bot can send messages
        
        Returns:
            True if verified, False otherwise
        """
        
        logger.info(f"Verifying Telegram chat ID: {self.chat_id}")
        
        url = f"{self.BASE_URL}/bot{self.bot_token}/getChat"
        payload = {'chat_id': self.chat_id}
        
        session = await self._get_session()
        
        try:
            async with session.post(url, json=payload, timeout=10) as response:
                
                if response.status == 200:
                    data = await response.json()
                    if data.get('ok'):
                        chat_info = data.get('result', {})
                        logger.info(f"Chat verified: {chat_info}")
                        return True
                
                logger.error("Failed to verify chat")
                return False
                
        except Exception as e:
            logger.error(f"Error verifying chat: {str(e)}")
            return False
    
    async def close(self) -> None:
        """Close the aiohttp session"""
        if self.session:
            await self.session.close()
    
    async def __aenter__(self):
        """Async context manager entry"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
