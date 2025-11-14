import aiosqlite
from config import DB_PATH

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                telegram_id INTEGER UNIQUE NOT NULL,
                target_folder TEXT,
                survey_time INTEGER,
                gpt_request TEXT,
                blocked_user TEXT DEFAULT '[]'
            )
        """)
        await db.commit()


async def add_user(telegram_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (telegram_id) VALUES (?)",
            (telegram_id,)
        )
        await db.commit()


async def get_target_folder(telegram_id: int) -> str:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("""
                              SELECT target_folder
                              FROM users
                              WHERE telegram_id = ?
                              """, (telegram_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None


async def update_target_folder(telegram_id: int, target_folder: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
                         UPDATE users
                         SET target_folder = ?
                         WHERE telegram_id = ?
                         """, (target_folder, telegram_id))
        await db.commit()
        print(target_folder)



async def get_blocked_users(telegram_id: int) -> str:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("""
                              SELECT blocked_user
                              FROM users
                              WHERE telegram_id = ?
                              """, (telegram_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else '[]'


async def update_blocked_users(telegram_id: int, blocked_id: int):
    import json
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("""
                              SELECT blocked_user
                              FROM users
                              WHERE telegram_id = ?
                              """, (telegram_id,)) as cursor:
            row = await cursor.fetchone()
            current = row[0] if row else '[]'

        try:
            lst = json.loads(current)
        except Exception:
            lst = []

        if blocked_id not in lst:
            lst.append(blocked_id)
            await db.execute("""
                             UPDATE users
                             SET blocked_user = ?
                             WHERE telegram_id = ?
                             """, (json.dumps(lst), telegram_id))
            await db.commit()

async def get_gpt_request(telegram_id: int) -> str:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("""
                              SELECT gpt_request
                              FROM users
                              WHERE telegram_id = ?
                              """, (telegram_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None
async def update_gpt_request(telegram_id: int, gpt_request: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
                         UPDATE users
                         SET gpt_request = ?
                         WHERE telegram_id = ?
                         """, (gpt_request, telegram_id))
        await db.commit()
