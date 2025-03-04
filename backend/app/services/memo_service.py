import aiosqlite
import json
from db.database import DATABASE

async def query_exists(query: str) -> bool:
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute(
            "SELECT EXISTS(SELECT 1 FROM queries WHERE query = ?)",
            (query,)
        ) as cursor:
            (exists,) = await cursor.fetchone()
            return bool(exists)

async def save_query_response(query: str, response: dict):
    response_str = json.dumps(response)
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute(
            "INSERT INTO queries (query, response) VALUES (?, ?)",
            (query, response_str)
        )
        await db.commit()

async def get_response_for_query(query: str) -> str:
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute(
            "SELECT response FROM queries WHERE query = ? LIMIT 1", (query,)
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                return json.loads(row[0])