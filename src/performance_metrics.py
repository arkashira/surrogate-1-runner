import time
import psutil
import GPUtil
from typing import Dict, Any

class PerformanceMetrics:
    def __init__(self):
        self.gpu_metrics = {}
        self.cpu_metrics = {}
        self.memory_metrics = {}

    def get_gpu_metrics(self) -> Dict[str, Any]:
        """Get GPU metrics using GPUtil."""
        gpus = GPUtil.getGPUs()
        for gpu in gpus:
            self.gpu_metrics[f'gpu_{gpu.id}'] = {
                'load': gpu.load * 100,
                'memory_used': gpu.memoryUsed,
                'memory_total': gpu.memoryTotal,
                'temperature': gpu.temperature
            }
        return self.gpu_metrics

    def get_cpu_metrics(self) -> Dict[str, Any]:
        """Get CPU metrics using psutil."""
        self.cpu_metrics = {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'cpu_count': psutil.cpu_count(),
            'cpu_freq': psutil.cpu_freq().current if psutil.cpu_freq() else None
        }
        return self.cpu_metrics

    def get_memory_metrics(self) -> Dict[str, Any]:
        """Get memory metrics using psutil."""
        self.memory_metrics = {
            'memory_percent': psutil.virtual_memory().percent,
            'memory_used': psutil.virtual_memory().used,
            'memory_total': psutil.virtual_memory().total
        }
        return self.memory_metrics

    def get_all_metrics(self) -> Dict[str, Any]:
        """Get all performance metrics."""
        return {
            'gpu': self.get_gpu_metrics(),
            'cpu': self.get_cpu_metrics(),
            'memory': self.get_memory_metrics()
        }