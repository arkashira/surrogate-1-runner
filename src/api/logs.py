
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from models import User, SessionMetadata, CommandLog
from schemas import CommandLogCreate
from database import get_db
from security import get_current_user

app = FastAPI()

@app.get("/api/logs", response_model=List[CommandLog])
def read_logs(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    logs = db.query(CommandLog).filter(CommandLog.user_id == current_user.id).all()
    return logs

@app.post("/api/logs", response_model=CommandLog)
def write_log(command: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    command_log = CommandLog(
        user_id=current_user.id,
        command=command,
        timestamp=datetime.now(),
        session_metadata=current_user.session_metadata
    )
    db.add(command_log)
    db.commit()
    db.refresh(command_log)
    return command_log

# src/api/routers/logs.py

from fastapi import APIRouter
from .logs import app as logs_app

router = APIRouter()
router.include_router(logs_app)

# src/static/js/logs.js

import axios from 'axios';

const apiUrl = '/api/logs';

async function fetchLogs() {
    const response = await axios.get(apiUrl);
    return response.data;
}

async function searchLogs(query) {
    const response = await axios.get(`${apiUrl}?command=${query}`);
    return response.data;
}

export { fetchLogs, searchLogs };

# src/static/js/App.js

import { fetchLogs, searchLogs } from './logs';

function Logs() {
    const [logs, setLogs] = React.useState([]);
    const [query, setQuery] = React.useState('');

    React.useEffect(() => {
        fetchLogs().then(data => setLogs(data));
    }, []);

    async function handleSearch(event) {
        event.preventDefault();
        const data = await searchLogs(query);
        setLogs(data);
    }

    return (
        <div>
            <form onSubmit={handleSearch}>
                <input type="text" value={query} onChange={event => setQuery(event.target.value)} />
                <button type="submit">Search</button>
            </form>
            <ul>
                {logs.map(log => (
                    <li key={log.id}>
                        {log.command} - {log.timestamp} - {log.user_id}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default Logs;