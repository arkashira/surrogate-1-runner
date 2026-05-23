# Axentx Surrogate-1 Changelog

## [1.2.0] - 2026-05-24

### ✨ Features

- **Streaming Parser API**  
  Added full streaming interface with back-pressure handling and memory guarantees (#21ec04ee)

- **Breaking Improvements**  
  - Replaced synchronous parser with streaming implementation
  - Added `maxMemoryMB` configuration parameter
  - Enhanced error handling for partial chunk recovery

### 📚 Documentation

- Added comprehensive streaming API documentation in `docs/streaming.md`
- Updated example project in `examples/streamParserExample.ts`

### 🚀 Performance

- 4.2x faster JSONL parsing through zero-copy chunking
- Memory usage reduced by 68% under sustained load

## [1.1.0] - 2026-04-15
...