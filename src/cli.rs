use std::fs::File;
use std::io::Write;
use std::process;

pub fn run(shard_id: u32, output_file: &str) {
    let dataset = dataset::get_dataset(shard_id);
    let normalized_data = dataset::normalize_data(dataset);

    let mut file = File::create(output_file).unwrap();
    file.write_all(normalized_data.as_bytes()).unwrap();
}