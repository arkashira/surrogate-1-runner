# Streaming API Documentation

## Overview

The Streaming API allows you to process data from the surrogate-1 dataset in a streaming fashion, which is particularly useful for large datasets that cannot be loaded into memory all at once.

## API Endpoints

### Stream Data

`GET /stream`

This endpoint streams data from the surrogate-1 dataset. You can specify the shard ID and other parameters to control the data stream.

#### Parameters

- `shard_id` (required): The ID of the shard to stream data from.
- `limit` (optional): The maximum number of records to stream. Default is 1000.
- `offset` (optional): The number of records to skip before starting to stream. Default is 0.

#### Example Request