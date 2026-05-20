use axentx_cli::prelude::*;

fn demo_command() -> Command {
    Command::new("demo")
        .about("CLI demo that captures a snapshot and then resumes watching to verify correctness")
        .arg(
            Arg::with_name("namespace")
                .long("namespace")
                .help("Namespace to watch")
                .default_value("all")
                .takes_value(true),
        )
        .action(|_, _| {
            let snapshot = kubesnap::capture_snapshot().unwrap();
            println!("Snapshot ID: {}", snapshot.id);
            println!("Resource Version: {}", snapshot.resource_version);

            let mut event_stream = kubesnap::watch_events(&snapshot.id).unwrap();
            for event in event_stream.take(30) {
                println!("{:?}", event);
            }
            println!("Demo exited cleanly.");
        })
}

fn main() {
    let matches = Command::new("kubesnap")
        .subcommand_required(true)
        .subcommand("demo", demo_command())
        .get_matches();
    match matches.subcommand() {
        Some(("demo", _)) => demo_command().run(),
        _ => unreachable!(),
    }
}