//! Clipboard handling utilities for AX “direct‑paste” attempts.
//!
//! The public API is deliberately small so that the same code can be used
//! both in production (real OS clipboard) and in unit‑tests (in‑memory mock).
//!
//!