import os
from typing import Iterator, Optional
import mmap

class ChunkLoader:
    def __init__(self, file_path: str, chunk_size: int = 1024 * 1024):
        self.file_path = file_path
        self.chunk_size = chunk_size
        self.file_size = os.path.getsize(file_path)

    def load_chunks(self) -> Iterator[bytes]:
        """返回内存映射的文件块迭代器（懒加载实现）"""
        with open(self.file_path, 'rb') as file:
            with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as mmapped_file:
                for start in range(0, self.file_size, self.chunk_size):
                    end = min(start + self.chunk_size, self.file_size)
                    yield mmapped_file[start:end]

    def get_chunk_count(self) -> int:
        """计算总块数（用于预分配）"""
        return (self.file_size + self.chunk_size - 1) // self.chunk_size