use super::*;
use assert_cmd::Command;
use predicates::prelude::*;
use std::fs;

#[test]
fn test_cli_help() {
    let mut cmd = Command::cargo_bin("surrogate-1").unwrap();
    cmd.arg("--help");
    cmd.assert().success().stdout(predicate::str::contains("Usage"));
}

#[test]
fn test_cli_version() {
    let mut cmd = Command::cargo_bin("surrogate-1").unwrap();
    cmd.arg("--version");
    cmd.assert().success().stdout(predicate::str::contains("1.0"));
}

#[test]
fn test_cli_run() {
    let mut cmd = Command::cargo_bin("surrogate-1").unwrap();
    cmd.arg("run").arg("--shard-id").arg("0");
    cmd.assert().success();
}

#[test]
fn test_cli_invalid_shard_id() {
    let mut cmd = Command::cargo_bin("surrogate-1").unwrap();
    cmd.arg("run").arg("--shard-id").arg("16");
    cmd.assert().failure().stderr(predicate::str::contains("Invalid shard ID"));
}

#[test]
fn test_cli_output_file() {
    let output_file = "test_output.json";
    let mut cmd = Command::cargo_bin("surrogate-1").unwrap();
    cmd.arg("run").arg("--shard-id").arg("0").arg("--output").arg(output_file);
    cmd.assert().success();

    assert!(fs::metadata(output_file).is_ok());
    fs::remove_file(output_file).unwrap();
}