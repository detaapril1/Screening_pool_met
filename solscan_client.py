"""
Solscan Client Module
Handles all API calls to Solscan for fetching pool and token data
"""

import logging
import asyncio
from typing import List, Dict, Any, Optional
import aiohttp
from datetime import datetime

logger = logging.getLogger(__name__)


class SolscanClient:
    """
    Client for interacting with Solscan API
    Fetches pool data, token information, and transaction details
    """
    
    BASE_URL = "https://api.solscan.io/api"
    
    def __init__(self, api_key: str):
        """
        Initialize Solscan client
        
        Args:
            api_key: Solscan API key from https://solscan.io/
        """
        self.api_key = api_key
        self.session: Optional[aiohttp.ClientSession] = None
        self.rate_limit_delay = 0.1  # Seconds between requests
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def _make_request(
        self,
        endpoint: str,
        params: Dict[str, Any] = None,
        retries: int = 3
    ) -> Dict[str, Any]:
        """
        Make API request to Solscan
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            retries: Number of retries on failure
            
        Returns:
            API response data
        """
        if params is None:
            params = {}
        
        # Add API key to params
        params['token'] = self.api_key
        
        session = await self._get_session()
        
        for attempt in range(retries):
            try:
                url = f"{self.BASE_URL}/{endpoint}"
                
                async with session.get(url, params=params, timeout=10) as response:
                    
                    # Handle rate limiting
                    if response.status == 429:
                        wait_time = int(response.headers.get('Retry-After', 60))
                        logger.warning(f"Rate limited. Waiting {wait_time} seconds...")
                        await asyncio.sleep(wait_time)
                        continue
                    
                    if response.status != 200:
                        logger.warning(f"API returned status {response.status}")
                        if attempt < retries - 1:
                            await asyncio.sleep(2 ** attempt)  # Exponential backoff
                            continue
                        return {}
                    
                    data = await response.json()
                    
                    # Check for API errors in response
                    if not data.get('success', True):
                        logger.warning(f"API error: {data.get('message', 'Unknown error')}")
                        return {}
                    
                    await asyncio.sleep(self.rate_limit_delay)
                    return data
                    
            except asyncio.TimeoutError:
                logger.error(f"Request timeout on attempt {attempt + 1}/{retries}")
                if attempt < retries - 1:
                    await asyncio.sleep(2 ** attempt)
            except Exception as e:
                logger.error(f"Request error: {str(e)}")
                if attempt < retries - 1:
                    await asyncio.sleep(2 ** attempt)
        
        return {}
    
    async def get_pools_by_program(
        self,
        program_id: str,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Fetch pools created by a specific program (e.g., Meteora)
        
        Args:
            program_id: Solana program ID
            limit: Number of results to return
            offset: Starting offset for pagination
            
        Returns:
            List of pool data
        """
        try:
            logger.info(f"Fetching pools for program {program_id}...")
            
            params = {
                'action': 'searchProgramCreatedAccounts',
                'programAddress': program_id,
                'limit': limit,
                'offset': offset
            }
            
            response = await self._make_request('account/search', params)
            
            pools = response.get('data', [])
            logger.info(f"Retrieved {len(pools)} pools from program")
            
            return pools
            
        except Exception as e:
            logger.error(f"Error fetching pools by program: {str(e)}")
            return []
    
    async def get_token_info(self, token_address: str) -> Dict[str, Any]:
        """
        Fetch detailed information about a token
        
        Args:
            token_address: Token mint address
            
        Returns:
            Token data
        """
        try:
            params = {
                'action': 'getTokenInfo',
                'tokenAddress': token_address
            }
            
            response = await self._make_request('token/meta', params)
            return response
            
        except Exception as e:
            logger.error(f"Error fetching token info: {str(e)}")
            return {}
    
    async def get_pool_details(self, pool_address: str) -> Dict[str, Any]:
        """
        Fetch detailed information about a specific pool
        
        Args:
            pool_address: Pool account address
            
        Returns:
            Pool details
        """
        try:
            params = {
                'action': 'getAccountData',
                'address': pool_address
            }
            
            response = await self._make_request('account', params)
            return response
            
        except Exception as e:
            logger.error(f"Error fetching pool details: {str(e)}")
            return {}
    
    async def get_pool_volume(
        self,
        pool_address: str,
        interval: str = '24h'
    ) -> Dict[str, Any]:
        """
        Fetch trading volume for a pool
        
        Args:
            pool_address: Pool address
            interval: Time interval ('1h', '24h', '7d')
            
        Returns:
            Volume data
        """
        try:
            params = {
                'action': 'getAccountVolume',
                'address': pool_address,
                'interval': interval
            }
            
            response = await self._make_request('account/volume', params)
            return response
            
        except Exception as e:
            logger.error(f"Error fetching pool volume: {str(e)}")
            return {}
    
    async def search_pools_by_tokens(
        self,
        token_a: str,
        token_b: str
    ) -> List[Dict[str, Any]]:
        """
        Search for pools containing specific token pairs
        
        Args:
            token_a: First token address
            token_b: Second token address
            
        Returns:
            List of matching pools
        """
        try:
            params = {
                'action': 'searchPools',
                'tokenA': token_a,
                'tokenB': token_b
            }
            
            response = await self._make_request('account/search', params)
            return response.get('data', [])
            
        except Exception as e:
            logger.error(f"Error searching pools: {str(e)}")
            return []
    
    async def get_recent_transactions(
        self,
        address: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get recent transactions for an address
        Useful for checking pool activity
        
        Args:
            address: Account address
            limit: Number of transactions
            
        Returns:
            List of transaction data
        """
        try:
            params = {
                'action': 'getTransactions',
                'address': address,
                'limit': limit
            }
            
            response = await self._make_request('account/transactions', params)
            return response.get('data', [])
            
        except Exception as e:
            logger.error(f"Error fetching transactions: {str(e)}")
            return []
    
    async def get_pools_with_high_volume(
        self,
        min_volume_usd: float = 10000,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Fetch pools with high trading volume
        
        Args:
            min_volume_usd: Minimum 24h volume in USD
            limit: Number of results
            
        Returns:
            List of high-volume pools
        """
        try:
            params = {
                'action': 'getHotPools',
                'minVolume': min_volume_usd,
                'limit': limit
            }
            
            response = await self._make_request('market/pools', params)
            return response.get('data', [])
            
        except Exception as e:
            logger.error(f"Error fetching high volume pools: {str(e)}")
            return []
    
    async def get_pool_liquidity(self, pool_address: str) -> Dict[str, Any]:
        """
        Get current liquidity for a pool
        
        Args:
            pool_address: Pool address
            
        Returns:
            Liquidity data
        """
        try:
            params = {
                'action': 'getLiquidity',
                'address': pool_address
            }
            
            response = await self._make_request('account/liquidity', params)
            return response
            
        except Exception as e:
            logger.error(f"Error fetching pool liquidity: {str(e)}")
            return {}
    
    async def batch_get_pool_data(
        self,
        pool_addresses: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Fetch data for multiple pools efficiently
        
        Args:
            pool_addresses: List of pool addresses
            
        Returns:
            List of pool data
        """
        results = []
        
        for address in pool_addresses:
            try:
                data = await self.get_pool_details(address)
                if data:
                    results.append(data)
                await asyncio.sleep(0.1)  # Respect rate limits
            except Exception as e:
                logger.warning(f"Error fetching pool {address}: {str(e)}")
                continue
        
        return results
    
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
