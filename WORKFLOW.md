# Meteora Pool Screening Bot - Detailed Workflow

This document explains exactly how the bot works, step by step.

## 📊 High-Level Workflow Overview

```
┌─────────────────────────────────────────────────────────────┐
│                  BOT MAIN LOOP (Continuous)                 │
└─────────────────────────────────────────────────────────────┘
                            ↓
        ┌───────────────────────────────────────┐
        │   START SCREENING CYCLE               │
        └───────────────────────────────────────┘
                            ↓
        ┌───────────────────────────────────────┐
        │   1. FETCH POOLS FROM SOLSCAN API     │
        │      ↓ (get all Meteora pools)        │
        │      45 pools fetched                  │
        └───────────────────────────────────────┘
                            ↓
        ┌───────────────────────────────────────┐
        │   2. ANALYZE EACH POOL                │
        │      ↓ (extract metrics & score)      │
        │      • Liquidity: $50,000             │
        │      • Volume: $12,000                │
        │      • Fee: 0.25%                     │
        │      • Age: 5 days                    │
        │      • Score: 82/100                  │
        └───────────────────────────────────────┘
                            ↓
        ┌───────────────────────────────────────┐
        │   3. FILTER GOOD POOLS                │
        │      ↓ (keep only scored ≥70)         │
        │      8 good pools identified          │
        └───────────────────────────────────────┘
                            ↓
        ┌───────────────────────────────────────┐
        │   4. SEND TELEGRAM ALERTS             │
        │      ↓ (notify for each good pool)    │
        │      Message 1: ✓ Sent                │
        │      Message 2: ✓ Sent                │
        │      Message 3: ✓ Sent                │
        └───────────────────────────────────────┘
                            ↓
        ┌───────────────────────────────────────┐
        │   5. WAIT & REPEAT                    │
        │      ↓ (300 seconds = 5 minutes)      │
        │      Next cycle starts...             │
        └───────────────────────────────────────┘
```

---

## 🔍 Step-by-Step Detailed Breakdown

### Step 1: Fetch Pools from Solscan

**Purpose**: Get all active pools on Meteora DEX

**API Call**:
```
GET https://api.solscan.io/api/account/search
Parameters:
  - action: searchProgramCreatedAccounts
  - programAddress: Eo7WjKq67rjm34Z9o5KvymzZH3DLmycq5hash5LvZQJ  (Meteora Program ID)
  - limit: 100
  - offset: 0
  - token: your_solscan_api_key
```

**What Happens**:
1. Bot connects to Solscan API
2. Requests pools created by Meteora program
3. Receives up to 100 pool records
4. Each pool contains:
   - Pool address
   - Token A & Token B (trading pair)
   - Liquidity amount
   - Created timestamp
   - Fee tier

**Example Response**:
```json
{
  "success": true,
  "data": [
    {
      "address": "8x7m8Lm3KpL6jQ1vR5tU4yZ2xA3bC5dE7fG9hI0jK",
      "token_a": {
        "address": "EPjFWaLb3odcccccccccc...",
        "symbol": "USDC",
        "decimals": 6
      },
      "token_b": {
        "address": "So11111111111111111...",
        "symbol": "WSOL",
        "decimals": 9
      },
      "liquidity_usd": 45230.50,
      "created_at": "2024-01-10T15:30:00Z",
      "fee": 0.25
    },
    // ... more pools
  ]
}
```

**Code Location**: `main.py` → `fetch_meteora_pools()` and `solscan_client.py` → `get_pools_by_program()`

---

### Step 2: Extract Metrics from Each Pool

**Purpose**: Get numerical values for analysis

**For each pool, extract**:

```python
metrics = {
    'liquidity_usd': 45230.50,           # Total liquidity value
    'volume_24h': 12500.00,              # Trading volume last 24h
    'fee_tier': 0.25,                    # Fee percentage (%)
    'created_at': '2024-01-10T15:30:00Z',# When pool was created
    'age_hours': 92.5                    # Hours since creation
}
```

**Calculations**:
```python
# Age calculation
pool_created = datetime.fromisoformat(created_timestamp)
current_time = datetime.now()
age_hours = (current_time - pool_created).total_seconds() / 3600
# Result: 92.5 hours

# Liquidity: directly from API
liquidity_usd = pool['liquidity_usd']
# Result: 45230.50

# Volume: directly from API
volume_24h = pool['volume_24h']
# Result: 12500.00

# Fee: directly from API
fee_tier = pool['fee']
# Result: 0.25
```

