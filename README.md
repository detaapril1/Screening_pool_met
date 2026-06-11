# 🤖 Meteora Pool Screening Bot

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://www.docker.com/)
[![Status: Production Ready](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)](https://github.com/your-username/meteora-pool-bot)

> **Real-time pool screening bot for Meteora DEX on Solana with Telegram notifications**

Automatically monitor and filter high-quality liquidity pools on Meteora, score them based on safety and metrics, and get instant Telegram alerts for promising opportunities.

## ✨ Features

- 🔍 **Real-time Monitoring** - Scans Meteora pools every configurable interval
- 📊 **Smart Filtering** - Evaluates pools based on 4 criteria (liquidity, volume, age, safety)
- 💬 **Telegram Alerts** - Instant notifications for quality pools
- 💾 **Duplicate Prevention** - SQLite database prevents alert spam
- 🔄 **Async Processing** - Non-blocking, efficient pool scanning
- 🐳 **Docker Ready** - Production deployment in seconds
- 🧪 **Full Test Suite** - Connection tests and configuration validation
- 📚 **Complete Docs** - 3,000+ lines of comprehensive documentation

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip & git
- Solscan API key (free: https://solscan.io)
- Telegram bot token (@BotFather)
- Telegram channel (for alerts)

### Installation (5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/your-username/meteora-pool-bot.git
cd meteora-pool-bot

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure
cp .env.example .env
# Edit .env with your API keys

# 5. Test
python test_bot.py

# 6. Run!
python bot.py
```

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker logs -f meteora-pool-bot

# Stop
docker-compose down
```

## 📋 Configuration

Copy `.env.example` to `.env` and fill in your credentials:

```env
# Required API Keys
SOLSCAN_API_KEY=your_api_key_here
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHANNEL_ID=-100your_channel_id

# Filter Settings (adjustable)
MIN_LIQUIDITY=1000              # Minimum USD
MIN_VOLUME_24H=5000             # Minimum USD
MIN_AGE_HOURS=1                 # Minimum hours
MAX_AGE_DAYS=30                 # Maximum days
MIN_SAFETY_SCORE=70             # Out of 100

# Bot Settings
SCAN_INTERVAL=300               # Seconds (5 minutes)
ENABLE_NOTIFICATIONS=true
LOG_LEVEL=INFO
```

### Filter Presets

**Aggressive** (High Risk, High Reward)
```env
MIN_LIQUIDITY=500
MIN_VOLUME_24H=1000
MIN_AGE_HOURS=0.5
SCAN_INTERVAL=60
```

**Balanced** (Default - Recommended)
```env
MIN_LIQUIDITY=5000
MIN_VOLUME_24H=10000
MIN_AGE_HOURS=2
SCAN_INTERVAL=300
```

**Conservative** (Low Risk)
```env
MIN_LIQUIDITY=20000
MIN_VOLUME_24H=50000
MIN_AGE_HOURS=24
SCAN_INTERVAL=600
```

## 📊 How It Works

```
1. Fetch pools from Solscan API
   ↓
2. Calculate scores (liquidity, volume, age, safety)
   ↓
3. Apply filter thresholds
   ↓
4. Check database for duplicates
   ↓
5. For new quality pools:
   • Format detailed message
   • Send Telegram notification
   • Update database
   ↓
6. Wait SCAN_INTERVAL
7. Repeat
```

### Scoring System (0-100 points)

| Criteria | Points | Description |
|----------|--------|-------------|
| Liquidity | 0-25 | Pool liquidity in USD |
| Volume 24h | 0-25 | Trading volume |
| Age | 0-25 | Pool maturity |
| Safety | 0-25 | Rug pull risk assessment |

**A pool must pass ALL minimum thresholds to trigger an alert.**

## 📁 Project Structure

```
meteora-pool-bot/
├── bot.py                      # Main bot orchestrator
├── solscan_api.py             # Solscan API wrapper
├── pool_filter.py             # Filtering logic
├── telegram_notifier.py       # Telegram integration
├── test_bot.py                # Test suite
│
├── requirements.txt           # Python dependencies
├── .env.example              # Configuration template
├── Dockerfile                # Docker build
├── docker-compose.yml        # Docker Compose
├── Makefile                  # Convenience commands
│
├── QUICK_START.md            # 5-minute setup guide ⭐
├── README.md                 # Project overview
├── METEORA_POOL_BOT_SETUP.md # Complete installation
├── API_INTEGRATION.md        # API documentation
├── PROJECT_SUMMARY.md        # Architecture details
└── INDEX.md                  # File reference
```

## 🔧 Commands

```bash
# Using Makefile
make install          # Install dependencies
make setup           # Create .env file
make run             # Run bot (development)
make run-debug       # Run with debug logging
make test            # Test all connections
make docker-build    # Build Docker image
make docker-run      # Run in Docker
make docker-stop     # Stop Docker container
make logs            # Show bot logs
make backup          # Backup .env and database
make clean           # Clean logs and database
```

## 📊 Monitoring

### View Real-time Logs
```bash
# Linux/Mac
tail -f logs/bot.log

# Windows (PowerShell)
Get-Content logs/bot.log -Wait
```

### Database Queries
```bash
# Check tracked pools
sqlite3 pool_tracking.db "SELECT COUNT(*) FROM pools;"

# View best pools
sqlite3 pool_tracking.db "SELECT address, name, score FROM pools ORDER BY score DESC LIMIT 10;"
```

## 🔐 Security

✅ API keys stored in `.env` (never commit!)
✅ `.gitignore` prevents accidental key leaks
✅ Docker runs as non-root user
✅ All API calls use HTTPS
✅ Input validation on all data
✅ No sensitive data in logs

## 📚 Documentation

| Document | Purpose | Read Time |
|----------|---------|-----------|
| [QUICK_START.md](QUICK_START.md) | 5-minute setup | 5 min |
| [README.md](README.md) | Project overview | 10 min |
| [METEORA_POOL_BOT_SETUP.md](METEORA_POOL_BOT_SETUP.md) | Complete guide | 20 min |
| [API_INTEGRATION.md](API_INTEGRATION.md) | API details | 15 min |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Architecture | 15 min |

## 🧪 Testing

Run the full test suite:

```bash
python test_bot.py
```

Tests cover:
- ✅ Environment variables validation
- ✅ Solscan API connectivity
- ✅ Telegram Bot authentication
- ✅ Pool filter functionality
- ✅ Database initialization

## 📈 Performance

| Metric | Value |
|--------|-------|
| Memory Usage | ~150 MB |
| CPU Usage | Minimal (sleeping) |
| API Calls/Day | 288 (1 per 5 min) |
| Solscan Quota | 1,000,000/month ✓ |
| Telegram Cost | FREE |

## 🛠️ Technology Stack

- **Language:** Python 3.8+
- **APIs:** Solscan v2, Telegram Bot API
- **Database:** SQLite
- **Async:** asyncio
- **Containerization:** Docker
- **Package Manager:** pip

## 📦 Dependencies

```
python-telegram-bot==20.0
requests==2.31.0
python-dotenv==1.0.0
aiohttp==3.9.0
pytz==2023.3
```

See [requirements.txt](requirements.txt) for full list.

## 🚀 Deployment

### Development
```bash
python bot.py
```

### Production (Docker)
```bash
docker-compose up -d
```

### Production (Background)
```bash
# Linux/Mac with tmux
tmux new-session -d -s bot "python bot.py"

# Linux with nohup
nohup python bot.py > logs/bot.log 2>&1 &
```

### Scheduled (Cron)
```bash
# Run daily at midnight
0 0 * * * /path/to/bot.py >> /path/to/logs/bot.log 2>&1
```

## 📞 Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "API key invalid"
- Check `.env` - key is correct?
- Regenerate from provider
- Check key hasn't expired

### "Telegram bot token invalid"
- Verify token format: `123456789:ABCdefGHI...`
- Test: `curl https://api.telegram.org/bot<TOKEN>/getMe`
- Create new bot from @BotFather

### "No notifications received"
- Verify bot is admin in channel
- Check channel ID format (should have -100 prefix)
- Enable notifications: `ENABLE_NOTIFICATIONS=true`

### "Rate limited"
- Increase `SCAN_INTERVAL` (default 300s)
- Upgrade to Solscan Pro plan
- Or just wait - Solscan limits are generous

See [METEORA_POOL_BOT_SETUP.md](METEORA_POOL_BOT_SETUP.md#troubleshooting) for more solutions.

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

**This bot is a screening and monitoring tool, not financial advice.**

- DYOR (Do Your Own Research)
- Cryptocurrency is high-risk
- Past performance ≠ future results
- Only invest what you can afford to lose
- This tool has no guarantee of profitability

## 🙏 Acknowledgments

- [Solscan](https://solscan.io) - Pool data API
- [Solana](https://solana.com) - Blockchain
- [Meteora](https://meteora.ag) - DEX platform
- [Telegram](https://telegram.org) - Notification service

## 📮 Support

- 📖 Read documentation in [docs/](docs/)
- 🐛 Report bugs via [Issues](../../issues)
- 💡 Suggest features via [Discussions](../../discussions)
- 📧 Contact: detaanakbaik@gmail.com

## 🌟 Show Your Support

If this project helped you, please give it a ⭐ on GitHub!

---

**Made with ❤️ for the Solana community**

**Version:** 1.0.0 | **Status:** Production Ready | **Last Updated:** Juny 2026

[⬆ back to top](#-meteora-pool-screening-bot)
