
from fastapi import FastAPI
from surrogate_1.api.dependencies import get_db, init_db
from surrogate_1.api.routes import router

app = FastAPI()

@app.on_event("startup")
async def startup():
    init_db()

app.include_router(router)