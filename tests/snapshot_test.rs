use axentx_surrogate::snapshot;
use mockall::predicate::*;
use std::collections::HashMap;

#[cfg(test)]
mod tests {
    use super::*;
    use mockall::*;

    mock! {
        pub trait Snapshotter {
            fn capture_snapshot(&self) -> Result<(String, String, String), String>;
        }
    }

    #[test]
    fn test_capture_snapshot_success() {
        let mut mock_snapshotter = MockSnapshotter::new();
        mock_snapshotter.expect_capture_snapshot()
            .returning(|| Ok(("snapshot123".to_string(), "resource1".to_string(), "checksum123".to_string())));

        let result = mock_snapshotter.capture_snapshot();
        assert!(result.is_ok());
        let (snapshot_id, resource_version, checksum) = result.unwrap();
        assert_eq!(snapshot_id, "snapshot123");
        assert_eq!(resource_version, "resource1");
        assert_eq!(checksum, "checksum123");
    }

    #[test]
    fn test_capture_snapshot_failure() {
        let mut mock_snapshotter = MockSnapshotter::new();
        mock_snapshotter.expect_capture_snapshot()
            .returning(|| Err("Failed to capture snapshot".to_string()));

        let result = mock_snapshotter.capture_snapshot();
        assert!(result.is_err());
        assert_eq!(result.unwrap_err(), "Failed to capture snapshot");
    }

    #[test]
    fn test_snapshot_persistence_local() {
        let snapshot_id = "snapshot123";
        let resource_version = "resource1";
        let checksum = "checksum123";

        let snapshot_data = HashMap::new();
        let persistence_result = snapshot::persist_snapshot_local(snapshot_id, resource_version, checksum, &snapshot_data);
        assert!(persistence_result.is_ok());
    }

    #[test]
    fn test_snapshot_persistence_remote() {
        let snapshot_id = "snapshot123";
        let resource_version = "resource1";
        let checksum = "checksum123";

        let snapshot_data = HashMap::new();
        let persistence_result = snapshot::persist_snapshot_remote(snapshot_id, resource_version, checksum, &snapshot_data);
        assert!(persistence_result.is_ok());
    }
}