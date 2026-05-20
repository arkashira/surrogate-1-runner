import time
from typing import Dict, Any
from performance_metrics import PerformanceMetrics

class GPUScaler:
    def __init__(self, target_fps: int, performance_metrics: PerformanceMetrics):
        self.target_fps = target_fps
        self.performance_metrics = performance_metrics
        self.gpu_scale_factor = 1.0

    def scale_gpu(self) -> float:
        """Scale GPU usage based on real-time performance metrics."""
        metrics = self.performance_metrics.get_all_metrics()
        current_fps = self._calculate_current_fps(metrics)

        if current_fps < self.target_fps * 0.95:
            self.gpu_scale_factor = min(1.0, self.gpu_scale_factor * 1.1)
        elif current_fps > self.target_fps * 1.05:
            self.gpu_scale_factor = max(0.5, self.gpu_scale_factor * 0.9)

        return self.gpu_scale_factor

    def _calculate_current_fps(self, metrics: Dict[str, Any]) -> float:
        """Calculate current FPS based on GPU metrics."""
        gpu_load = metrics['gpu']['gpu_0']['load']
        return self.target_fps * (1 - gpu_load / 100)

    def manual_override(self, scale_factor: float) -> None:
        """Manually override the GPU scale factor."""
        self.gpu_scale_factor = scale_factor