import Foundation
import AppKit   // for NSPasteboard

/// High‑performance, thread‑safe monitor that reliably captures *paste‑cascade* events
/// (rapid successive changes to the system pasteboard) on macOS.
///
/// Typical usage:
///
///