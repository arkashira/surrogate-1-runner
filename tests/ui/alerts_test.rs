use surrogate_1::ui::alerts::{Alert, Severity, render_alerts};

#[test]
fn test_alert_display() {
    let alert = Alert::new(42, "Test alert", Severity::Warning);
    let display = format!("{}", alert);
    assert!(display.contains("Test alert"));
    assert!(display.contains("WARN"));
    assert!(display.contains("id=42"));
}

#[test]
fn test_render_alerts() {
    let alerts = vec![
        Alert::new(1, "First", Severity::Info),
        Alert::new(2, "Second", Severity::Critical),
    ];

    // Capture stdout
    let mut output = Vec::new();
    {
        let stdout = std::io::stdout();
        let mut handle = stdout.lock();
        let _ = std::io::set_output_capture(Some(&mut output));
        render_alerts(&alerts);
        let _ = std::io::set_output_capture(None);
    }

    let output_str = String::from_utf8(output).expect("UTF-8");
    assert!(output_str.contains("First"));
    assert!(output_str.contains("Second"));
    assert!(output_str.contains("id=1"));
    assert!(output_str.contains("id=2"));
}