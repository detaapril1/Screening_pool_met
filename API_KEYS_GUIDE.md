# Complete API Keys Guide - Meteora Pool Screening Bot

This guide walks you through getting every API key you need, with screenshots-style instructions.

## 📋 Quick Summary

You need **3 things** to run the bot:

1. **Solscan API Key** - Access blockchain pool data
2. **Telegram Bot Token** - Send notifications
3. **Telegram Chat ID** - Receive notifications

Total cost: **FREE** ✓

---

## 1️⃣ Solscan API Key

### What it does
Solscan is a Solana blockchain explorer. It provides an API to fetch data about tokens, pools, and transactions on Solana.

**Cost**: Free (with rate limits) | Paid plans available
**Rate Limit**: ~100 requests/minute on free tier
**What you get**: Pool data including liquidity, volume, fees, age

### Step-by-Step Guide

#### Step 1: Go to Solscan Website
```
URL: https://solscan.io/
Open in your browser
```

#### Step 2: Sign Up (if you don't have an account)
```
Click "Sign Up" (top right corner)
┌─────────────────────────┐
│  Solscan Explorer       │
│  [☰ Menu]              │
│                         │
│               [Sign Up] │
│               [Login]   │
└─────────────────────────┘

Fill in:
- Email address
- Password (strong password)
- Confirm password

Click "Sign Up"
```

#### Step 3: Verify Email
```
Check your email inbox
Find email from Solscan
Click verification link
```

#### Step 4: Go to Account Settings
```
Click your profile icon (top right)
┌─────────────────────────┐
│ Profile Menu            │
├─────────────────────────┤
│ [👤] Profile            │
│ [⚙️]  Settings          │ ← Click here
│ [🔑] API Keys           │ ← Or here
│ [📊] Dashboard          │
│ [🚪] Logout             │
└─────────────────────────┘
```

#### Step 5: Navigate to API Keys
```
In Settings page:
Left sidebar:
├─ General
├─ Notification
├─ API Keys        ← Click here
└─ Billing
```

#### Step 6: Create New API Key
```
Click "API Keys" section
You'll see:

"API Keys"
┌─────────────────────────────────┐
│ Key Name: [_____________]       │
│ Description: [_____________]    │
│                                 │
│ [Create API Key]  [Cancel]      │
└─────────────────────────────────┘

Enter:
- Key Name: "Meteora Pool Bot"
- Description: "For screening Meteora pools"

Click "Create API Key"
```

#### Step 7: Copy Your API Key
```
You'll see:
┌─────────────────────────────────┐
│ API Key Created Successfully!   │
│                                 │
│ Key: abc123xyz789def456ghi...   │
│       [Copy]                    │
│                                 │
│ ⚠️ Save this key in a safe place!
│ You won't see it again.         │
└─────────────────────────────────┘

Click [Copy] button
Paste into .env file
```

#### Step 8: Add to .env
```bash
# Open .env file (created earlier)
nano .env

# Find this line:
SOLSCAN_API_KEY=your_solscan_api_key_here

# Replace with:
SOLSCAN_API_KEY=abc123xyz789def456ghi

# Save file (Ctrl+X, then Y, then Enter in nano)
```

### Alternative: Using API Keys Page

```
Direct URL:
https://solscan.io/user/settings/api-keys

Benefits:
- Manage multiple API keys
- See usage statistics
- Delete old keys
- Regenerate key if compromised
```

---

## 2️⃣ Telegram Bot Token

### What it does
Telegram Bot Token is a secret key that allows the bot to send messages through Telegram's API.

**Cost**: Free (100% free, forever)
**Rate Limit**: ~30 messages/second per bot
**What you get**: Ability to send notifications to Telegram

### Step-by-Step Guide

#### Step 1: Open Telegram
```
Download Telegram from:
- App Store (iOS)
- Google Play (Android)
- telegram.org (Desktop)

Or use: web.telegram.org (Web version)
```

#### Step 2: Search for BotFather
```
In Telegram:
1. Click search icon (magnifying glass)
2. Search: "@BotFather"
3. Open the official BotFather account
   (Verified with blue checkmark ✓)
```

