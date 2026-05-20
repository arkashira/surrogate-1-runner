# Audit Log Schema

The audit log schema provides immutable records of all LLM interactions, ensuring traceability and compliance.

## Key Features

1. **Immutability**: Enforced through Pydantic's `frozen` config and JSON serialization
2. **Tamper Evidence**: Sorted JSON serialization creates consistent hashes
3. **Comprehensive Context**: Captures both prompt/response and execution environment
4. **Extensibility**: Optional metadata field for additional context

## Schema Details

- `timestamp` (string): ISO 8601 UTC timestamp of record creation
- `model_version` (string): Model identifier (e.g., "gpt-4-1106-preview")
- `execution_environment` (dict): System context including:
  - Hardware specifications
  - Software versions
  - Configuration parameters
- `prompt` (string): Original input to the LLM
- `response` (string): Generated output from the LLM
- `metadata` (dict, optional): Additional context like user/session IDs

## Usage Example