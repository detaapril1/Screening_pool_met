# ⚡ Quick Start Guide (5 Minutes)

Fast-track to running the bot. Read the full README for details.

---

## 🎯 3 Simple Steps

### Step 1: Get Your API Keys (3 minutes)

**Solscan API Key**
1. Visit https://solscan.io/ → Sign up
2. Settings → API Keys → Create API Key
3. Copy the key

**Telegram Bot Token**
1. Open Telegram → Search "@BotFather"
2. Send `/newbot`
3. Name bot: "Meteora Pool Bot"
4. Username: "meteora_pool_bot_yourname"
5. Copy the token

**Telegram Chat ID**
1. Send `/start` to @userinfobot in Telegram
2. Copy your ID number

See [API_KEYS_GUIDE.md](API_KEYS_GUIDE.md) for detailed instructions.

---

### Step 2: Install Bot (1 minute)

```bash
# Clone repository
git clone https://github.com/yourusername/meteora-pool-bot.git
cd meteora-pool-bot

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

### Step 3: Configure & Run (1 minute)

```bash
# Copy example config
cp .env.example .env

# Edit .env with your API keys
nano .env  # Or use your favorite editor

# Add these values:
# SOLSCAN_API_KEY=your_key_here
# TELEGRAM_BOT_TOKEN=your_token_here
# TELEGRAM_CHAT_ID=your_id_here

# Run the bot
python main.py
```

---

## ✅ Verify It Works

You should see:

```
2024-01-15 10:30:45 - INFO - Starting Meteora Pool Screening Bot
2024-01-15 10:30:46 - INFO - ==================================================
2024-01-15 10:30:46 - INFO - Starting pool screening cycle
2024-01-15 10:30:47 - INFO - Fetching Meteora pools from Solscan...
2024-01-15 10:30:48 - INFO - Fetched 45 pools from Meteora
```

**And**: Check your Telegram - you should get a test message "✅ Meteora Pool Bot Started!"

---

## 🛑 Stop the Bot

Press `Ctrl + C` in your terminal.

---

## 🚀 Next Steps

1. **Read README.md** - Full documentation
2. **Check WORKFLOW.md** - How it works in detail
3. **Adjust .env** - Customize screening criteria
4. **Monitor logs** - Watch bot.log for activity
5. **Upload to GitHub** - Back up your config (NOT the .env!)

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| "No module named 'aiohttp'" | Run: `pip install -r requirements.txt` |
| "API key not set" | Edit .env with your actual keys |
| "Chat not found" | Use @userinfobot to get correct Chat ID |
| "Rate limited" | Increase SCREENING_INTERVAL in .env |
| No notifications | Check that all criteria in .env are correct |

---

## 📚 Learn More

- **[README.md](README.md)** - Complete guide
- **[WORKFLOW.md](WORKFLOW.md)** - How bot works
- **[API_KEYS_GUIDE.md](API_KEYS_GUIDE.md)** - Getting API keys
- **[.env.example](.env.example)** - All configuration options

---

**Done! Bot is now monitoring Meteora pools and will notify you on Telegram when good pools are found.** 🎉

For detailed setup, see **README.md**.