#### Step 3: Start BotFather
```
Click "Start" button
Or send: /start

You'll see:
┌────────────────────────────┐
│ BotFather                  │
├────────────────────────────┤
│ I can help you create and  │
│ manage Telegram bots. Here │
│ are all the commands I     │
│ know:                      │
│                            │
│ /newbot - create a new bot │
│ /mybots - edit your bots   │
│ /deletbot - delete a bot   │
│ ...                        │
└────────────────────────────┘
```

#### Step 4: Create New Bot
```
Send: /newbot

BotFather responds:
"Alright! Send me the name of your bot."

You type: Meteora Pool Bot

BotFather: "Good. Now tell me the username of your bot."

You type: meteora_pool_bot
(Must be unique, lowercase, with underscore)

BotFather responds:
┌────────────────────────────┐
│ Done! Congratulations on   │
│ your new bot. You'll find  │
│ it at                      │
│ t.me/meteora_pool_bot      │
│                            │
│ Use this token to access   │
│ the HTTP API:              │
│                            │
│ 123456:ABC-DEF1234ghIkl-   │
│ zyx57W2v1u123ew11          │
│                            │
│ Keep your token secure and │
│ store it safely!           │
└────────────────────────────┘
```

#### Step 5: Copy the Token
```
Select and copy the token:
123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

Format: <BOT_ID>:<API_TOKEN>
```

#### Step 6: Add to .env
```bash
# Open .env file
nano .env

# Find:
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# Replace with:
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

# Save file
```

### Verification (Optional)

```bash
# Test if token works
curl -s https://api.telegram.org/bot123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11/getMe | python -m json.tool

# Should show bot info:
{
  "ok": true,
  "result": {
    "id": 123456,
    "is_bot": true,
    "first_name": "Meteora Pool Bot",
    "username": "meteora_pool_bot",
    "can_join_groups": true
  }
}
```

---

## 3️⃣ Telegram Chat ID

### What it does
Chat ID tells the bot WHERE to send messages (your personal ID, group, or channel).

**Cost**: Free
**Format**: Numeric ID (like: 123456789)
**Can be**: Your personal ID, group ID, or channel ID

### Step-by-Step Guide (Method 1: Using Bot)

#### Step 1: Search for UserInfo Bot
```
In Telegram:
Search: "@userinfobot"
(Verified account with blue checkmark)
```

#### Step 2: Get Your ID
```
Click "Start" or send /start

You'll see:
┌──────────────────────────────┐
│ Your Telegram information:   │
│                              │
│ User ID: 123456789           │
│ First Name: John             │
│ Username: @johndoe           │
│ Language: en                 │
│ Is Bot: No                   │
└──────────────────────────────┘
```

#### Step 3: Copy Your ID
```
Copy: 123456789
```

#### Step 4: Add to .env
```bash
# Open .env file
nano .env

# Find:
TELEGRAM_CHAT_ID=your_telegram_chat_id_here

# Replace with:
TELEGRAM_CHAT_ID=123456789

# Save file
```

### Step-by-Step Guide (Method 2: Manual)

#### Step 1: Start Your Bot
```
In Telegram:
Search for your bot: "@meteora_pool_bot"
Click "Start"
```

#### Step 2: Send Test Message
```
Send any message to your bot:
"test" or "hello"

(The bot won't respond yet, that's ok)
```

#### Step 3: Get Updates from Bot API
```
Open browser and go to:
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates

Replace <YOUR_BOT_TOKEN> with your actual token from Step 2.

Full example:
https://api.telegram.org/bot123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11/getUpdates

You'll see JSON:
{
  "ok": true,
  "result": [
    {
      "update_id": 123456,
      "message": {
        "message_id": 1,
        "date": 1705330500,
        "chat": {
          "id": 987654321,    ← YOUR CHAT ID IS HERE
          "first_name": "John"
        },
        "from": {
          "id": 987654321,    ← OR HERE
          "first_name": "John"
        },
        "text": "test"
      }
    }
  ]
}
```

#### Step 4: Extract Chat ID
```
Look for "chat": { "id": 987654321 }
Your Chat ID is: 987654321
```

#### Step 5: Add to .env
```bash
TELEGRAM_CHAT_ID=987654321
```

### For Group Chats (Optional)

If you want notifications in a group:

