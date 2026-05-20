import os
import psutil
from utils.memory_monitor import get_memory_usage

def adaptive_batch_size(data):
    memory_threshold = 0.8  # 80% memory usage threshold
    available_memory = psutil.virtual_memory().available * (1 - memory_threshold)
    batch_size = min(len(data), available_memory // (sys.getsizeof(data[0]) * 1.2))  # 20% overhead
    return batch_size

def process_data(data):
    batch_size = adaptive_batch_size(data)
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        # process batch here
        pass

# /opt/axentx/surrogate-1/src/utils/memory_monitor.py
import psutil

def get_memory_usage():
    return psutil.virtual_memory().percent

# Summary:
# - Implemented adaptive batch sizing algorithm in batch_processor.py
# - Updated memory_monitor.py to return memory usage percentage
# - Batch size now adjusts based on available memory, staying below 80% threshold
# - Processing speed improvement depends on the specific processing task and data size