# ⚡ Quick Start - Mulai Bot dalam 5 Menit

## 🎯 Objectives
- ✅ Install bot
- ✅ Get API keys
- ✅ Configure & run
- ✅ Monitor pools

---

## STEP 1️⃣: SETUP ENVIRONMENT (2 Menit)

### Windows
```powershell
# 1. Open Command Prompt / PowerShell

# 2. Clone repo
git clone <repo-url>
cd meteora-pool-bot

# 3. Create venv
python -m venv venv
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt
```

### Mac / Linux
```bash
# 1. Clone repo
git clone <repo-url>
cd meteora-pool-bot

# 2. Create venv
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## STEP 2️⃣: GET API KEYS (2 Menit)

### 🔑 Solscan API Key

1. Go to https://solscan.io/
2. Click **Sign In** (top right)
3. Create account atau login
4. Click **Account** (top right)
5. Go to **API Keys**
6. Click **Add New Key**
7. Copy the key

### 🤖 Telegram Bot Token

1. Open Telegram
2. Search for **@BotFather**
3. Send: `/newbot`
4. Follow instructions:
   - Give bot a name
   - Give bot username (must end with `_bot`)
5. Copy the token (looks like: `123456789:ABCdefGHI...`)

### 💬 Telegram Channel ID

1. Create a **new channel** in Telegram
2. Add the bot as admin:
   - Click channel settings
   - Add members
   - Search for your bot
   - Make it admin
3. Send any message to the channel
4. Get channel ID:

**Linux/Mac:**
```bash
curl https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates

# Look for "chat":{"id":-100123456789}
# Copy the negative number with -100 prefix
```

**Windows (use online tool):**
- Go to: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
- Replace `<YOUR_TOKEN>` with your actual token
- Find `"id":-100123456789` in the result

---

## STEP 3️⃣: CONFIGURE BOT (1 Menit)

### Create .env file

**Windows (PowerShell):**
```powershell
copy .env.example .env
notepad .env
```

**Mac/Linux:**
```bash
cp .env.example .env
nano .env
```

### Edit .env dengan nilai Anda:

```env
# Paste API keys yang sudah didapatkan
SOLSCAN_API_KEY=paste_your_solscan_key_here
TELEGRAM_BOT_TOKEN=paste_your_bot_token_here
TELEGRAM_CHANNEL_ID=-100paste_your_channel_id_here

# Biarkan sisanya default untuk sekarang
```

### Save & Close
- Windows: `Ctrl + S` → Close
- Mac/Linux: `Ctrl + X` → `Y` → `Enter`

---

## STEP 4️⃣: TEST CONFIGURATION (1 Menit)

Sebelum run bot, test koneksi:

```bash
python test_bot.py
```

Output yang diharapkan:
```
✓ Environment Variables: OK
✓ Solscan API: OK
✓ Telegram Bot: OK
✓ Pool Filter: OK
✓ Database: OK

✅ ALL TESTS PASSED!
```

Jika ada ❌, periksa:
1. API keys benar?
2. Bot adalah admin di channel?
3. Internet connection OK?

---

## STEP 5️⃣: RUN BOT! 🚀

### Option A: Simple Run (Recommended untuk testing)
```bash
python bot.py
```

Output:
```
🚀 METEORA POOL SCREENING BOT - STARTING
🔐 Validating API keys...
📡 Initializing Solscan API...
🎯 Initializing pool filter...
💬 Initializing Telegram notifier...
✓ Bot initialization successful!
✓ Telegram connection successful. Bot: @your_bot_name
✓ Database initialized: pool_tracking.db

🔍 SCAN #1 - 2024-01-15 10:00:00
📥 Fetched 100 pools from Solscan
✓ Filtering complete: 3 good pools, 97 filtered out

✨ NEW QUALITY POOL: ABC123... (Score: 78.5)
```

### Option B: Background Run (untuk production)

**Linux/Mac:**
```bash
# Using nohup
nohup python bot.py > logs/bot.log 2>&1 &