```
1. Create a Telegram group
2. Add your bot as admin
3. Send a message in the group:
   @userinfobot
4. It will show the group ID (negative number like: -987654321)
5. Use that in TELEGRAM_CHAT_ID
```

### For Channels (Optional)

If you want notifications in a channel:

```
1. Create a Telegram channel
2. Add your bot as admin
3. Send a message in the channel via your bot API
4. Get the channel ID from getUpdates
5. Use that in TELEGRAM_CHAT_ID
```

---

## ✅ Verification Checklist

### 1. Verify Solscan API Key

```bash
# Test the key works
curl -s "https://api.solscan.io/api/account/search?action=searchProgramCreatedAccounts&programAddress=Eo7WjKq67rjm34Z9o5KvymzZH3DLmycq5hash5LvZQJ&limit=1&token=YOUR_SOLSCAN_KEY" | python -m json.tool

# Should show pool data:
{
  "success": true,
  "data": [
    {
      "address": "...",
      "liquidity_usd": 12345,
      ...
    }
  ]
}
```

### 2. Verify Telegram Bot Token

```bash
# Test the token works
curl -s https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getMe

# Should show:
{
  "ok": true,
  "result": {
    "id": 123456,
    "is_bot": true,
    "first_name": "Meteora Pool Bot"
  }
}
```

### 3. Verify Telegram Chat ID

```bash
# Test sending a message
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/sendMessage" \
  -d "chat_id=<YOUR_CHAT_ID>&text=Test+message"

# Should show:
{
  "ok": true,
  "result": {
    "message_id": 12345,
    "text": "Test message",
    ...
  }
}
```

---

## 📝 Final .env File Template

After getting all keys, your `.env` should look like:

```bash
# ============================
# API KEYS (Required)
# ============================

SOLSCAN_API_KEY=abc123xyz789def456ghi...
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
TELEGRAM_CHAT_ID=987654321

# ============================
# Optional Settings
# ============================

MIN_LIQUIDITY_USD=10000
MIN_VOLUME_24H_USD=5000
MIN_POOL_SCORE=70
SCREENING_INTERVAL=300
DEBUG_MODE=False
```

---

## 🔒 Security Tips

### API Key Safety

```
✓ DO:
  - Keep .env file locally
  - Add to .gitignore
  - Rotate keys monthly
  - Use strong passwords
  - Delete old unused keys

✗ DON'T:
  - Commit .env to GitHub
  - Share keys publicly
  - Use in frontend code
  - Post in forums/chat
  - Hardcode in scripts
```

### If Key is Compromised

```
1. Solscan API Key:
   - Go to https://solscan.io/user/settings/api-keys
   - Delete the compromised key
   - Create a new key
   - Update .env

2. Telegram Bot Token:
   - Go to BotFather
   - Send: /mybots
   - Select your bot
   - Click "Edit Token"
   - BotFather will provide new token
   - Update .env

3. Important:
   - Restart the bot immediately
   - Monitor for unauthorized access
```

---

## 🆘 Troubleshooting

### "Invalid API Key"

**For Solscan**:
```
1. Double-check you copied the entire key
2. Make sure no extra spaces
3. Go to https://solscan.io/user/settings/api-keys
4. Create a fresh new key
5. Copy and try again
```

**For Telegram**:
```
1. Verify with BotFather:
   /mybots → select bot → check token
2. Make sure it's in format: ID:TOKEN
3. No spaces or extra characters
```

### "Invalid Chat ID"

```
1. Verify you got correct ID:
   Send message to @userinfobot
   Copy the "id" field
2. Make sure it's just numbers
   (Groups have negative numbers like: -123456)
3. Check bot is not blocked:
   Message your bot, see if it works
```

### "Rate Limited"

```
If you get "429 Too Many Requests":

For Solscan:
- Increase SCREENING_INTERVAL to 600+ seconds
- Upgrade to paid Solscan plan
- Reduce batch size

For Telegram:
- Space out messages with delays
- Don't send more than 30/second
```

---

## 📞 Getting Help

If you have issues:

1. **Solscan Support**: https://solscan.io/help
2. **Telegram BotFather**: Send /help to @BotFather
3. **GitHub Issues**: Open issue in repository
4. **Solana Community**: Ask on Solana Discord

---

**You're all set! All three API keys are free and easy to get. Total setup time: ~10 minutes.** 🎉
