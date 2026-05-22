import torch
import logging
from typing import List, Dict, Optional

class GPUManager:
    def __init__(self, max_gpus: int = 4):
        self.max_gpus = max_gpus
        self.available_gpus = self._detect_gpus()
        self.allocated_gpus = {}

    def _detect_gpus(self) -> List[int]:
        """Detect available GPUs."""
        gpus = []
        if torch.cuda.is_available():
            num_gpus = min(torch.cuda.device_count(), self.max_gpus)
            gpus = list(range(num_gpus))
        return gpus

    def allocate_gpu(self, task_id: str) -> Optional[int]:
        """Allocate a GPU for a task."""
        if not self.available_gpus:
            logging.warning("No GPUs available for allocation.")
            return None

        gpu_id = self.available_gpus.pop(0)
        self.allocated_gpus[task_id] = gpu_id
        logging.info(f"Allocated GPU {gpu_id} to task {task_id}.")
        return gpu_id

    def release_gpu(self, task_id: str) -> bool:
        """Release a GPU allocated to a task."""
        if task_id not in self.allocated_gpus:
            logging.warning(f"Task {task_id} has no allocated GPU.")
            return False

        gpu_id = self.allocated_gpus.pop(task_id)
        self.available_gpus.append(gpu_id)
        logging.info(f"Released GPU {gpu_id} from task {task_id}.")
        return True

    def get_gpu_info(self) -> Dict[str, List[int]]:
        """Get information about available and allocated GPUs."""
        return {
            "available_gpus": self.available_gpus,
            "allocated_gpus": list(self.allocated_gpus.values())
        }