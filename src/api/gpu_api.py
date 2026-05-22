from fastapi import FastAPI, HTTPException
from src.gpu_manager import GPUManager

app = FastAPI()
gpu_manager = GPUManager()

@app.post("/allocate_gpu")
def allocate_gpu(task_id: str):
    gpu_id = gpu_manager.allocate_gpu(task_id)
    if gpu_id is None:
        raise HTTPException(status_code=400, detail="No GPUs available")
    return {"task_id": task_id, "gpu_id": gpu_id}

@app.post("/release_gpu")
def release_gpu(task_id: str):
    if not gpu_manager.release_gpu(task_id):
        raise HTTPException(status_code=400, detail="GPU not allocated to this task")
    return {"task_id": task_id, "status": "GPU released"}

@app.get("/gpu_info")
def get_gpu_info():
    return gpu_manager.get_gpu_info()