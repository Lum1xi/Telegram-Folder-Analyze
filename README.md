# 🚀 Telegram Folder Analyzer Bot (Aiogram + Telethon + Gemini API)

A simple Telegram bot that:
- 🗂️ Lets an admin choose a Telegram folder (Dialog Filter) to monitor.
- 📥 Collects recent messages from chats inside that folder (last ~12 hours).
- 🤖 Sends aggregated context plus a configurable instruction ("GPT request") to Google Gemini (Generative Language API) for analysis.
- 💾 Stores per-user settings (folder name, survey frequency, custom analysis prompt) in a local SQLite database via aiosqlite.

Default Gemini model now: **gemini-2.5-flash** (see `geminiapi.py`).

## 📦 Requirements
Listed in `requirements.txt`:
```
aiogram~=3.22.0
Telethon~=1.41.2
python-dotenv~=1.2.1
aiosqlite~=0.21.0
aiohttp~=3.12.15
```
Install with:
```bash
pip install -r requirements.txt
```

## ✨ Features
- 🧩 Command keyboard:
  - ▶️ "Analyze now" – fetch messages and run AI summary.
  - 📁 "Choose folder" – set target folder name stored in DB.
  - 🧠 "Configure GPT Request" – update analysis instruction.
- ⚡ Async, non-blocking I/O (aiogram + telethon + aiohttp).
- 🗃️ Simple persistence (SQLite file, path configurable).

## 🛠 Tech Stack
- 🐍 Python 3.11+
- 🤖 aiogram (Telegram Bot API framework)
- 📡 telethon (Telegram client for reading messages & folders)
- 🧬 aiosqlite (async SQLite)
- 🗝️ python-dotenv (environment configuration)
- 🌐 aiohttp (HTTP client for Gemini API)

## 🗂 Project Structure (simplified)
```
config.py          -> Loads environment variables
main.py            -> Bot entrypoint (dispatcher, routers, DB init, telethon client start)
database.py        -> Async CRUD for user settings
bots/handlers/     -> Bot command & message handlers (start, setup)
bots/telethon_service.py -> Folder & message collection logic
geminiapi.py       -> Gemini API wrapper (call_gemini_api, generate_text(prompt, request_text))
keyboards.py       -> Reply keyboard factory
.env               -> Environment variables (DO NOT COMMIT REAL SECRETS)
```

## 🔐 Environment Variables (.env)
Create a `.env` file (never commit real secrets):
```
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
OWNER_ID=YOUR_TELEGRAM_NUMERIC_ID
GEMINI_KEY=YOUR_GEMINI_API_KEY
API_ID=YOUR_TELEGRAM_API_ID
API_HASH=YOUR_TELEGRAM_API_HASH
SESSION_NAME=your_session_name
DB_PATH=data.db
```
Notes:
- 👤 OWNER_ID is used by IsAdmin filter (ensure it matches your Telegram account numeric ID).
- 🧪 GEMINI_KEY comes from Google AI Studio (Generative Language API key).
- 💼 SESSION_NAME identifies Telethon session file (e.g. "123").

⚠️ Real tokens/keys MUST be kept out of commits and rotated if exposed. The sample `.env` in your local workspace contains live values; change them before publishing.

## 📦 Installation
1. 📥 Clone repository.
2. 🧪 Create & activate virtual environment.
3. 📑 Install dependencies:
   ```bash
   pip install aiogram telethon aiosqlite python-dotenv aiohttp
   ```
4. ✍️ Create `.env` with your values.
5. ▶️ Run:
   ```bash
   python main.py
   ```

On first run Telethon may prompt for authorization (code sent to your Telegram account). After that a session file is stored locally.

## 🧭 Usage Flow
1. ✅ Start the bot (ensure OWNER_ID matches your account).
2. 💬 Open bot chat, use the keyboard:
   - 📁 Choose folder: enter exact folder name as it appears in Telegram (Dialog Filter title).
   - 🧠 Configure GPT Request: supply custom instruction (e.g. "Summarize discussions and list action items").
   - ▶️ Analyze now: fetch messages, send to Gemini (model gemini-2.5-flash), receive analysis.


