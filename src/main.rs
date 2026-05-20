use std::process::Command;
use std::env;

fn main() {
    // Check if Java is installed
    let java_check = Command::new("java")
        .arg("-version")
        .output();

    if java_check.is_ok() {
        eprintln!("Warning: Java is installed. This plugin should run without Java. Please remove Java to ensure optimal performance.");
    }

    // Your existing plugin logic here
    println!("Running surrogate-1 plugin without Java dependency");

    // Add a fallback mechanism to ensure plugin execution
    if java_check.is_err() {
        eprintln!("Error: Java is not installed. Please install Java to run this plugin.");
    }
}