package main

import (
	"context"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"os/exec"
	"strings"
	"time"

	"golang.org/x/crypto/ssh"
)

// TerminalAccess handles secure terminal access for surrogate-1 runners
type TerminalAccess struct {
	authToken string
	sshConfig *ssh.ClientConfig
}

// AuthRequest represents authentication request payload
type AuthRequest struct {
	Token string `json:"token"`
	User  string `json:"user"`
}

// AuthResponse represents authentication response
type AuthResponse struct {
	Success bool   `json:"success"`
	Message string `json:"message"`
	Session  string `json:"session,omitempty"`
}

// NewTerminalAccess creates a new terminal access instance
func NewTerminalAccess(authToken string) *TerminalAccess {
	return &TerminalAccess{
		authToken: authToken,
	}
}

// Authenticate validates the authentication token
func (ta *TerminalAccess) Authenticate(ctx context.Context) (*AuthResponse, error) {
	authReq := AuthRequest{
		Token: ta.authToken,
		User:  os.Getenv("USER"),
	}

	resp, err := ta.postJSON("/api/auth", authReq)
	if err != nil {
		return nil, fmt.Errorf("authentication request failed: %w", err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("failed to read auth response: %w", err)
	}

	var authResp AuthResponse
	if err := json.Unmarshal(body, &authResp); err != nil {
		return nil, fmt.Errorf("failed to parse auth response: %w", err)
	}

	if !authResp.Success {
		return nil, fmt.Errorf("authentication failed: %s", authResp.Message)
	}

	ta.sshConfig = ta.buildSSHConfig(authResp.Session)
	return &authResp, nil
}

// buildSSHConfig creates SSH client configuration from session token
func (ta *TerminalAccess) buildSSHConfig(session string) *ssh.ClientConfig {
	return &ssh.ClientConfig{
		User: "axentx",
		Auth: []ssh.AuthMethod{
			ssh.PublicKeys(sshAgentKey()),
		},
		HostKeyCallback: ssh.InsecureIgnoreHostKey(),
		Timeout:         30 * time.Second,
	}
}

// sshAgentKey retrieves SSH key from agent
func sshAgentKey() ssh.Signer {
	agent, err := ssh.NewAgent()
	if err != nil {
		panic(err)
	}
	return agent.Signers()[0]
}

// Connect establishes a secure SSH connection
func (ta *TerminalAccess) Connect(ctx context.Context, host string) (*ssh.Client, error) {
	if ta.sshConfig == nil {
		return nil, fmt.Errorf("authentication not completed")
	}

	client, err := ssh.Dial("tcp", host, ta.sshConfig)
	if err != nil {
		return nil, fmt.Errorf("failed to establish SSH connection: %w", err)
	}

	return client, nil
}

// ExecuteTerminal runs a command in the terminal session
func (ta *TerminalAccess) ExecuteTerminal(ctx context.Context, client *ssh.Client, command string) error {
	session, err := client.NewSession()
	if err != nil {
		return fmt.Errorf("failed to create SSH session: %w", err)
	}
	defer session.Close()

	output, err := session.CombinedOutput(command)
	if err != nil {
		return fmt.Errorf("command execution failed: %w, output: %s", err, string(output))
	}

	fmt.Println(string(output))
	return nil
}

// InteractiveTerminal provides interactive terminal access
func (ta *TerminalAccess) InteractiveTerminal(ctx context.Context, client *ssh.Client) error {
	session, err := client.NewSession()
	if err != nil {
		return fmt.Errorf("failed to create interactive session: %w", err)
	}
	defer session.Close()

	// Set up PTY for terminal
	pty, err := session.Openpty()
	if err != nil {
		return fmt.Errorf("failed to open PTY: %w", err)
	}
	defer pty.Close()

	// Start command
	cmd := exec.CommandContext(ctx, "bash")
	cmd.Stdin = pty
	cmd.Stdout = pty
	cmd.Stderr = pty

	if err := cmd.Start(); err != nil {
		return fmt.Errorf("failed to start command: %w", err)
	}

	// Copy stdin/stdout
	go copyToSession(cmd, pty)
	go copyFromSession(cmd, pty)

	<-cmd.ProcessState
	return nil
}

func copyToSession(cmd *exec.Cmd, pty *os.File) {
	io.Copy(pty, os.Stdin)
}

func copyFromSession(cmd *exec.Cmd, pty *os.File) {
	io.Copy(os.Stdout, pty)
}

// HealthCheck validates terminal access is working
func (ta *TerminalAccess) HealthCheck(ctx context.Context) error {
	resp, err := ta.postJSON("/api/health", nil)
	if err != nil {
		return fmt.Errorf("health check failed: %w", err)
	}
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)
	fmt.Printf("Health check response: %s\n", string(body))
	return nil
}

// postJSON sends a JSON POST request
func (ta *TerminalAccess) postJSON(path string, data interface{}) (*http.Response, error) {
	jsonData, err := json.Marshal(data)
	if err != nil {
		return nil, err
	}

	req, err := http.NewRequest("POST", path, strings.NewReader(string(jsonData)))
	if err != nil {
		return nil, err
	}

	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer "+ta.authToken)

	client := &http.Client{Timeout: 30 * time.Second}
	return client.Do(req)
}

// GetSessionInfo retrieves current session information
func (ta *TerminalAccess) GetSessionInfo(ctx context.Context) (*AuthResponse, error) {
	resp, err := ta.postJSON("/api/session", nil)
	if err != nil {
		return nil, fmt.Errorf("session info request failed: %w", err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("failed to read session info: %w", err)
	}

	var authResp AuthResponse
	if err := json.Unmarshal(body, &authResp); err != nil {
		return nil, fmt.Errorf("failed to parse session info: %w", err)
	}

	return &authResp, nil
}

// CloseSession terminates the current terminal session
func (ta *TerminalAccess) CloseSession(ctx context.Context) error {
	resp, err := ta.postJSON("/api/session/close", nil)
	if err != nil {
		return fmt.Errorf("close session request failed: %w", err)
	}
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)
	fmt.Printf("Session close response: %s\n", string(body))
	return nil
}