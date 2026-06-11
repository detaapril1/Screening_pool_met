"""
Meteora Pool Screening Bot
Main application file that orchestrates pool screening and notifications
"""

import asyncio
import logging
from datetime import datetime
from typing import List, Dict, Any

from solscan_client import SolscanClient
from pool_analyzer import PoolAnalyzer
from telegram_notifier import TelegramNotifier
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class MeteoraPooLScreeningBot:
    """
    Main bot class that coordinates pool screening from Meteora/Solscan
    and sends notifications via Telegram
    """
    
    def __init__(self):
        """Initialize bot with configuration and clients"""
        self.config = Config()
        self.solscan_client = SolscanClient(self.config.SOLSCAN_API_KEY)
        self.pool_analyzer = PoolAnalyzer(self.config)
        self.telegram_notifier = TelegramNotifier(
            self.config.TELEGRAM_BOT_TOKEN,
            self.config.TELEGRAM_CHAT_ID
        )
        self.processed_pools = set()  # Track processed pools to avoid duplicates
        
    async def fetch_meteora_pools(self) -> List[Dict[str, Any]]:
        """
        Fetch active pools from Meteora via Solscan
        
        Returns:
            List of pool data dictionaries
        """
        try:
            logger.info("Fetching Meteora pools from Solscan...")
            
            # Get pools created on Meteora program ID
            pools = await self.solscan_client.get_pools_by_program(
                program_id=self.config.METEORA_PROGRAM_ID
            )
            
            logger.info(f"Fetched {len(pools)} pools from Meteora")
            return pools
            
        except Exception as e:
            logger.error(f"Error fetching Meteora pools: {str(e)}")
            return []
    
    async def analyze_and_filter_pools(self, pools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze pools and filter for good opportunities
        
        Args:
            pools: List of pool data
            
        Returns:
            List of pools that meet screening criteria
        """
        good_pools = []
        
        for pool in pools:
            try:
                # Skip already processed pools
                if pool.get('address') in self.processed_pools:
                    continue
                
                # Perform detailed analysis
                analysis = self.pool_analyzer.analyze_pool(pool)
                
                # Check if pool meets criteria
                if analysis.get('is_good_pool', False):
                    pool['analysis'] = analysis
                    good_pools.append(pool)
                    self.processed_pools.add(pool.get('address'))
                    
                    logger.info(f"Good pool found: {pool.get('address')} - "
                              f"Score: {analysis.get('score')}")
            
            except Exception as e:
                logger.warning(f"Error analyzing pool: {str(e)}")
                continue
        
        return good_pools
    
    async def send_notifications(self, pools: List[Dict[str, Any]]) -> None:
        """
        Send pool information via Telegram
        
        Args:
            pools: List of good pools to notify about
        """
        for pool in pools:
            try:
                # Format message
                message = self._format_pool_message(pool)
                
                # Send via Telegram
                await self.telegram_notifier.send_message(message)
                
                logger.info(f"Notification sent for pool: {pool.get('address')}")
                
                # Add delay between messages to avoid rate limits
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"Error sending notification: {str(e)}")
                continue
    
    def _format_pool_message(self, pool: Dict[str, Any]) -> str:
        """
        Format pool data into readable Telegram message
        
        Args:
            pool: Pool data dictionary
            
        Returns:
            Formatted message string
        """
        analysis = pool.get('analysis', {})
        
        message = f"""
🎯 <b>New Good Pool Found!</b>

📍 <b>Pool Address:</b>
<code>{pool.get('address', 'N/A')}</code>

💰 <b>Liquidity:</b> ${analysis.get('liquidity_usd', 0):,.2f}
📊 <b>24h Volume:</b> ${analysis.get('volume_24h', 0):,.2f}
🔄 <b>Fee Tier:</b> {analysis.get('fee_tier', 'N/A')}%

📈 <b>Score:</b> {analysis.get('score', 0)}/100
✅ <b>Meets Criteria:</b> {', '.join(analysis.get('criteria_met', []))}

⏰ <b>Detected:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🔗 View on Solscan: https://solscan.io/account/{pool.get('address')}
"""
        return message
    
    async def run_screening_cycle(self) -> None:
        """Execute one complete screening cycle"""
        try:
            logger.info("=" * 50)
            logger.info("Starting pool screening cycle")
            logger.info("=" * 50)
            
            # Fetch pools
            pools = await self.fetch_meteora_pools()
            if not pools:
                logger.warning("No pools fetched. Skipping cycle.")
                return
            
            # Analyze and filter
            good_pools = await self.analyze_and_filter_pools(pools)
            logger.info(f"Found {len(good_pools)} good pools this cycle")
            
            # Send notifications
            if good_pools:
                await self.send_notifications(good_pools)
            else:
                logger.info("No good pools found this cycle")
            
            logger.info("Pool screening cycle completed")
            
        except Exception as e:
            logger.error(f"Error in screening cycle: {str(e)}")
    
    async def run_continuous(self) -> None:
        """
        Run bot continuously with intervals
        """
        logger.info("Starting Meteora Pool Screening Bot")
        
        try:
            while True:
                await self.run_screening_cycle()
                
                # Wait before next cycle
                logger.info(f"Waiting {self.config.SCREENING_INTERVAL} seconds "
                          "before next cycle...")
                await asyncio.sleep(self.config.SCREENING_INTERVAL)
                
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        except Exception as e:
            logger.error(f"Unexpected error in continuous run: {str(e)}")
            raise


async def main():
    """Main entry point"""
    bot = MeteoraPooLScreeningBot()
    await bot.run_continuous()


if __name__ == "__main__":
    asyncio.run(main())
