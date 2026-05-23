import queue
from typing import Optional

class StreamingBuffer:
    def __init__(self, max_size: int = 500 * 1024 * 1024):
        self.buffer = queue.Queue(max_size)
        self.current_chunk: Optional[bytes] = None
        self.current_position = 0

    def add_chunk(self, chunk: bytes):
        """添加新块到缓冲区"""
        if self.current_chunk is None:
            self.current_chunk = chunk
        else:
            if self.buffer.full():
                self.buffer.get_nowait()
            self.buffer.put(self.current_chunk)
            self.current_chunk = chunk
        self.current_position = 0

    def read(self, size: int) -> bytes:
        """流式读取数据（支持跨块读取）"""
        if self.current_chunk is None:
            return b''

        remaining_in_chunk = len(self.current_chunk) - self.current_position
        if size <= remaining_in_chunk:
            data = self.current_chunk[self.current_position:self.current_position+size]
            self.current_position += size
            return data

        data = self.current_chunk[self.current_position:]
        self.current_position = len(self.current_chunk)

        while remaining_size > 0:
            if self.buffer.empty():
                break
            next_chunk = self.buffer.get_nowait()
            chunk_size = min(remaining_size, len(next_chunk))
            data += next_chunk[:chunk_size]
            remaining_size -= chunk_size
            if remaining_size > 0:
                self.current_chunk = next_chunk[chunk_size:]
                self.current_position = chunk_size
            else:
                self.current_chunk = next_chunk[chunk_size:]
                self.current_position = 0
                break

        return data

    def clear(self):
        """清空缓冲区"""
        self.buffer.queue.clear()
        self.current_chunk = None
        self.current_position = 0