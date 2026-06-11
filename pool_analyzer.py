"""
Pool Analyzer Module
Contains logic for analyzing and scoring pools based on multiple criteria
"""

import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
import hashlib

logger = logging.getLogger(__name__)


class PoolAnalyzer:
    """
    Analyzes pools and scores them based on defined criteria.
    Determines if a pool is worth notifying about.
    """
    
    def __init__(self, config):
        """
        Initialize analyzer with configuration
        
        Args:
            config: Config object containing screening criteria
        """
        self.config = config
    
    def analyze_pool(self, pool: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive analysis of a pool
        
        Args:
            pool: Pool data dictionary from Solscan
            
        Returns:
            Analysis result with score and criteria met
        """
        analysis = {
            'address': pool.get('address'),
            'score': 0,
            'is_good_pool': False,
            'criteria_met': [],
            'criteria_failed': [],
            'metrics': {}
        }
        
        try:
            # Extract metrics
            metrics = self._extract_metrics(pool)
            analysis['metrics'] = metrics
            
            # Check each criterion
            criteria_checks = [
                ('liquidity', self._check_liquidity, metrics),
                ('volume', self._check_volume, metrics),
                ('fee_tier', self._check_fee_tier, metrics),
                ('age', self._check_age, metrics),
                ('token_quality', self._check_token_quality, pool),
                ('safety', self._check_safety, pool),
            ]
            
            score = 0
            for criterion_name, check_func, check_data in criteria_checks:
                result = check_func(check_data)
                
                if result['passed']:
                    analysis['criteria_met'].append(criterion_name)
                    score += result['score']
                else:
                    analysis['criteria_failed'].append(criterion_name)
            
            analysis['score'] = score
            analysis['liquidity_usd'] = metrics.get('liquidity_usd', 0)
            analysis['volume_24h'] = metrics.get('volume_24h', 0)
            analysis['fee_tier'] = metrics.get('fee_tier', 0)
            
            # Determine if pool is good
            analysis['is_good_pool'] = (
                score >= self.config.MIN_POOL_SCORE and
                len(analysis['criteria_failed']) <= 1  # Allow max 1 failed criterion
            )
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing pool {pool.get('address')}: {str(e)}")
            analysis['error'] = str(e)
            analysis['is_good_pool'] = False
            return analysis
    
    def _extract_metrics(self, pool: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract trading and liquidity metrics from pool data
        
        Args:
            pool: Raw pool data
            
        Returns:
            Dictionary of extracted metrics
        """
        try:
            # Try multiple field names as different APIs use different naming
            liquidity_usd = (
                pool.get('liquidity_usd') or
                pool.get('tvl') or
                pool.get('total_liquidity') or
                0
            )
            
            volume_24h = (
                pool.get('volume_24h') or
                pool.get('volume24h') or
                pool.get('trading_volume') or
                0
            )
            
            fee_tier = float(pool.get('fee', pool.get('fee_tier', 0)) or 0)
            
            # Parse timestamp
            created_at = pool.get('created_at', pool.get('timestamp', 0))
            if isinstance(created_at, str):
                try:
                    pool_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                except:
                    pool_date = datetime.now()
            else:
                pool_date = datetime.fromtimestamp(int(created_at) / 1000)
            
            pool_age_hours = (datetime.now() - pool_date).total_seconds() / 3600
            
            return {
                'liquidity_usd': float(liquidity_usd),
                'volume_24h': float(volume_24h),
                'fee_tier': fee_tier,
                'created_at': pool_date.isoformat(),
                'age_hours': pool_age_hours
            }
        except Exception as e:
            logger.warning(f"Error extracting metrics: {str(e)}")
            return {
                'liquidity_usd': 0,
                'volume_24h': 0,
                'fee_tier': 0,
                'created_at': datetime.now().isoformat(),
                'age_hours': 0
            }
    
    def _check_liquidity(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if liquidity meets minimum threshold
        Scoring: 25 points
        """
        liquidity = metrics.get('liquidity_usd', 0)
        min_required = self.config.MIN_LIQUIDITY_USD
        
        passed = liquidity >= min_required
        
        # Score based on liquidity level
        if liquidity >= min_required * 5:  # Excellent liquidity
            score = 25
        elif liquidity >= min_required * 2:  # Good liquidity
            score = 20
        else:
            score = 0
        
        return {
            'passed': passed,
            'score': score,
            'actual': liquidity,
            'required': min_required,
            'metric': f"${liquidity:,.0f} / ${min_required:,.0f}"
        }
    
    def _check_volume(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if 24h volume meets minimum threshold
        Indicates active trading
        Scoring: 25 points
        """
        volume = metrics.get('volume_24h', 0)
        min_required = self.config.MIN_VOLUME_24H_USD
        
        passed = volume >= min_required
        
        # Score based on volume level
        if volume >= min_required * 5:
            score = 25
        elif volume >= min_required * 2:
            score = 20
        else:
            score = 0
        
        return {
            'passed': passed,
            'score': score,
            'actual': volume,
            'required': min_required,
            'metric': f"${volume:,.0f} / ${min_required:,.0f}"
        }
    
    def _check_fee_tier(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if fee tier is within acceptable range
        Too low = poor LP incentive, Too high = bad for traders
        Scoring: 20 points
        """
        fee = metrics.get('fee_tier', 0)
        
        passed = (
            fee >= self.config.MIN_FEE_TIER and
            fee <= self.config.MAX_FEE_TIER
        )
        
        score = 20 if passed else 0
        
        return {
            'passed': passed,
            'score': score,
            'actual': fee,
            'min': self.config.MIN_FEE_TIER,
            'max': self.config.MAX_FEE_TIER,
            'metric': f"{fee}% (Range: {self.config.MIN_FEE_TIER}%-{self.config.MAX_FEE_TIER}%)"
        }
    
    def _check_age(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check pool age
        Newer pools = better opportunity, but not too new = stability
        Scoring: 15 points
        """
        age = metrics.get('age_hours', float('inf'))
        max_age = self.config.MAX_AGE_HOURS
        
        passed = age <= max_age
        
        # Recently created pools have higher potential
        if age <= 24:  # Less than 1 day
            score = 15
        elif age <= 168:  # Less than 1 week
            score = 15
        else:
            score = 10 if passed else 0
        
        return {
            'passed': passed,
            'score': score,
            'actual': age,
            'max': max_age,
            'metric': f"{int(age)} hours / {max_age} hours max"
        }
    
    def _check_token_quality(self, pool: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check token quality indicators
        Scoring: 10 points
        """
        score = 0
        issues = []
        
        try:
            # Check for verified status
            if pool.get('verified'):
                score += 5
            
            # Check for standard token properties
            token_a = pool.get('token_a', {})
            token_b = pool.get('token_b', {})
            
            if token_a.get('decimals') and token_b.get('decimals'):
                score += 5
            
            # Check if one token is WSOL (wrapped SOL - good stability)
            token_a_symbol = str(token_a.get('symbol', '')).upper()
            token_b_symbol = str(token_b.get('symbol', '')).upper()
            
            if 'WSOL' in [token_a_symbol, token_b_symbol]:
                score = min(score + 2, 10)
            
            passed = score >= 5
            
        except Exception as e:
            logger.warning(f"Error checking token quality: {str(e)}")
            passed = False
            score = 0
        
        return {
            'passed': passed,
            'score': score,
            'metric': f"Quality: {score}/10"
        }
    
    def _check_safety(self, pool: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check for potential rug pulls, honeypots, or scams
        Scoring: 10 points (either safe or not)
        """
        score = 0
        issues = []
        
        try:
            # Check for known problematic patterns
            name = str(pool.get('name', '')).lower()
            symbol = str(pool.get('symbol', '')).lower()
            
            # Red flags
            red_flags = [
                'moon', 'pump', 'rug', 'scam', 'fake',
                'test', 'copy', 'clone'
            ]
            
            combined_text = f"{name} {symbol}".lower()
            
            has_red_flag = any(flag in combined_text for flag in red_flags)
            
            if not has_red_flag:
                score = 10
                passed = True
            else:
                passed = False
                issues.append("Token name contains suspicious keywords")
            
            # Check supply (if available)
            supply = pool.get('token_supply', 0)
            if supply and supply > 1e18:  # Very high supply can be risky
                if not has_red_flag:
                    score -= 2  # Slight penalty but not disqualifying
            
        except Exception as e:
            logger.warning(f"Error checking safety: {str(e)}")
            passed = True
            score = 5
        
        return {
            'passed': passed,
            'score': max(score, 0),
            'issues': issues,
            'metric': f"Safety: {'✓' if passed else '✗'}"
        }
    
    def get_score_breakdown(self, pool: Dict[str, Any]) -> str:
        """
        Get human-readable breakdown of pool score
        
        Args:
            pool: Pool data
            
        Returns:
            Formatted score explanation
        """
        analysis = self.analyze_pool(pool)
        
        breakdown = f"Pool Score: {analysis['score']}/100\n"
        breakdown += f"Status: {'GOOD' if analysis['is_good_pool'] else 'REJECTED'}\n\n"
        
        breakdown += "✓ Criteria Met:\n"
        for criterion in analysis['criteria_met']:
            breakdown += f"  • {criterion}\n"
        
        if analysis['criteria_failed']:
            breakdown += "\n✗ Criteria Failed:\n"
            for criterion in analysis['criteria_failed']:
                breakdown += f"  • {criterion}\n"
        
        return breakdown
