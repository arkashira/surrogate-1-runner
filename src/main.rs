
mod attack_detection;

use attack_detection::{AttackDetector, AttackAlert};
use std::sync::mpsc;
use std::thread;

fn main() {
    let detector = AttackDetector::new();
    detector.detect_attack();

    let (rx, _tx) = mpsc::channel();
    thread::spawn(move || {
        loop {
            match rx.recv() {
                Ok(AttackAlert { message }) => {
                    println!("Attack alert: {}", message);
                }
                Err(_) => {
                    println!("Channel closed");
                    break;
                }
            }
        }
    });

    // Keep the main thread running to prevent the program from exiting
    loop {}
}