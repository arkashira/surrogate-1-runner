import os
import hashlib
import concurrent.futures
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor
import resource

class Parser:
    def __init__(self, max_workers: int = 4, chunk_size: int = 1000, memory_limit_mb: int = 512):
        self.max_workers = max_workers
        self.chunk_size = chunk_size
        self.memory_limit_bytes = memory_limit_mb * 1024 * 1024
        self._validate_memory_limits()

    def _validate_memory_limits(self):
        """Ensure system can handle requested memory limits"""
        current_limit = resource.getrlimit(resource.RLIMIT_AS)
        if self.memory_limit_bytes > current_limit[0]:
            raise MemoryError(f"Requested {self.memory_limit_bytes} bytes exceeds system limit of {current_limit[0]} bytes")

    def parse_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process data in chunks with memory monitoring"""
        results = []
        for i in range(0, len(data), self.chunk_size):
            chunk = data[i:i + self.chunk_size]
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = [executor.submit(self._process_item, item) for item in chunk]
                results.extend([future.result() for future in concurrent.futures.as_completed(futures)])
            self._check_memory_usage()
        return results

    def _check_memory_usage(self):
        """Monitor memory usage and raise if approaching limits"""
        current_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024
        if current_usage > self.memory_limit_bytes * 0.9:
            raise MemoryError(f"Memory usage {current_usage} bytes exceeds 90% of limit {self.memory_limit_bytes}")

    def _process_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize and deduplicate a single item"""
        normalized_item = self._normalize_item(item)
        return self._deduplicate_item(normalized_item)

    def _normalize_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize item fields (implement specific normalization logic)"""
        if 'name' in item:
            item['name'] = item['name'].strip().lower()
        return item

    def _deduplicate_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Deduplicate using MD5 hash of normalized content"""
        item_hash = self._generate_md5_hash(item)
        if not hasattr(self, '_seen_hashes'):
            self._seen_hashes = set()
        if item_hash in self._seen_hashes:
            return None
        self._seen_hashes.add(item_hash)
        return item

    def _generate_md5_hash(self, item: Dict[str, Any]) -> str:
        """Generate consistent MD5 hash for deduplication"""
        item_str = str(sorted(item.items())).encode('utf-8')
        return hashlib.md5(item_str).hexdigest()