**Code Location**: `pool_analyzer.py` → `_extract_metrics()`

---

### Step 3: Score Each Pool (0-100 Points)

**Purpose**: Quantify pool quality for decision-making

**Scoring System**:

#### Criterion 1: Liquidity Check (0-25 points)

```python
def _check_liquidity(metrics):
    liquidity = metrics['liquidity_usd']
    min_required = 10000  # From config
    
    if liquidity >= min_required * 5:      # $50,000+
        score = 25                         # Excellent
    elif liquidity >= min_required * 2:    # $20,000+
        score = 20                         # Good
    else:
        score = 0                          # Poor
    
    passed = liquidity >= min_required
    return {'passed': passed, 'score': score}

# Example: liquidity = $45,230
# Result: score = 25 (excellent), passed = True
```

#### Criterion 2: Volume Check (0-25 points)

```python
def _check_volume(metrics):
    volume = metrics['volume_24h']
    min_required = 5000  # From config
    
    if volume >= min_required * 5:         # $25,000+
        score = 25                         # Active
    elif volume >= min_required * 2:       # $10,000+
        score = 20                         # Decent
    else:
        score = 0                          # Inactive
    
    passed = volume >= min_required
    return {'passed': passed, 'score': score}

# Example: volume = $12,500
# Result: score = 25 (active), passed = True
```

#### Criterion 3: Fee Tier Check (0-20 points)

```python
def _check_fee_tier(metrics):
    fee = metrics['fee_tier']
    
    # Must be between 0.01% and 1.0%
    if 0.01 <= fee <= 1.0:
        score = 20
        passed = True
    else:
        score = 0
        passed = False
    
    return {'passed': passed, 'score': score}

# Example: fee = 0.25%
# Result: score = 20, passed = True
```

#### Criterion 4: Pool Age Check (0-15 points)

```python
def _check_age(metrics):
    age = metrics['age_hours']
    max_age = 720  # 30 days from config
    
    if age <= 24:                          # Less than 1 day old
        score = 15                         # Very new (hot)
    elif age <= 168:                       # Less than 1 week old
        score = 15                         # Recent
    else:
        score = 10 if age <= max_age else 0  # Established or too old
    
    passed = age <= max_age
    return {'passed': passed, 'score': score}

# Example: age = 92.5 hours (~4 days)
# Result: score = 15 (recent), passed = True
```

#### Criterion 5: Token Quality Check (0-10 points)

```python
def _check_token_quality(pool):
    score = 0
    
    # Check if verified
    if pool.get('verified'):
        score += 5
    
    # Check if standard token properties exist
    if pool.get('token_a', {}).get('decimals') and \
       pool.get('token_b', {}).get('decimals'):
        score += 5
    
    # Bonus for WSOL (wrapped SOL)
    if 'WSOL' in [pool['token_a']['symbol'], pool['token_b']['symbol']]:
        score += 2
    
    passed = score >= 5
    return {'passed': passed, 'score': min(score, 10)}

# Example: USDC-WSOL pair, both verified
# Result: score = 10, passed = True
```

#### Criterion 6: Safety Check (0-10 points)

```python
def _check_safety(pool):
    score = 0
    
    # Check for red flags in name/symbol
    red_flags = ['moon', 'pump', 'rug', 'scam', 'fake']
    name_symbol = f"{pool['name']} {pool['symbol']}".lower()
    
    has_red_flag = any(flag in name_symbol for flag in red_flags)
    
    if not has_red_flag:
        score = 10
        passed = True
    else:
        score = 0
        passed = False
    
    return {'passed': passed, 'score': score}

# Example: "USDC-WSOL" pool (no red flags)
# Result: score = 10, passed = True
```

#### Total Score Calculation

```python
# Sum all criteria points
total_score = (
    liquidity_score +      # 25
    volume_score +         # 25
    fee_score +            # 20
    age_score +            # 15
    token_quality_score +  # 10
    safety_score           # 10
)
# Total: 25 + 25 + 20 + 15 + 10 + 10 = 105 max possible

# But cap at 100
final_score = min(total_score, 100)

# Example calculation:
# 25 + 25 + 20 + 15 + 10 + 10 = 105 → 100/100 (but actually 85/100)
# More realistic example:
# 25 + 20 + 20 + 15 + 8 + 10 = 98 → actual score 85/100
```

**Code Location**: `pool_analyzer.py` → `analyze_pool()` and individual check methods

---

