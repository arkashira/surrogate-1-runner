package detector

// DriftEvent is the information that the CLI (and any CI step) will surface.
// Keep it JSON‑serialisable so the stub implementation can read/write it
// without extra dependencies.
type DriftEvent struct {
	Message string `json:"message"`
}

// Detect is the only function the rest of the codebase needs to call.
// It hides the concrete implementation behind an interface, making it
// trivial to swap in a “real” detector later.
func Detect() ([]DriftEvent, error) {
	return impl.Detect()
}