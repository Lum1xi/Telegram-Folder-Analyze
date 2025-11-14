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

## 🤖 Gemini Prompt Handling
Current helper signature:
```python
generate_text(prompt: str, request_text)
```
It concatenates `prompt + "\n" + request_text` into a single Gemini content part. In `setup.py` the `prompt` already embeds the GPT request, and `request_text` passes it again, causing duplication. Improvement: refactor to:
```python
def generate_text(instruction: str, context: str):
    combined = f"{instruction}\n\nContext:\n{context}"
```
Or use structured parts:
```python
payload = {"contents": [{"parts": [{"text": instruction}, {"text": context}]}]}
```

## 🔧 Customization
- 🛞 Change model: edit `MODEL_NAME` in `geminiapi.py` (e.g. `gemini-2.5-flash`, `gemini-1.5-pro`).
- ✂️ Limit number of messages: adjust flattening logic in `setup.py` (currently all collected messages; consider capping to avoid token overflow).
- ⏱️ Time window: modify `start_time` in `analyze_chat` (currently last 12 hours).
- 🧠 Prompt composition: `generate_text(prompt, request_text)` concatenates user instruction + context; refactor if you need separate system vs user parts.
Note: `survey_time` column exists but there is currently NO `get_survey_time` function in `database.py`; import in `telethon_service.py` will fail if referenced. Either implement the getter or remove the import.

## 🛡 Security & Privacy
- 🚫 Do not expose API keys or the SQLite DB.
- 🌍 Data sent to Gemini leaves your environment (review compliance & policies).
- 🧪 Consider anonymizing sensitive content before analysis.
- 🔒 Limit bot access to trusted admin (OWNER_ID).
Add secret scanning (e.g. `gitleaks`) to CI before publishing.

## 📈 Potential Improvements
- 🛎 Scheduling using `survey_time` (currently stored but not executed) via asyncio tasks / APScheduler.
- 📚 Store analysis history per user/chat in a new `analyses` table.
- 🧩 Chunking for large folders (split context). 
- 🚦 Rate limiting & structured error reporting.
- 🐳 Dockerfile / requirements.txt for reproducible deployment.
- 🔄 Retry & exponential backoff for transient API/network failures.
- 📝 Improve prompt with role separation when Gemini adds native roles support.
- ✅ Implement missing `get_survey_time` and scheduling logic.
- 🧪 Split prompt parts for better model grounding.

## 🆘 Troubleshooting
- ❌ Empty analysis: folder name mismatch or no recent messages; verify Dialog Filter exists.
- 🔑 Telethon auth issues: delete `SESSION_NAME.session` and re-run for fresh login.
- 🧪 Gemini errors: verify key, quota, model name spelling, and network access.
- 🧵 Large output truncated: Telegram message limit (~4096 chars); implement splitting logic if needed.
Additional:
- 🧩 Import error for `get_survey_time`: create the function or remove the import.
- 🔁 Duplicate instruction in Gemini prompt: adjust `generate_text` usage.

## 📄 License
Add a LICENSE file (e.g. MIT) before distribution.

## ⚠️ Disclaimer
Sample project for demonstration; harden for production (logging, monitoring, compliance). Rotate any secrets already exposed.
