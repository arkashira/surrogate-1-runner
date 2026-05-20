use clap::{App, Arg};
use std::process;

mod cli;
mod dataset;

fn main() {
    let matches = App::new("surrogate-1")
        .version("1.0")
        .author("axentx-dev-bot")
        .about("Parallel public-dataset ingest workers")
        .arg(
            Arg::with_name("shard-id")
                .long("shard-id")
                .value_name("SHARD_ID")
                .help("Sets the shard ID for the worker")
                .takes_value(true)
                .required(true),
        )
        .arg(
            Arg::with_name("output")
                .long("output")
                .value_name("OUTPUT_FILE")
                .help("Sets the output file path")
                .takes_value(true),
        )
        .get_matches();

    let shard_id = matches.value_of("shard-id").unwrap().parse::<u32>().unwrap();
    let output_file = matches.value_of("output").unwrap_or("output.json");

    if shard_id >= 16 {
        eprintln!("Invalid shard ID: {}", shard_id);
        process::exit(1);
    }

    cli::run(shard_id, output_file);
}