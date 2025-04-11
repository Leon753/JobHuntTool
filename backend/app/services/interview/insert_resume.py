import aiosqlite
from db.database import DATABASE

async def insert_resume(filename: str, resume_text: str, userId: str):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute(
            "INSERT INTO resumes (filename, resume_text, user_id) VALUES (?, ?, ?)",
            (filename, resume_text, userId)
        )
        await db.commit()
