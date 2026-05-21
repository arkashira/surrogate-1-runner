import asyncio
from typing import Dict, List

class RenderSubmitter:
    def __init__(self, gpu_cluster: Dict[str, str]):
        self.gpu_cluster = gpu_cluster
        self.submitted_jobs = {}

    async def submit_render_job(self, frame_data: Dict[str, str], gpu_id: str):
        job_id = f"render_job_{len(self.submitted_jobs)}"
        self.submitted_jobs[job_id] = {"gpu_id": gpu_id, "frame_data": frame_data}
        await self._submit_job(job_id)

    async def _submit_job(self, job_id: str):
        # Simulate GPU submission and completion
        await asyncio.sleep(0.01)  # 10ms
        if self.gpu_cluster[job_id]["status"] == "completed":
            return self.gpu_cluster[job_id]["frame_data"]
        else:
            raise Exception("GPU failed or timed out")

    async def get_completed_frame(self, job_id: str):
        return await self._submit_job(job_id)

    async def batch_submit_render_jobs(self, frame_data_list: List[Dict[str, str]]):
        tasks = []
        for frame_data in frame_data_list:
            gpu_id = self.gpu_cluster["gpu_id"]
            task = asyncio.create_task(self.submit_render_job(frame_data, gpu_id))
            tasks.append(task)
        completed_frames = await asyncio.gather(*tasks)
        return completed_frames

    def error_callback(self, job_id: str, error: str):
        print(f"Error: {error} for job {job_id}")

    def get_gpu_cluster(self):
        return self.gpu_cluster

# Example usage:
gpu_cluster = {
    "gpu_id": "gpu_0",
    "status": "available"
}

submitter = RenderSubmitter(gpu_cluster)
frame_data = {
    "width": 1920,
    "height": 1080,
    "format": "RGB"
}

completed_frame = await submitter.submit_render_job(frame_data, gpu_cluster["gpu_id"])
print(completed_frame)

# API endpoint to support batch submission
async def render_endpoint(request):
    frame_data_list = request.json()["frame_data_list"]
    completed_frames = await submitter.batch_submit_render_jobs(frame_data_list)
    return {"completed_frames": completed_frames}

# Error callback
async def error_endpoint(request):
    job_id = request.json()["job_id"]
    error = request.json()["error"]
    submitter.error_callback(job_id, error)
    return {"error": error}