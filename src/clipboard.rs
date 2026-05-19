//! Clipboard‑related utilities.
//!
//! The public API consists of three functions:
//! 1. `ax_direct_paste()` – stub for the future Accessibility‑API implementation.
//! 2. `cg_event_cmd_v()` – concrete fallback that synthesises Cmd+V via `osascript`.
//! 3. `paste_with_fallback()` – tries (1) then (2) and logs the outcome.

use std::process::Command;
use log::{info, error};

/// Attempt to paste using the macOS Accessibility (AX) API.
///
/// **Current status** – not implemented.  The function returns an `Err` with a
/// helpful message so the fallback path is exercised automatically.
///
/// When you have a real AX implementation, replace the body with the proper
/// calls (e.g. via the `core-graphics` or `accessibility` crates) and return
/// `Ok(())` on success.
pub fn ax_direct_paste() -> Result<(), String> {
    // TODO: replace with real AX code.
    Err("AX direct paste not implemented".into())
}

/// Fallback paste that sends a synthetic Cmd+V keystroke using `osascript`.
///
/// This works on any macOS where the `osascript` command is present (all
/// standard installations).  It is deliberately simple and has **no
/// external Rust dependencies** beyond the standard library.
///
/// Returns:
/// * `Ok(())` – the script exited with status 0 (the keystroke was sent).
/// * `Err(String)` – the script failed; the string contains the stderr output.
pub fn cg_event_cmd_v() -> Result<(), String> {
    // AppleScript that presses Cmd+V in the frontmost application.
    let script = r#"
        tell application "System Events"
            keystroke "v" using command down
        end tell
    "#;

    let output = Command::new("osascript")
        .arg("-e")
        .arg(script)
        .output()
        .map_err(|e| format!("Failed to spawn osascript: {}", e))?;

    if output.status.success() {
        info!("CGEvent Cmd+V synthetic paste succeeded");
        Ok(())
    } else {
        let stderr = String::from_utf8_lossy(&output.stderr);
        error!("CGEvent Cmd+V failed: {}", stderr);
        Err(format!("CGEvent Cmd+V failed: {}", stderr))
    }
}

/// High‑level helper used by the application.
///
/// 1. Try `ax_direct_paste()`.
/// 2. If it fails, log the error and try `cg_event_cmd_v()`.
/// 3. Log the final outcome (success or double‑failure).
pub fn paste_with_fallback() {
    match ax_direct_paste() {
        Ok(_) => {
            info!("AX direct paste succeeded");
        }
        Err(ax_err) => {
            error!("AX direct paste failed: {}", ax_err);
            match cg_event_cmd_v() {
                Ok(_) => info!("Fallback CGEvent Cmd+V succeeded"),
                Err(cg_err) => error!("Fallback CGEvent Cmd+V also failed: {}", cg_err),
            }
        }
    }
}