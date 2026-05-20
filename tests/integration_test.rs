use std::process::Command;
use std::path::Path;
use tempfile::NamedTempFile;
use surrogate_1::router::{route_board, RoutingResult};

#[test]
fn test_routing_integration() {
    // Create a temporary board file for testing
    let board_file = NamedTempFile::new().expect("Failed to create temp file");
    let board_path = board_file.path().to_str().unwrap();
    
    // Write minimal KiCAD board content
    std::fs::write(board_path, "(kicad_pcb (version 20211014) (host pcbnew 5.99.0-unknown)\n(net 0 \"\")\n)").unwrap();

    // Call the routing function
    let result = route_board(board_path);
    
    // Verify the result
    assert!(result.is_ok(), "Routing failed: {:?}", result.err());
    
    let routing_result = result.unwrap();
    assert!(!routing_result.netlist.is_empty(), "Empty netlist returned");
    assert!(routing_result.time_seconds > 0.0, "Invalid routing time");
    
    // Verify the output file was created
    assert!(Path::new(&routing_result.output_path).exists(), "Output file not found");
}

#[test]
fn test_cli_integration() {
    // Test the CLI directly
    let output = Command::new("surrogate-1")
        .arg("route")
        .arg("--input")
        .arg("test_data/simple_board.kicad_pcb")
        .arg("--output")
        .arg("test_output.kicad_pcb")
        .output()
        .expect("Failed to execute CLI");
    
    assert!(output.status.success(), "CLI failed: {:?}", output.stderr);
    assert!(Path::new("test_output.kicad_pcb").exists(), "Output file not created");
}