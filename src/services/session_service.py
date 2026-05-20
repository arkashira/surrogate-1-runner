from typing import List
from ..models import Session
from ..database import database

async def get_all_sessions() -> List[Session]:
    query = "SELECT * FROM sessions"
    return await database.fetch_all(query)

async def delete_session(session_id: str) -> bool:
    query = "DELETE FROM sessions WHERE id = $1"
    result = await database.execute(query, session_id)
    return result == "DELETE 1"