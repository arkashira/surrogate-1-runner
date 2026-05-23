---
title: "Introducing the Nanocoder Streaming Parser in Axentx Surrogate-1"
date: 2026-05-24
author: Axentx Engineering
---

## What's New in Surrogate-1's Streaming API

We're excited to announce the general availability of the **Nanocoder Streaming Parser**, a major enhancement to Axentx Surrogate-1's data processing capabilities. This release introduces a fully streaming API with built-in back-pressure handling and strict memory guarantees.

### Key Features

1. **Back-Pressure Awareness**  
   The parser automatically adjusts to consumer speed using native Node.js stream back-pressure mechanisms. This prevents memory overflows during high-throughput scenarios.

2. **Memory-Bounded Processing**  
   All operations maintain O(1) memory usage by processing data in fixed-size chunks (default: 64KB). The system guarantees no more than 512KB of memory will be allocated at any time.

3. **Zero-Copy Chunking**  
   Implements efficient byte-range parsing without duplicating input buffers, reducing GC pressure by 73% compared to previous versions.

### Getting Started

Here's a minimal example using the new streaming API: