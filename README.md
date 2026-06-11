# Meteora Pool Screening Bot 🤖

A powerful cryptocurrency bot that automatically monitors and screens Meteora DEX pools on Solana blockchain, identifies profitable opportunities, and sends real-time notifications to Telegram.

## 📋 Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Setup Guide](#setup-guide)
- [Configuration](#configuration)
- [API Keys Required](#api-keys-required)
- [Running the Bot](#running-the-bot)
- [Monitoring and Logs](#monitoring-and-logs)
- [Troubleshooting](#troubleshooting)

---

## ✨ Features

✅ **Real-Time Pool Monitoring** - Continuously scans Meteora pools every 5 minutes
✅ **Intelligent Filtering** - Multi-criteria scoring system (liquidity, volume, fees, age, safety)
✅ **Telegram Notifications** - Instant alerts for profitable pools
✅ **Rug Pull Detection** - Identifies suspicious token patterns
✅ **Safe & Secure** - API keys stored in local .env file, not committed to GitHub
✅ **Comprehensive Logging** - Detailed logs for debugging and monitoring
✅ **Async Processing** - Fast, non-blocking API calls
✅ **Rate Limit Handling** - Respects API rate limits with exponential backoff

---

## 🔄 How It Works

### Bot Workflow Diagram

```
START
  │
  ├─→ [1] Fetch Pools from Solscan
  │       (Get all Meteora pools)
  │
  ├─→ [2] Extract Metrics
  │       • Liquidity (USD)
  │       • 24h Trading Volume
  │       • Fee Tier
  │       • Pool Age
  │
  ├─→ [3] Analyze Pools
  │       • Score each pool (0-100)
  │       • Check against criteria
  │       • Identify safety issues
  │
  ├─→ [4] Filter Good Pools
  │       • Only keep pools scoring ≥70
  │       • Verify criteria met
  │       • Remove duplicates
  │
  ├─→ [5] Send Telegram Alerts
  │       • Format pool information
  │       • Send notification
  │       • Include Solscan link
  │
  ├─→ [6] Wait (5 minutes)
  │       • Resume screening
  │
  └─→ REPEAT

```

### Scoring Criteria

Each pool is scored out of 100 points based on:

| Criteria | Points | Requirement |
|----------|--------|-------------|
| **Liquidity** | 25 | ≥ $10,000 |
| **24h Volume** | 25 | ≥ $5,000 |
| **Fee Tier** | 20 | 0.01% - 1.0% |
| **Pool Age** | 15 | ≤ 30 days old |
| **Token Quality** | 10 | Verified, standard decimals |
| **Safety** | 10 | No suspicious patterns |
| **TOTAL** | **100** | ≥ 70 to pass |

---

## 🏗️ Architecture

```
Meteora Pool Bot Project Structure:

meteora_pool_bot/
├── main.py                 # Main bot orchestration
├── config.py              # Configuration management
├── pool_analyzer.py       # Pool analysis & scoring logic
├── solscan_client.py      # Solscan API integration
├── telegram_notifier.py   # Telegram notifications
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template (copy to .env)
├── .env                  # (Create this with your keys)
├── .gitignore           # Prevents .env from being committed
├── README.md            # This file
└── WORKFLOW.md          # Detailed workflow documentation

```

### Component Relationships

```
┌──────────────────────────────────────────┐
│         main.py (Orchestrator)           │
├──────────────────────────────────────────┤
│  Coordinates all components and loops    │
│  Manages screening cycles                │
└────────┬─────────────────────────────────┘
         │
    ┌────┴────────────┬──────────────┬──────────────┐
    │                 │              │              │
    ▼                 ▼              ▼              ▼
┌─────────────┐ ┌──────────────┐ ┌────────────┐ ┌──────────────┐
│   Config    │ │ Solscan      │ │   Pool     │ │   Telegram   │
│   (config)  │ │  (client)    │ │  Analyzer  │ │  (notifier)  │
├─────────────┤ ├──────────────┤ ├────────────┤ ├──────────────┤
│ • API Keys  │ │ • Fetch      │ │ • Score    │ │ • Format     │
│ • Settings  │ │   pools      │ │   pools    │ │   messages   │
│ • Criteria  │ │ • Get metrics│ │ • Filter   │ │ • Send msgs  │
└─────────────┘ └──────────────┘ └────────────┘ └──────────────┘
```

---

## 📦 Prerequisites

- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **pip** (comes with Python)
- **Git** (for cloning the repository)
- **Telegram Account** (for notifications)
- **Internet Connection** (for API access)

### System Requirements

- **RAM**: 512 MB minimum
- **Disk Space**: 200 MB
- **CPU**: Any modern processor
- **Network**: Stable internet connection

---

## 🚀 Setup Guide

### Step 1: Clone the Repository

```bash
# Clone from GitHub
git clone https://github.com/yourusername/meteora-pool-bot.git
cd meteora-pool-bot

# Or create directory manually
mkdir meteora-pool-bot
cd meteora-pool-bot
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Get Required API Keys

#### A. Solscan API Key

1. Visit https://solscan.io/
2. Click your profile icon (top right)
3. Select "Settings"
4. Go to "API Keys"
5. Click "Create API Key"
6. Copy your API key
7. Save for next step

**Cost**: Free with rate limits

#### B. Telegram Bot Token

1. Open Telegram app
2. Search for `@BotFather`
3. Send `/start` command
4. Send `/newbot` command
5. Choose a name (e.g., "Meteora Pool Bot")
6. Choose a username (e.g., "meteora_pool_bot")
7. Copy the token provided (looks like: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)
8. Save for next step

**Cost**: Free

#### C. Telegram Chat ID

1. Start a conversation with your bot:
   - In Telegram, search for your bot username (from Step B)
   - Click "Start"
2. Get your Chat ID:
   - Option 1: Send `/start` to `@userinfobot` in Telegram
   - Option 2: Send a message to your bot, then go to:
     ```
     https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
     ```
     (Replace `<YOUR_BOT_TOKEN>` with your actual token)
   - Look for `"id"` field in the JSON response
3. Copy your Chat ID (a long number)

### Step 5: Configure Environment Variables

```bash
# Copy the example .env file
cp .env.example .env

# Edit .env file with your actual keys
# Use your favorite editor:
# On Windows: notepad .env
# On macOS/Linux: nano .env
```

Edit `.env` and add:

```
SOLSCAN_API_KEY=your_solscan_key_here
TELEGRAM_BOT_TOKEN=your_telegram_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here
```

**⚠️ IMPORTANT**: Never share your .env file or commit it to GitHub!

### Step 6: Create .gitignore (if not exists)

```bash
# Create .gitignore to prevent accidentally committing API keys
echo ".env" > .gitignore
echo "*.log" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo "venv/" >> .gitignore
```

### Step 7: Test the Setup

```bash
# Test imports and configuration
python -c "from main import MeteoraPooLScreeningBot; print('✓ Setup successful!')"

# This should print: ✓ Setup successful!
```

---

## ⚙️ Configuration

### Quick Configuration

Edit `.env` to adjust these key settings:

```bash
# Screening criteria
MIN_LIQUIDITY_USD=10000           # Minimum liquidity needed
MIN_VOLUME_24H_USD=5000           # Minimum 24h trading volume
MIN_POOL_SCORE=70                 # Minimum score (0-100)
MAX_AGE_HOURS=720                 # Max pool age in hours

# Bot behavior
SCREENING_INTERVAL=300            # Check every 5 minutes
DEBUG_MODE=False                  # Detailed logging on/off

# Safety filters
EXCLUDE_RUG_PULL_TOKENS=True      # Block suspicious tokens
EXCLUDE_HONEYPOT_TOKENS=True      # Block honeypot patterns
```

### Advanced Configuration

See `.env.example` for all available options with detailed comments.

---

## 🔑 API Keys Required

### 1. Solscan API Key

**Purpose**: Fetch pool data from Solana blockchain
**Where to Get**: https://solscan.io/ (free account)
**Cost**: Free with rate limits
**Rate Limit**: ~100 requests/minute on free tier

**How to Get**:
```
1. Sign up at https://solscan.io/
2. Go to Settings → API Keys
3. Create new API key
4. Copy and paste into .env
```

### 2. Telegram Bot Token

**Purpose**: Send notifications to Telegram
**Where to Get**: @BotFather in Telegram (free)
**Cost**: Free
**Rate Limit**: ~30 messages/second

**How to Get**:
```
1. Open Telegram
2. Message @BotFather
3. Send: /newbot
4. Follow prompts to create bot
5. Copy token to .env
```

### 3. Telegram Chat ID

**Purpose**: Destination for bot notifications
**Where to Get**: Your Telegram user ID (free)
**Cost**: Free

**How to Get**:
```
Option A:
1. Message @userinfobot on Telegram
2. Copy the "id" field shown

Option B:
1. Send message to your bot
2. Visit: https://api.telegram.org/bot<TOKEN>/getUpdates
3. Find "id" in JSON response
```

---

## ▶️ Running the Bot

### Start the Bot

```bash
# Make sure virtual environment is activated
# Then run:
python main.py

# You should see:
# 2024-01-15 10:30:45 - INFO - Starting Meteora Pool Screening Bot
# 2024-01-15 10:30:46 - INFO - ==================================================
# 2024-01-15 10:30:46 - INFO - Starting pool screening cycle
```

### Stop the Bot

Press `Ctrl + C` to stop the bot gracefully.

### Run in Background (Linux/macOS)

```bash
# Using nohup
nohup python main.py > bot.log 2>&1 &

# Or using screen
screen -S meteora_bot
python main.py
# Press Ctrl+A then D to detach
```

### Run in Background (Windows)

```bash
# Using Task Scheduler or create a batch file:
# bot.bat
@echo off
cd /d %~dp0
python main.py
pause
```

---

## 📊 Monitoring and Logs

### View Logs

```bash
# View last 50 lines
tail -n 50 bot.log

# Watch logs in real-time
tail -f bot.log

# Search for specific events
grep "Good pool found" bot.log
```

### Log Levels

- **DEBUG**: Very detailed, for development
- **INFO**: Normal operation (recommended)
- **WARNING**: Something unexpected happened
- **ERROR**: Something failed
- **CRITICAL**: Bot may stop

Change in `.env`:
```
LOG_LEVEL=INFO  # Default
```

### Understanding Log Messages

```
2024-01-15 10:35:00 - INFO - ==================================================
2024-01-15 10:35:00 - INFO - Starting pool screening cycle
2024-01-15 10:35:01 - INFO - Fetching Meteora pools from Solscan...
2024-01-15 10:35:02 - INFO - Fetched 45 pools from Meteora
2024-01-15 10:35:05 - INFO - Good pool found: 8x7m8... - Score: 85
2024-01-15 10:35:05 - INFO - Notification sent for pool: 8x7m8...
2024-01-15 10:35:06 - INFO - Pool screening cycle completed
2024-01-15 10:35:06 - INFO - Waiting 300 seconds before next cycle...
```

---

## 🐛 Troubleshooting

### Error: "SOLSCAN_API_KEY not set"

**Problem**: Missing Solscan API key in .env
**Solution**:
1. Open `.env` file
2. Add: `SOLSCAN_API_KEY=your_actual_key`
3. Save file
4. Restart bot

### Error: "ConnectionError" or "Timeout"

**Problem**: Can't connect to API
**Solution**:
1. Check internet connection
2. Verify API keys are correct
3. Solscan/Telegram APIs might be down
4. Try again in a few minutes

### Error: "Invalid telegram token"

**Problem**: Wrong Telegram bot token
**Solution**:
1. Go to @BotFather in Telegram
2. Send `/mybots` → select your bot
3. Click "Edit Token"
4. Copy new token
5. Update in `.env`

### Bot sends no notifications

**Problem**: No good pools found, or notifications disabled
**Solution**:
1. Check bot.log for messages
2. Lower MIN_POOL_SCORE in `.env` (try 50-60)
3. Lower MIN_LIQUIDITY_USD
4. Verify Telegram chat ID is correct
5. Send test message: set `SEND_TEST_MESSAGE=True`

### API Rate Limits

**Problem**: "Rate limited" message in logs
**Solution**:
1. Increase `SCREENING_INTERVAL` in `.env` (e.g., from 300 to 600 seconds)
2. Get higher-tier API key from Solscan
3. Run bot during off-peak hours

### Module Import Errors

**Problem**: "No module named 'aiohttp'"
**Solution**:
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Or install specific package
pip install aiohttp==3.9.1
```

---

## 📝 Project Structure

```
meteora-pool-bot/
│
├── main.py                 # Main application entry point
│                          # - Bot orchestration
│                          # - Screening cycle coordination
│                          # - Message formatting
│
├── config.py              # Configuration management
│                          # - Loads .env variables
│                          # - Validates configuration
│                          # - Stores all settings
│
├── solscan_client.py      # Solscan API client
│                          # - Fetch pools from blockchain
│                          # - Get token information
│                          # - Retrieve pool metrics
│
├── pool_analyzer.py       # Pool analysis logic
│                          # - Score pools (0-100)
│                          # - Check criteria
│                          # - Detect rug pulls
│
├── telegram_notifier.py   # Telegram notifications
│                          # - Send formatted messages
│                          # - Handle rate limits
│                          # - Verify chat connection
│
├── requirements.txt       # Python dependencies
│
├── .env.example          # Configuration template
│
├── .env                  # Actual config (create from .env.example)
│
├── .gitignore            # Don't commit these files
│
├── bot.log              # Bot activity logs
│
└── README.md            # This file
```

---

## 🔒 Security Best Practices

1. **Never commit `.env`** - It contains your API keys
2. **Use .gitignore** - Prevents accidental commits
3. **Keep keys private** - Don't share them
4. **Rotate keys regularly** - Change them monthly
5. **Use environment variables** - Never hardcode credentials
6. **Run on private server** - Not a public machine
7. **Monitor logs** - Watch for suspicious activity

---

## 📈 Future Improvements

- [ ] Web dashboard for pool statistics
- [ ] Database storage for historical data
- [ ] Multiple DEX support (Raydium, Orca, etc.)
- [ ] Advanced analytics and trend detection
- [ ] Push notifications support
- [ ] Performance optimizations
- [ ] Multi-user support

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

---

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.

---

## 📞 Support

For issues, questions, or suggestions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review [WORKFLOW.md](WORKFLOW.md) for detailed explanations
3. Open an issue on GitHub
4. Contact the maintainers

---

## ⚠️ Disclaimer

This bot is provided as-is for educational purposes. Cryptocurrency trading involves risks. Always:

- Do your own research (DYOR)
- Invest only what you can afford to lose
- Use stop losses
- Be aware of tax implications
- Not financial advice - use at your own risk

---

**Happy pool screening! 🚀**

Last Updated: January 2024
