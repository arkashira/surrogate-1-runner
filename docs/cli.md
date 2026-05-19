## Command Line Interface

The surrogate-1 runner accepts several flags to control its behavior.  
Below is a list of the available options.

| Flag | Description | Default |
|------|-------------|---------|
| `--validate-file` | **(New)** Validate that the specified mesh file exists before starting the workflow. If the file is missing, the runner will exit with a clear error message instead of proceeding. | `false` |
| `--mesh-file` | Path to the mesh file to be used in the workflow. Supports both absolute and relative paths. | *required* |
| `--shard-id` | Identifier for the dataset shard to process. | `0` |
| `--log-level` | Logging verbosity (`debug`, `info`, `warn`, `error`). | `info` |

### Example Usage