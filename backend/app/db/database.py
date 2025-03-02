import aiosqlite

DATABASE = "database.db"

async def init_db():
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                excel_id TEXT NOT NULL
            )
            """
        )
        await db.commit()
