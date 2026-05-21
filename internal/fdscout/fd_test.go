package fdscout

import (
	"testing"
)

func TestListOpenFDs(t *testing.T) {
	t.Parallel()

	fds, err := ListOpenFDs()
	if err != nil {
		t.Fatalf("ListOpenFDs returned error: %v", err)
	}

	// The process should have at least the standard descriptors (0,1,2).
	if len(fds) < 3 {
		t.Fatalf("expected at least 3 open fds, got %d", len(fds))
	}

	seen := make(map[int]bool)
	for _, fd := range fds {
		if fd.FD < 0 {
			t.Errorf("invalid FD number %d", fd.FD)
		}
		if fd.Target == "" {
			t.Errorf("fd %d has empty target", fd.FD)
		}
		if seen[fd.FD] {
			t.Errorf("duplicate FD entry for %d", fd.FD)
		}
		seen[fd.FD] = true
	}
}