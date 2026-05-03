from fastapi import FastAPI
from routes import router
from repositories import status_event_repo

app = FastAPI()

app.include_router(router)

@app.on_event("shutdown")
async def shutdown_event():
    await session.close()