### Step 4: Filter Good Pools

**Purpose**: Keep only pools that meet minimum criteria

**Filtering Logic**:

```python
good_pools = []

for pool in all_pools:
    analysis = analyzer.analyze_pool(pool)
    
    # Check if pool is good
    is_good = (
        # Must score 70 or higher
        analysis['score'] >= 70 and
        # Can fail at most 1 criterion
        len(analysis['criteria_failed']) <= 1
    )
    
    if is_good:
        good_pools.append(pool)
        # Track to avoid duplicates
        processed_pools.add(pool['address'])

# Result: good_pools now contains only profitable opportunities
```

**Example**:

```
INPUT: 45 pools from Solscan

Pool Analysis Results:
├─ Pool A: Score 85/100 ✓ GOOD (all criteria met)
├─ Pool B: Score 92/100 ✓ GOOD (all criteria met)
├─ Pool C: Score 68/100 ✗ BAD (score too low)
├─ Pool D: Score 72/100 ✓ GOOD (1 criterion failed, score OK)
├─ Pool E: Score 45/100 ✗ BAD (score too low)
└─ ... (40 more pools, mostly bad)

OUTPUT: 8 good pools identified for notification
```

**Code Location**: `main.py` → `analyze_and_filter_pools()`

---

### Step 5: Send Telegram Alerts

**Purpose**: Notify about good pools in real-time

**For each good pool**, format a message:

```python
message = f"""
🎯 <b>New Good Pool Found!</b>

📍 <b>Pool Address:</b>
<code>8x7m8Lm3KpL6jQ1vR5tU4yZ2xA3bC5dE7fG9hI0jK</code>

💰 <b>Liquidity:</b> $45,230.50
📊 <b>24h Volume:</b> $12,500.00
🔄 <b>Fee Tier:</b> 0.25%

📈 <b>Score:</b> 85/100
✅ <b>Meets Criteria:</b> liquidity, volume, fee_tier, age, token_quality, safety

⏰ <b>Detected:</b> 2024-01-15 14:35:00

🔗 View on Solscan: https://solscan.io/account/8x7m8Lm3KpL6...
"""

# Send via Telegram Bot API
response = await telegram_bot.send_message(message)

# Telegram delivers notification to your phone within 1-2 seconds
```

**Telegram API Call**:
```
POST https://api.telegram.org/bot<YOUR_BOT_TOKEN>/sendMessage

JSON Body:
{
  "chat_id": "123456789",
  "text": "🎯 New Good Pool Found!...",
  "parse_mode": "HTML",
  "disable_web_page_preview": true
}

Response:
{
  "ok": true,
  "result": {
    "message_id": 12345,
    "date": 1705330500,
    "text": "..."
  }
}
```

**Code Location**: `main.py` → `send_notifications()` and `telegram_notifier.py` → `send_message()`

---

### Step 6: Wait and Repeat

**Purpose**: Continuous monitoring without overload

```python
while True:
    # Do screening cycle
    await run_screening_cycle()
    
    # Wait before next cycle
    wait_time = 300  # 5 minutes from config
    logger.info(f"Waiting {wait_time} seconds...")
    
    await asyncio.sleep(wait_time)
    
    # Loop continues...
```

**Timeline Example**:
```
10:00:00 - Cycle 1 starts, 45 pools checked, 8 notified
10:00:10 - Cycle 1 completes
10:00:10 - Bot waits 300 seconds...
10:05:10 - Cycle 2 starts, 48 pools checked, 3 notified
10:05:20 - Cycle 2 completes
10:05:20 - Bot waits 300 seconds...
10:10:20 - Cycle 3 starts...
```

**Code Location**: `main.py` → `run_continuous()`

---

## 🔄 Data Flow Diagram

```
Solscan API
    │
    │ Fetch pools
    │ (JSON data)
    ▼
┌─────────────────────┐
│  solscan_client.py  │
│  get_pools_by_      │
│  program()          │
└────────────┬────────┘
             │
             │ List of pool dicts
             ▼
        ┌─────────────────────┐
        │ main.py             │
        │ fetch_meteora_      │
        │ pools()             │
        └────────────┬────────┘
                     │
                     │ 45 pools
                     ▼
            ┌────────────────────┐
            │ main.py            │
            │ analyze_and_       │
            │ filter_pools()     │
            └────────┬───────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┌─────────────────┐      ┌──────────────┐
│ pool_analyzer   │      │ pool_analyzer│
│ .analyze_pool() │      │ .analyze()   │
└────────┬────────┘      └──────┬───────┘
         │                      │
         │ Score 0-100         │ Score 0-100
         ▼                      ▼
    (for each pool)         (total result)
    
         └──────────┬──────────┘
                    │
                    │ 8 good pools
                    │ (score >= 70)
                    ▼
           ┌────────────────────┐
           │ main.py            │
           │ send_notifications()
           └────────┬───────────┘
                    │
                    │ Format messages
                    ▼
          ┌──────────────────────┐
          │ telegram_notifier.py │
          │ send_message()       │
          └────────┬─────────────┘
                   │
                   │ HTTP POST
                   ▼
            Telegram Bot API
                   │
                   │ Deliver
                   ▼
              Your Telegram
              (instant alert)
```

