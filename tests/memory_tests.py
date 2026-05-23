import psutil
import pytest
import time
from contextlib import contextmanager
from surrogate.parser import StreamParser
from tests.utils import generate_large_json_stream

@contextmanager
def memory_profiler():
    start_mem = psutil.virtual_memory().used
    start_time = time.time()
    try:
        yield
    finally:
        end_mem = psutil.virtual_memory().used
        end_time = time.time()
        print(f"\nMemory used: {end_mem - start_mem} bytes")
        print(f"Processing time: {end_time - start_time:.2f}s")

def test_parser_memory_usage():
    parser = StreamParser()
    data_stream = generate_large_json_stream(10_000_000)  # 10M entries
    
    with memory_profiler():
        assert parser.process_stream(data_stream) is not None
        # Ensure memory stays below 500MB
        assert (psutil.virtual_memory().used - parser._peak_memory) < 500_000_000

def test_parser_leak_detection():
    parser = StreamParser()
    data_stream = generate_large_json_stream(1_000_000)
    
    for _ in range(5):  # 5 iterations
        with memory_profiler():
            parser.process_stream(data_stream)
            # Force GC between iterations
            parser.clear_cache()
            import gc; gc.collect()
    
    # Memory should stabilize after multiple runs
    assert parser._memory_peak_history[-1] < parser._memory_peak_history[0] * 1.1

def test_streaming_performance():
    parser = StreamParser()
    data_stream = generate_large_json_stream(5_000_000)
    
    start_time = time.time()
    with memory_profiler():
        parser.process_stream(data_stream)
    end_time = time.time()
    
    # Ensure processing time doesn't exceed 30s for 5M entries
    assert (end_time - start_time) < 30