#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_demo_command() {
        let output = std::process::Command::new("cargo")
            .arg("run")
            .arg("--bin")
            .arg("kubesnap")
            .arg("--")
            .arg("demo")
            .arg("--namespace")
            .arg("all")
            .output()
            .unwrap();
        assert!(output.status.success());
    }
}