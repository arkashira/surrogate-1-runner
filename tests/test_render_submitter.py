import unittest
from unittest.mock import Mock
from src.render.submitter import RenderSubmitter

class TestRenderSubmitter(unittest.IsolatedAsyncioTestCase):
    async def test_submit_render_job(self):
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
        self.assertEqual(completed_frame, frame_data)

    async def test_batch_submit_render_jobs(self):
        gpu_cluster = {
            "gpu_id": "gpu_0",
            "status": "available"
        }
        submitter = RenderSubmitter(gpu_cluster)
        frame_data_list = [
            {
                "width": 1920,
                "height": 1080,
                "format": "RGB"
            },
            {
                "width": 1920,
                "height": 1080,
                "format": "RGB"
            }
        ]
        completed_frames = await submitter.batch_submit_render_jobs(frame_data_list)
        self.assertEqual(len(completed_frames), 2)

    async def test_error_callback(self):
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
        await submitter.submit_render_job(frame_data, gpu_cluster["gpu_id"])
        submitter.error_callback("job_0", "GPU failed or timed out")
        self.assertEqual(submitter.submitted_jobs["job_0"]["error"], "GPU failed or timed out")

if __name__ == "__main__":
    unittest.main()