# Check status
tail -f logs/bot.log
```

**Windows (menggunakan Task Scheduler):**
1. Open **Task Scheduler**
2. Create new task
3. General tab:
   - Name: "Meteora Pool Bot"
4. Triggers tab:
   - New → At startup
5. Actions tab:
   - Program: `C:\full\path\to\python.exe`
   - Arguments: `C:\path\to\bot.py`
   - Start in: `C:\path\to\meteora-pool-bot`

---

## 🔍 MONITORING BOT

### Check Bot is Running

**Linux/Mac:**
```bash
ps aux | grep bot.py

# If running, you'll see:
# user 12345 ... python bot.py
```

**Windows:**
```powershell
Get-Process | Select-String python
```

### View Live Logs
```bash
# Linux/Mac
tail -f logs/bot.log

# Windows (use File Explorer)
# Open logs/bot.log with Notepad
```

### Bot sends message to Telegram
Bot akan mengirim alert seperti ini:

```
🟢 NEW QUALITY POOL DETECTED!

📌 Pool Information:
• Name: USDC-SOL
• Symbol: LP-USDC-SOL
• Address: ABC123...

📊 Metrics:
• Liquidity: $15,000 USD
• Volume 24h: $50,000 USD
• Safety Score: 20/25

🎯 Scoring Breakdown:
• Liquidity Score: 25/25
• Volume Score: 25/25
• Age Score: 25/25
• Safety Score: 20/25

📈 Total Score: 95.0/100
```

---

## ⚙️ FINE-TUNING

Jika bot terlalu banyak/sedikit alert, edit .env:

### Terlalu banyak alert?
```env
# Increase these thresholds:
MIN_LIQUIDITY=5000        # default 1000
MIN_VOLUME_24H=20000      # default 5000
MIN_SAFETY_SCORE=80       # default 70
SCAN_INTERVAL=600         # default 300 (scan lebih jarang)
```

### Terlalu sedikit alert?
```env
# Decrease these thresholds:
MIN_LIQUIDITY=500         # default 1000
MIN_VOLUME_24H=1000       # default 5000
MIN_SAFETY_SCORE=50       # default 70
SCAN_INTERVAL=60          # default 300 (scan lebih sering)
```

---

## ⚠️ TROUBLESHOOTING

### "ModuleNotFoundError"
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### "Invalid API key"
- Check .env - API key benar?
- Visit https://solscan.io - key ada?
- Generate key baru jika perlu

### "Bot token invalid"
- Check token di .env - format benar?
- Test: https://api.telegram.org/bot<TOKEN>/getMe
- Generate bot baru dari @BotFather

### "Chat ID not found"
- Bot sudah admin di channel?
- Channel ID format benar? (-100XXXXX atau XXXXX)
- Send message ke channel terlebih dahulu

### Bot tidak kirim notifikasi
```bash
# Check logs
tail logs/bot.log | grep -i error

# Enable debug mode
# Edit .env:
LOG_LEVEL=DEBUG

# Restart bot
```

---

## 📞 NEXT STEPS

1. **Read Full Documentation**: `METEORA_POOL_BOT_SETUP.md`
2. **Understand API Integration**: `API_INTEGRATION.md`
3. **Setup Backups**: `make backup`
4. **Monitor Regularly**: Keep logs directory clean
5. **Update Settings**: Adjust filters based on results

---

## 🎓 LEARNING RESOURCES

- **Solscan Documentation**: https://solscan.io
- **Telegram Bot API**: https://core.telegram.org/bots/api
- **Meteora**: https://meteora.ag
- **Solana**: https://docs.solana.com

---

## ✨ THAT'S IT!

Bot sekarang running dan akan:
- ✅ Screening pools setiap 5 menit
- ✅ Kirim alert untuk quality pools
- ✅ Track semua pools di database
- ✅ Prevent duplicate notifications

**Happy pool hunting! 🚀**

---

**Pro Tips:**
- 💡 Monitor bot selama 1-2 hari pertama
- 💡 Adjust filter settings sesuai kebutuhan
- 💡 Keep backups regular: `make backup`
- 💡 Check logs untuk debug: `tail -f logs/bot.log`

**Questions?** Check `README.md` atau detailed `METEORA_POOL_BOT_SETUP.md`
