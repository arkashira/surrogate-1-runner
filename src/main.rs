use std::error::Error;
use log::{info, error};
use env_logger;

mod clipboard;

fn main() -> Result<(), Box<dyn Error>> {
    env_logger::init();

    let text = "Hello, world!"; // In a real app this would come from elsewhere

    match clipboard::paste_with_fallback(text) {
        Ok(_) => info!("Clipboard paste succeeded"),
        Err(e) => error!("All paste methods failed: {}", e),
    }

    Ok(())
}