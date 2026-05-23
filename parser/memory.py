"""
memory.py – Memory‑efficiency helpers for the surrogate‑1 parser.

The original implementation accumulated entire files or large intermediate
structures in memory, which caused high RAM pressure when processing the
public dataset (tens of gigabytes).  This module introduces three
light‑weight techniques that together reduce the memory footprint while
preserving the existing public API:

1. **Chunked streaming** – `stream_parse` reads a file in configurable
   byte‑chunks and yields parsed records lazily.  Callers can iterate over
   the generator without ever holding the whole dataset in RAM.

2. **Reusable byte‑buffer pool** – `BufferPool` maintains a small pool of
   pre‑allocated ``bytearray`` objects.  Re‑using buffers eliminates the
   overhead of repeated allocations during high‑throughput parsing.

3. **Context‑manager for temporary buffers** – `temp_buffer` provides a
   convenient ``with`` block that automatically acquires and releases a
   buffer from the pool.

These helpers are deliberately dependency‑free and can be dropped into
existing code with minimal changes: