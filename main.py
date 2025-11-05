from telethon import TelegramClient, functions, types
import asyncio


API_ID = 123123
API_HASH = ''
SESSION_NAME = ''
target_folder = ""

async def get_folder_by_name(client, folder_name: str):

    result = await client(functions.messages.GetDialogFiltersRequest())
    for f in result.filters:
        if isinstance(f, types.DialogFilter):
            title = getattr(f, 'title', None)
            name = getattr(title, 'text', title)
            if name == folder_name:
                return f
    return None


async def get_chats_from_folder(client, folder_name: str) -> list:

    folder = await get_folder_by_name(client, folder_name)
    if not folder:
        return []

    def get_peer_id(p):
        return getattr(p, 'user_id', None) or getattr(p, 'channel_id', None) or getattr(p, 'chat_id', None)

    included = {get_peer_id(p) for p in getattr(folder, 'include_peers', []) if get_peer_id(p) is not None}
    pinned = {get_peer_id(p) for p in getattr(folder, 'pinned_peers', []) if get_peer_id(p) is not None}
    excluded = {get_peer_id(p) for p in getattr(folder, 'exclude_peers', []) if get_peer_id(p) is not None}

    target_ids = included.union(pinned)

    dialogs = await client.get_dialogs()
    ids = []
    for d in dialogs:
        chat_id = d.entity.id
        if chat_id in excluded:
            continue
        if chat_id in target_ids:
            ids.append(chat_id)

    unique_ids = list(dict.fromkeys(ids))
    return unique_ids


async def main():
    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        ids = await get_chats_from_folder(client, target_folder)
        print(ids)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error: {e}")
