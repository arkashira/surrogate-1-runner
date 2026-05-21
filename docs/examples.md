## Usage Examples & Best Practices for the Surrogate‑1 Validation Engine

The Surrogate‑1 Validation Engine is a lightweight Java library that validates
structured data against a set of rules defined in JSON Schema or custom
validation DSL.  Below you will find step‑by‑step examples that cover:

1. **Project setup** – adding the library to your Maven/Gradle build.
2. **Basic validation** – validating a single JSON payload.
3. **Batch validation** – validating a stream of records.
4. **Custom rule integration** – extending the engine with your own logic.
5. **Best practices** – performance, error handling, and versioning tips.

> **Note**: All examples assume you are using Java 17 or newer.

---

### 1. Project Setup

#### Maven