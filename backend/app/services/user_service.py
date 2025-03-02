import aiosqlite
from db.database import DATABASE

async def save_user_info_to_db(user_id: str, excel_id: str):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute(
            "INSERT INTO users (user_id, excel_id) VALUES (?, ?)",
            (user_id, excel_id)
        )
        await db.commit()

async def get_user_excel_from_db(user_id: str):
    async with aiosqlite.connect(DATABASE) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            if row is None:
                return None
            return {"excel_id": row["excel_id"]}
            
async def delete_user_info_from_db(user_id: str) -> bool:
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("DELETE FROM users WHERE user_id = ?", (user_id,)) as cursor:
            await db.commit()
            # Check if any row was affected
            if cursor.rowcount == 0:
                return False
            return True