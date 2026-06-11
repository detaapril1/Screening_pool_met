"""
Configuration Module
Loads and manages all bot configuration from environment variables
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Configuration class that holds all bot settings
    Reads from environment variables for security
    """
    
    # ==================== API KEYS ====================
    
    @property
    def SOLSCAN_API_KEY(self) -> str:
        """
        Solscan API Key
        Get from: https://solscan.io/
        Required for fetching pool data
        """
        key = os.getenv('SOLSCAN_API_KEY', '')
        if not key:
            raise ValueError("SOLSCAN_API_KEY not set in environment variables")
        return key
    
    @property
    def TELEGRAM_BOT_TOKEN(self) -> str:
        """
        Telegram Bot Token
        Get from: https://t.me/BotFather
        Required for sending messages
        """
        token = os.getenv('TELEGRAM_BOT_TOKEN', '')
        if not token:
            raise ValueError("TELEGRAM_BOT_TOKEN not set in environment variables")
        return token
    
    @property
    def TELEGRAM_CHAT_ID(self) -> str:
        """
        Telegram Chat ID where bot sends messages
        Can be a user ID or channel ID
        """
        chat_id = os.getenv('TELEGRAM_CHAT_ID', '')
        if not chat_id:
            raise ValueError("TELEGRAM_CHAT_ID not set in environment variables")
        return chat_id
    
    # ==================== PROGRAM IDs ====================
    
    @property
    def METEORA_PROGRAM_ID(self) -> str:
        """Meteora DEX program ID on Solana blockchain"""
        return os.getenv(
            'METEORA_PROGRAM_ID',
            'Eo7WjKq67rjm34Z9o5KvymzZH3DLmycq5hash5LvZQJ'  # Official Meteora Program
        )
    
    @property
    def RAYDIUM_PROGRAM_ID(self) -> str:
        """Raydium DEX program ID (alternative pool source)"""
        return os.getenv(
            'RAYDIUM_PROGRAM_ID',
            '675kPX9MHTjS2zt1qrXjVnYYtYUZsqBoWQe8J7RETiX'  # Official Raydium Program
        )
    
    # ==================== SCREENING CRITERIA ====================
    
    @property
    def MIN_LIQUIDITY_USD(self) -> float:
        """Minimum liquidity in USD to be considered good pool"""
        return float(os.getenv('MIN_LIQUIDITY_USD', '10000'))
    
    @property
    def MIN_VOLUME_24H_USD(self) -> float:
        """Minimum 24h trading volume in USD"""
        return float(os.getenv('MIN_VOLUME_24H_USD', '5000'))
    
    @property
    def MIN_POOL_SCORE(self) -> int:
        """Minimum score (0-100) for pool to be considered good"""
        return int(os.getenv('MIN_POOL_SCORE', '70'))
    
    @property
    def MAX_AGE_HOURS(self) -> int:
        """Maximum pool age in hours to be considered new/good"""
        return int(os.getenv('MAX_AGE_HOURS', '720'))  # 30 days
    
    @property
    def MIN_FEE_TIER(self) -> float:
        """Minimum fee tier (%) - ensures adequate liquidity provider incentive"""
        return float(os.getenv('MIN_FEE_TIER', '0.01'))
    
    @property
    def MAX_FEE_TIER(self) -> float:
        """Maximum fee tier (%) - not too expensive for traders"""
        return float(os.getenv('MAX_FEE_TIER', '1.0'))
    
    # ==================== BOT BEHAVIOR ====================
    
    @property
    def SCREENING_INTERVAL(self) -> int:
        """
        Seconds between screening cycles
        Default: 300 seconds (5 minutes)
        """
        return int(os.getenv('SCREENING_INTERVAL', '300'))
    
    @property
    def SOLSCAN_BATCH_SIZE(self) -> int:
        """Number of pools to fetch per API request"""
        return int(os.getenv('SOLSCAN_BATCH_SIZE', '100'))
    
    @property
    def ENABLE_DEBUG_MODE(self) -> bool:
        """Enable debug logging and verbose output"""
        return os.getenv('DEBUG_MODE', 'False').lower() == 'true'
    
    # ==================== FILTERING OPTIONS ====================
    
    @property
    def FILTER_BY_TOKEN_TYPE(self) -> Optional[str]:
        """
        Filter pools by token type: 'spl', 'wsol', 'usdc', 'all'
        'all' = no filtering
        """
        return os.getenv('FILTER_BY_TOKEN_TYPE', 'all')
    
    @property
    def EXCLUDE_RUG_PULL_TOKENS(self) -> bool:
        """Check for known rug pull patterns"""
        return os.getenv('EXCLUDE_RUG_PULL_TOKENS', 'True').lower() == 'true'
    
    @property
    def EXCLUDE_HONEYPOT_TOKENS(self) -> bool:
        """Check for honeypot token patterns"""
        return os.getenv('EXCLUDE_HONEYPOT_TOKENS', 'True').lower() == 'true'
    
    @property
    def REQUIRE_VERIFIED_TOKENS(self) -> bool:
        """Only include pools with verified tokens"""
        return os.getenv('REQUIRE_VERIFIED_TOKENS', 'False').lower() == 'true'
    
    # ==================== NOTIFICATION SETTINGS ====================
    
    @property
    def SEND_TEST_MESSAGE(self) -> bool:
        """Send test message on startup"""
        return os.getenv('SEND_TEST_MESSAGE', 'True').lower() == 'true'
    
    @property
    def NOTIFY_ON_ALL_POOLS(self) -> bool:
        """If True: notify on every pool checked (debug mode)"""
        return os.getenv('NOTIFY_ON_ALL_POOLS', 'False').lower() == 'true'
    
    def __repr__(self) -> str:
        """String representation of configuration"""
        return (
            f"<Config: "
            f"Meteora={self.METEORA_PROGRAM_ID[:8]}... "
            f"MinLiquidity=${self.MIN_LIQUIDITY_USD:,.0f} "
            f"Interval={self.SCREENING_INTERVAL}s>"
        )


# Create singleton instance
config = Config()


def validate_config() -> bool:
    """
    Validate all required configuration is present
    Returns True if valid, raises exception otherwise
    """
    required_keys = [
        'SOLSCAN_API_KEY',
        'TELEGRAM_BOT_TOKEN',
        'TELEGRAM_CHAT_ID'
    ]
    
    try:
        for key in required_keys:
            getattr(config, key)
        return True
    except ValueError as e:
        raise ValueError(f"Configuration validation failed: {str(e)}")