---

## 📊 Example: Complete Pool Analysis

Let's trace a single pool through the entire analysis:

### Pool Input Data:
```json
{
  "address": "8x7m8Lm3KpL6jQ1vR5tU4yZ2xA3bC5dE7fG9hI0jK",
  "name": "USDC-WSOL",
  "token_a": {
    "symbol": "USDC",
    "address": "EPjFWaLb3odcccccccc...",
    "decimals": 6,
    "verified": true
  },
  "token_b": {
    "symbol": "WSOL",
    "address": "So11111111111111111...",
    "decimals": 9,
    "verified": true
  },
  "liquidity_usd": 45230.50,
  "volume_24h": 12500.00,
  "fee": 0.25,
  "created_at": "2024-01-10T15:30:00Z"
}
```

### Step-by-Step Analysis:

```
1. EXTRACT METRICS
   ├─ liquidity_usd: 45230.50
   ├─ volume_24h: 12500.00
   ├─ fee_tier: 0.25
   ├─ created_at: 2024-01-10T15:30:00Z
   └─ age_hours: 92.5 (4 days old)

2. CHECK LIQUIDITY
   ├─ Value: $45,230.50
   ├─ Min Required: $10,000
   ├─ Assessment: $45,230.50 >= $50,000*1 (excellent)
   ├─ Points: 25 ✓
   └─ Passed: YES

3. CHECK VOLUME
   ├─ Value: $12,500.00
   ├─ Min Required: $5,000
   ├─ Assessment: $12,500 >= $10,000*1 (good)
   ├─ Points: 20 ✓
   └─ Passed: YES

4. CHECK FEE TIER
   ├─ Value: 0.25%
   ├─ Range: 0.01% - 1.0%
   ├─ Assessment: Within acceptable range
   ├─ Points: 20 ✓
   └─ Passed: YES

5. CHECK AGE
   ├─ Value: 92.5 hours
   ├─ Max: 720 hours (30 days)
   ├─ Assessment: 92.5 <= 168 hours (recent, 4 days)
   ├─ Points: 15 ✓
   └─ Passed: YES

6. CHECK TOKEN QUALITY
   ├─ Verified: YES (USDC + WSOL)
   ├─ Has Decimals: YES
   ├─ Contains WSOL: YES
   ├─ Points: 10 ✓
   └─ Passed: YES

7. CHECK SAFETY
   ├─ Name: "USDC-WSOL"
   ├─ Red Flags: None found
   ├─ Assessment: Safe
   ├─ Points: 10 ✓
   └─ Passed: YES

3. CALCULATE TOTAL SCORE
   ├─ Liquidity:     25
   ├─ Volume:        20
   ├─ Fee Tier:      20
   ├─ Age:           15
   ├─ Token Quality: 10
   ├─ Safety:        10
   ├─ ─────────────────
   └─ Total: 100/100 ✓✓✓

4. DECISION
   ├─ Score: 100/100 >= 70 ✓
   ├─ Failed Criteria: 0 (max allowed: 1) ✓
   ├─ Is Good Pool: YES ✓✓✓
   └─ Action: NOTIFY VIA TELEGRAM
```

### Telegram Notification Sent:
```
🎯 New Good Pool Found!

📍 Pool Address:
8x7m8Lm3KpL6jQ1vR5tU4yZ2xA3bC5dE7fG9hI0jK

💰 Liquidity: $45,230.50
📊 24h Volume: $12,500.00
🔄 Fee Tier: 0.25%

📈 Score: 100/100
✅ Meets Criteria: liquidity, volume, fee_tier, age, token_quality, safety

⏰ Detected: 2024-01-15 14:35:00

🔗 View on Solscan: https://solscan.io/account/8x7m8Lm3KpL6...
```

