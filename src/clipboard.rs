use std::process::Command;
use std::io::{self, Write};

/// Result type for clipboard operations
pub type ClipboardResult = Result<(), ClipboardError>;

/// Errors that can occur while pasting.
#[derive(Debug)]
pub enum ClipboardError {
    Io(io::Error),
    AppleScript(String),
    AxError(String),
    CgEventError(String),
}

impl std::fmt::Display for ClipboardError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            ClipboardError::Io(e) => write!(f, "IO error: {}", e),
            ClipboardError::AppleScript(s) => write!(f, "AppleScript error: {}", s),
            ClipboardError::AxError(s) => write!(f, "AX error: {}", s),
            ClipboardError::CgEventError(s) => write!(f, "CGEvent error: {}", s),
        }
    }
}

impl std::error::Error for ClipboardError {}

impl From<io::Error> for ClipboardError {
    fn from(err: io::Error) -> Self {
        ClipboardError::Io(err)
    }
}

/// Public entry point – tries the three paste methods in order.
/// Returns `Ok(())` on the first success, otherwise the last error.
pub fn paste_with_fallback(text: &str) -> ClipboardResult {
    // 1. AX direct paste
    if let Err(e) = ax_direct_paste(text) {
        log::warn!("AX paste failed: {}. Trying CGEvent.", e);
        // 2. CGEvent paste
        if let Err(e) = cg_event_paste(text) {
            log::warn!("CGEvent paste failed: {}. Trying AppleScript.", e);
            // 3. AppleScript fallback
            applescript_paste(text)
        } else {
            Ok(())
        }
    } else {
        Ok(())
    }
}

/// Sets the system clipboard to `text`.  Uses `pbcopy` for simplicity.
fn set_clipboard(text: &str) -> io::Result<()> {
    let mut child = Command::new("pbcopy")
        .stdin(std::process::Stdio::piped())
        .spawn()?;

    {
        let stdin = child.stdin.as_mut().ok_or_else(|| {
            io::Error::new(io::ErrorKind::Other, "Failed to open pbcopy stdin")
        })?;
        stdin.write_all(text.as_bytes())?;
    }

    child.wait()?;
    Ok(())
}

/// Attempts to paste using the Accessibility API (AXUIElement).
/// In practice this is just a thin wrapper around an AppleScript that
/// sends ⌘‑V to the front‑most application.
fn ax_direct_paste(text: &str) -> ClipboardResult {
    set_clipboard(text)?;

    let script = r#"tell application "System Events"
    keystroke "v" using command down
end tell"#;

    let output = Command::new("osascript")
        .arg("-e")
        .arg(script)
        .output()
        .map_err(|e| ClipboardError::AxError(e.to_string()))?;

    if output.status.success() {
        log::info!("AX paste succeeded");
        Ok(())
    } else {
        let err = String::from_utf8_lossy(&output.stderr);
        Err(ClipboardError::AxError(err.to_string()))
    }
}

/// Attempts to paste by synthesising a Cmd‑V key‑event via a short Python
/// script that uses Quartz.  This is the most reliable fallback on
/// recent macOS versions.
fn cg_event_paste(text: &str) -> ClipboardResult {
    set_clipboard(text)?;

    let python_script = r#"
import Quartz
import time

# 'v' key code
key_code = 9

# Command modifier
flags = Quartz.kCGEventFlagMaskCommand

# Key down
key_down = Quartz.CGEventCreateKeyboardEvent(None, key_code, True)
Quartz.CGEventSetFlags(key_down, flags)
Quartz.CGEventPost(Quartz.kCGHIDEventTap, key_down)

# Small pause
time.sleep(0.01)

# Key up
key_up = Quartz.CGEventCreateKeyboardEvent(None, key_code, False)
Quartz.CGEventSetFlags(key_up, flags)
Quartz.CGEventPost(Quartz.kCGHIDEventTap, key_up)
"#;

    let output = Command::new("python3")
        .args(&["-c", python_script])
        .output()
        .map_err(|e| ClipboardError::CgEventError(e.to_string()))?;

    if output.status.success() {
        log::info!("CGEvent paste succeeded");
        Ok(())
    } else {
        let err = String::from_utf8_lossy(&output.stderr);
        Err(ClipboardError::CgEventError(err.to_string()))
    }
}

/// AppleScript fallback – identical to the AX script but used only
/// when the other two methods fail.  It is kept separate so callers
/// can decide whether to use it as a final resort.
fn applescript_paste(text: &str) -> ClipboardResult {
    set_clipboard(text)?;

    let script = r#"tell application "System Events"
    keystroke "v" using command down
end tell"#;

    let output = Command::new("osascript")
        .arg("-e")
        .arg(script)
        .output()
        .map_err(|e| ClipboardError::AppleScript(e.to_string()))?;

    if output.status.success() {
        log::info!("AppleScript paste succeeded");
        Ok(())
    } else {
        let err = String::from_utf8_lossy(&output.stderr);
        Err(ClipboardError::AppleScript(err.to_string()))
    }
}