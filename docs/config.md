## Configuration Documentation

The configuration file `config.yaml` plays a crucial role in setting up the surrogate-1-runner application. It contains various parameters that control the behavior of the runners. Below is a detailed explanation of each parameter:

### Parameters

- **dataset_path**: Specifies the path to the dataset directory. This is where the raw data is located.
  - Example: `/path/to/dataset`

- **output_path**: Defines the path where the processed data will be stored after normalization and deduplication.
  - Example: `/path/to/output`

- **shard_count**: Determines the number of shards to divide the dataset into. Each shard is processed by a separate runner.
  - Example: `16`

- **interval_minutes**: Sets the interval in minutes at which the runners should be launched. This can be adjusted based on the frequency of data updates.
  - Example: `30`

### Example Configuration

Below is an example of a fully configured `config.yaml` file: