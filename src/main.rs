use std::process::Command;
use std::path::Path;

fn main() {
    let board_file = "/path/to/board/file.kicad_pcb"; // Replace with actual board file path
    let surrogate_cli = "/path/to/surrogate-1-cli"; // Replace with actual Surrogate-1 CLI path

    // Validate paths exist before proceeding
    if !Path::new(board_file).exists() {
        eprintln!("Error: Board file not found at {}", board_file);
        return;
    }

    if !Path::new(surrogate_cli).exists() {
        eprintln!("Error: Surrogate-1 CLI not found at {}", surrogate_cli);
        return;
    }

    let output = Command::new(surrogate_cli)
        .arg("route")
        .arg(board_file)
        .output()
        .expect("Failed to execute Surrogate-1 CLI");

    if output.status.success() {
        let routed_netlist = String::from_utf8_lossy(&output.stdout);
        // Apply routed netlist to KiCAD session
        println!("Successfully generated routed netlist:\n{}", routed_netlist);
    } else {
        let error_message = String::from_utf8_lossy(&output.stderr);
        eprintln!("Routing failed with error:\n{}", error_message);
    }
}