import aiosqlite
from db.database import DATABASE

async def insert_resume(filename: str, resume_text: str):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute(
            "INSERT INTO resumes (filename, resume_text) VALUES (?, ?)",
            (filename, resume_text)
        )
        await db.commit()
