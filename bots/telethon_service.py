from datetime import datetime, timedelta, timezone
from telethon import TelegramClient
from config import API_ID, API_HASH, SESSION_NAME
from database import get_target_folder, get_survey_time
from telethon import functions, types

from geminiapi import call_gemini_api

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)


async def get_folder_by_name(folder_name: str):
    result = await client(functions.messages.GetDialogFiltersRequest())
    for f in result.filters:
        if isinstance(f, types.DialogFilter):
            title = getattr(f, "title", None)
            name = getattr(title, "text", title)
            if name == folder_name:
                return f
    return None


async def get_chats_from_folder(user_id: int):
    folder_name = await get_target_folder(user_id)
    folder = await get_folder_by_name(folder_name)

    print(folder)

    if not folder:
        return []

    def get_peer_id(p):
        return (
                getattr(p, "user_id", None) or
                getattr(p, "channel_id", None) or
                getattr(p, "chat_id", None)
        )

    included = {get_peer_id(p) for p in folder.include_peers}
    pinned = {get_peer_id(p) for p in folder.pinned_peers}
    excluded = {get_peer_id(p) for p in folder.exclude_peers}

    target_ids = included.union(pinned)

    dialogs = await client.get_dialogs()
    ids = []

    for d in dialogs:
        chat_id = d.entity.id
        if chat_id not in excluded and chat_id in target_ids:
            ids.append(chat_id)

    unique_ids = list(dict.fromkeys(ids))
    print(unique_ids)

    return unique_ids


async def analyze_chat(client, chat_id):
    now = datetime.now(timezone.utc)
    start_time = now - timedelta(hours=12)

    collected = []

    async for msg in client.iter_messages(
        chat_id,
        reverse=True,
        offset_date=start_time
    ):
        msg_date = msg.date
        if msg_date.tzinfo is None:
            msg_date = msg_date.replace(tzinfo=timezone.utc)

        if not (start_time <= msg_date <= now):
            continue

        real_chat_id = getattr(msg.peer_id, "channel_id", None) \
                       or getattr(msg.peer_id, "chat_id", None) \
                       or getattr(msg.peer_id, "user_id", None) \
                       or chat_id

        text = msg.text if msg.text else "<non-text message>"

        collected.append({
            "chat_id": real_chat_id,
            "message_id": msg.id,
            "date": msg_date.isoformat(),
            "text": text
        })

    return collected

async def analyze_folder(user_id: int):
    chat_ids = await get_chats_from_folder(user_id)

    if not chat_ids:
        return {"status": "empty", "data": {}}

    results = {}
    for chat_id in chat_ids:
        try:
            results[chat_id] = await analyze_chat(client, chat_id)
        except Exception as e:
            results[chat_id] = {"error": str(e)}

    return {"status": "ok", "data": results}