# 🤖 Meteora Pool Screening Bot

Real-time pool screening bot untuk Meteora DEX dengan Telegram notifications.

## ⚡ Quick Start (5 Menit)

### 1. Clone & Setup
```bash
git clone <repo-url>
cd meteora-pool-bot

# Install dependencies
make install

# Setup environment
make setup
```

### 2. Get API Keys (10 Menit)

#### Solscan API Key
- Kunjungi: https://solscan.io
- Login → Account Settings → API Keys
- Create new key → Copy

#### Telegram Bot Token
- Buka: https://t.me/BotFather
- Ketik: `/newbot`
- Follow instruksi → Copy token

#### Telegram Channel ID
```bash
# 1. Create channel di Telegram
# 2. Add bot sebagai admin
# 3. Jalankan:
curl https://api.telegram.org/bot<TOKEN>/getUpdates

# 4. Cari "chat":{"id": -100XXXXX}
```

### 3. Edit .env
```bash
nano .env

# Isi dengan:
SOLSCAN_API_KEY=your_key_here
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_CHANNEL_ID=-100123456789
```

### 4. Run Bot!
```bash
make run
```

Selesai! 🎉 Bot akan mulai screening pool setiap 5 menit.

---

## 📁 Project Structure

```
meteora-pool-bot/
├── bot.py                      # Main bot file
├── solscan_api.py             # Solscan API handler
├── pool_filter.py             # Pool filtering logic
├── telegram_notifier.py       # Telegram integration
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
├── Dockerfile                # Docker configuration
├── docker-compose.yml        # Docker Compose setup
├── Makefile                  # Convenience commands
├── logs/                     # Log files directory
└── METEORA_POOL_BOT_SETUP.md # Detailed documentation
```

---

## 🚀 Running Bot

### Mode 1: Development (Simple)
```bash
make run
```

### Mode 2: Debug Mode (Detailed Logging)
```bash
make run-debug
```

### Mode 3: Docker (Production)
```bash
make docker-build
make docker-run
```

### Mode 4: Background (Linux/Mac)
```bash
# Using tmux
tmux new-session -d -s bot "make run"

# Check status
tmux attach-session -s bot

# Stop
tmux kill-session -s bot
```

---

## ⚙️ Configuration

Edit `.env` untuk customize settings:

```env
# API Keys (REQUIRED)
SOLSCAN_API_KEY=your_key
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHANNEL_ID=your_channel_id

# Filter Settings
MIN_LIQUIDITY=1000           # Min $USD
MIN_VOLUME_24H=5000          # Min $USD
MIN_AGE_HOURS=1              # Min hours
MAX_AGE_DAYS=30              # Max days
MIN_SAFETY_SCORE=70          # Safety 0-100

# Bot Settings
SCAN_INTERVAL=300            # Seconds (5 min)
ENABLE_NOTIFICATIONS=true
LOG_LEVEL=INFO               # DEBUG, INFO, WARNING, ERROR
```

### Preset Configurations

**Aggressive** (High Risk, High Reward)
```env
MIN_LIQUIDITY=500
MIN_VOLUME_24H=1000
MIN_AGE_HOURS=0.5
MIN_SAFETY_SCORE=50
SCAN_INTERVAL=60
```

**Balanced** (Recommended)
```env
MIN_LIQUIDITY=5000
MIN_VOLUME_24H=10000
MIN_AGE_HOURS=2
MIN_SAFETY_SCORE=70
SCAN_INTERVAL=300
```

**Conservative** (Low Risk)
```env
MIN_LIQUIDITY=20000
MIN_VOLUME_24H=50000
MIN_AGE_HOURS=24
MIN_SAFETY_SCORE=85
SCAN_INTERVAL=600
```

---

## 📊 How It Works

```
1. Bot mendapatkan pools dari Solscan API
2. Filter pools berdasarkan kriteria:
   - Likuiditas >= MIN_LIQUIDITY
   - Volume 24h >= MIN_VOLUME_24H
   - Umur pool >= MIN_AGE_HOURS
   - Safety score >= MIN_SAFETY_SCORE
3. Untuk pool yang lolos filter:
   - Cek jika pool sudah pernah di-report (database)
   - Jika pool baru → kirim Telegram alert
   - Track pool di database
4. Tunggu SCAN_INTERVAL kemudian repeat
```

---

## 🔗 Supported Links

Bot akan mengirim link ke:
- **Solscan**: Pool details & analytics
- **Solana Explorer**: On-chain verification
- **Meteora**: Direct pool link

---

## 🛠️ Troubleshooting

### "ModuleNotFoundError" pada import
```bash
# Reinstall dependencies
make clean
make install
```

### "Invalid API Key" from Solscan
- Check API key di .env benar
- Verify key tidak expired
- Try generate new key

### "Bot Token invalid" dari Telegram
```bash
# Test token manually
curl https://api.telegram.org/bot<TOKEN>/getMe
```

### Bot tidak kirim notifikasi
- Check TELEGRAM_CHANNEL_ID benar
- Verify bot adalah admin di channel
- Check ENABLE_NOTIFICATIONS=true

### Rate limit dari Solscan
- Free tier: 10 req/s, 1M req/month
- Increase SCAN_INTERVAL jika kena limit
- Upgrade ke Pro plan untuk unlimited

---

## 📝 Logs

Bot logs disimpan di `logs/bot.log`

### View Logs
```bash
# Real-time
tail -f logs/bot.log

# Last 50 lines
tail -50 logs/bot.log

# Full log
cat logs/bot.log

# Using Makefile
make logs
```

---

## 📞 Support

Jika ada error atau issue:

1. Check logs: `tail -f logs/bot.log`
2. Verify .env configuration
3. Test API connections: `make test`
4. Check internet connection
5. Try restart bot

---

## 📚 Resources

- **Solscan Docs**: https://solscan.io
- **Meteora Docs**: https://meteora.ag
- **Telegram Bot API**: https://core.telegram.org/bots/api
- **Solana Docs**: https://docs.solana.com

---

## 📄 License

MIT License - Feel free to use & modify

---

## 🙏 Disclaimer

**⚠️ Risk Warning:**
- Always do your own research (DYOR)
- Cryptocurrency is high-risk
- This bot is a screening tool, not financial advice
- Past performance ≠ future results
- Only invest what you can afford to lose

---

**Last Updated**: January 2024
**Version**: 1.0.0

Made with ❤️ for the Solana community