---

## 🔐 API Integration Details

### Solscan API

**Endpoint**: `https://api.solscan.io/api`

**Authentication**: Query parameter `token=YOUR_API_KEY`

**Rate Limits**:
- Free Tier: ~100 requests/minute
- Premium: Higher limits

**Key Endpoints Used**:
1. `account/search` - Find pools by program
2. `token/meta` - Get token information
3. `account` - Get account details
4. `account/volume` - Get trading volume

### Telegram Bot API

**Endpoint**: `https://api.telegram.org/bot<BOT_TOKEN>/sendMessage`

**Authentication**: Bot token in URL path

**Rate Limits**:
- ~30 messages/second per bot
- Respect 429 responses (rate limit exceeded)

**Parameters**:
```json
{
  "chat_id": "recipient_id",
  "text": "message",
  "parse_mode": "HTML" | "Markdown",
  "disable_web_page_preview": true
}
```

---

## ⚠️ Error Handling

### Retry Logic

```python
# Exponential backoff
for attempt in range(3):
    try:
        response = await api_call()
        return response
    except TimeoutError:
        wait = 2 ** attempt  # 1s, 2s, 4s
        await asyncio.sleep(wait)
    except RateLimitError:
        wait = response.headers['Retry-After']
        await asyncio.sleep(wait)
```

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| 429 Too Many Requests | Rate limit exceeded | Wait and retry |
| 401 Unauthorized | Invalid API key | Check .env file |
| 403 Forbidden | API key lacks permission | Upgrade/recreate key |
| 500 Server Error | API down temporarily | Retry later |
| ConnectionError | No internet | Check connection |

---

## 📈 Performance Metrics

### Typical Cycle Times

```
Fetch Pools:        1-2 seconds
Analyze 45 Pools:   2-3 seconds
Send 8 Alerts:      8-10 seconds
─────────────────────────────
Total per Cycle:    11-15 seconds

Cycle Interval:     300 seconds (5 minutes)
API Calls per Cycle: ~50-60
Daily API Calls:    ~15,000
```

### Resource Usage

```
Memory: ~50-100 MB (Python + libraries)
CPU:    < 1% while waiting, 10-20% during cycle
Disk:   ~200 MB (code + dependencies)
Network: ~1-2 MB per cycle
```

---

## 🎯 Configuration Impact

### Change: `MIN_LIQUIDITY_USD = 5000` (from 10000)

```
Effect:
├─ More pools pass liquidity check
├─ Score increases for more pools
├─ More "good" pools identified
├─ More Telegram notifications sent
└─ Risk: Includes lower-liquidity pools

Example:
  Before: 8 good pools
  After:  15 good pools (+87%)
```

### Change: `SCREENING_INTERVAL = 60` (from 300)

```
Effect:
├─ Check pools 5x more frequently
├─ Faster discovery of new pools
├─ API usage increased 5x
├─ May hit rate limits faster
└─ Risk: More API costs, possible bans

Calculation:
  Before: ~50 API calls/cycle * 12 cycles/hour = 600/hour
  After:  ~50 API calls/cycle * 60 cycles/hour = 3000/hour
```

---

## 🔗 Complete Request/Response Examples

### Request 1: Fetch Pools

```
GET https://api.solscan.io/api/account/search?
  action=searchProgramCreatedAccounts
  &programAddress=Eo7WjKq67rjm34Z9o5KvymzZH3DLmycq5hash5LvZQJ
  &limit=100
  &offset=0
  &token=abc123xyz

Response (simplified):
{
  "success": true,
  "data": [
    {
      "address": "8x7m8...",
      "liquidity_usd": 45230.50,
      "volume_24h": 12500.00,
      "fee": 0.25,
      "created_at": "2024-01-10T15:30:00Z",
      ...
    },
    ...
  ]
}
```

### Request 2: Send Telegram Message

```
POST https://api.telegram.org/bot987654321:ABCDefGHijKLmnoPQRstUVwxyz/sendMessage

{
  "chat_id": "123456789",
  "text": "🎯 <b>New Good Pool Found!</b>...",
  "parse_mode": "HTML",
  "disable_web_page_preview": true
}

Response:
{
  "ok": true,
  "result": {
    "message_id": 12345,
    "date": 1705330500,
    "chat": {"id": 123456789},
    "text": "..."
  }
}
```

---

This completes the detailed workflow explanation. The bot operates in this continuous cycle, providing real-time alerts for profitable Meteora pools.
