pub fn get_dataset(shard_id: u32) -> Vec<String> {
    // Mock dataset for testing
    vec![
        format!("data-{}", shard_id),
        format!("data-{}", shard_id + 1),
        format!("data-{}", shard_id + 2),
    ]
}

pub fn normalize_data(data: Vec<String>) -> String {
    data.join("\n")
}