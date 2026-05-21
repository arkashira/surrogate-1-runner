import asyncio
from fastapi import FastAPI
from src.render.submitter import RenderSubmitter

app = FastAPI()

submitter = RenderSubmitter({
    "gpu_id": "gpu_0",
    "status": "available"
})

@app.post("/render")
async def render_endpoint(request):
    frame_data_list = request.json()["frame_data_list"]
    completed_frames = await submitter.batch_submit_render_jobs(frame_data_list)
    return {"completed_frames": completed_frames}

@app.post("/error")
async def error_endpoint(request):
    job_id = request.json()["job_id"]
    error = request.json()["error"]
    submitter.error_callback(job_id, error)
    return {"error": error}