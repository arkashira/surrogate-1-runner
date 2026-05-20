package com.axentx.surrogate.dataset;

public class DatasetShard {

    private int shardId;
    private byte[] data;

    public DatasetShard(int shardId, byte[] data) {
        this.shardId = shardId;
        this.data = data;
    }

    public int getShardId() {
        return shardId;
    }

    public byte[] getData() {
        return data;
    }
}