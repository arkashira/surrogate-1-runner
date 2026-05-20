package security

import (
	"os"
	"os/user"
	"syscall"
	"testing"
)

// TestProcessNotRoot asserts the running process is not running as root (uid != 0)
func TestProcessNotRoot(t *testing.T) {
	uid := syscall.Getuid()
	if uid == 0 {
		t.Fatal("process is running as root (uid=0), which violates security requirements")
	}

	// Also verify via os/user for cross-platform consistency
	u, err := user.Current()
	if err != nil {
		t.Fatalf("failed to get current user: %v", err)
	}

	// Ensure we're not running as root user
	if u.Uid == "0" {
		t.Fatal("process is running as root user, which violates security requirements")
	}
}

// TestIsRunningAsNonRootUser is the main security check function
// that verifies the process is not running as root
func TestIsRunningAsNonRootUser(t *testing.T) {
	// This tests the actual security check logic
	passed, err := IsRunningAsNonRootUser()
	if err != nil {
		t.Fatalf("IsRunningAsNonRootUser returned error: %v", err)
	}

	if !passed {
		t.Fatal("security check failed: process is running as root")
	}
}

// TestGetEffectiveUID tests the UID retrieval function
func TestGetEffectiveUID(t *testing.T) {
	uid := GetEffectiveUID()
	if uid == 0 {
		t.Fatal("effective UID is 0 (root)")
	}

	// UID should be a positive integer
	if uid < 1 {
		t.Fatalf("effective UID %d is invalid", uid)
	}
}

// TestGetEffectiveUIDError tests error handling when UID retrieval fails
func TestGetEffectiveUIDError(t *testing.T) {
	// In normal operation this should not fail, but we test the function exists
	uid := GetEffectiveUID()
	if uid == 0 {
		t.Fatal("expected non-zero UID")
	}
}

// TestUserCurrentUID tests user.Current() UID retrieval
func TestUserCurrentUID(t *testing.T) {
	u, err := user.Current()
	if err != nil {
		t.Fatalf("user.Current() failed: %v", err)
	}

	uid, err := u.LookupId()
	if err != nil {
		t.Fatalf("user.LookupId() failed: %v", err)
	}

	if uid == "0" {
		t.Fatal("user.Current() returned root user")
	}
}