import subprocess
import uuid

class GPUDiscovry:
    def discover_gpus(self):
        try:
            output = subprocess.check_output(['nvidia-smi', '--query-gpu=index,name,uuid,memory.total,pcie.link.gen.current,driver_version', '--format=csv,noheader,nounits'])
            gpus = []
            for line in output.decode('utf-8').split('\n'):
                if line.strip():
                    parts = line.split(', ')
                    gpu_info = {
                        'id': parts[2],
                        'name': parts[1],
                        'total_memory': int(parts[3]),
                        'pcie_bandwidth': int(parts[4]),
                        'driver_version': parts[5]
                    }
                    gpus.append(gpu_info)
            return gpus
        except subprocess.CalledProcessError:
            return []

class GPUAllocation:
    def __init__(self):
        self.allocated_gpus = {}

    def allocate_gpu(self, gpu_id):
        if gpu_id in self.allocated_gpus:
            return None
        handle = str(uuid.uuid4())
        self.allocated_gpus[gpu_id] = handle
        return handle

    def release_gpu(self, handle):
        for gpu_id, allocated_handle in self.allocated_gpus.items():
            if allocated_handle == handle:
                del self.allocated_gpus[gpu_id]
                break