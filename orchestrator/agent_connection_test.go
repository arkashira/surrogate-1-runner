package orchestrator

import (
	"context"
	"net"
	"testing"
	"time"

	"github.com/axentx/surrogate-1/models"
)

func TestAgentConnection(t *testing.T) {
	listener, err := net.Listen("tcp", "localhost:0")
	if err != nil {
		t.Fatalf("failed to listen: %v", err)
	}
	defer listener.Close()

	go func() {
		conn, err := listener.Accept()
		if err != nil {
			t.Errorf("failed to accept: %v", err)
			return
		}
		defer conn.Close()

		buf := make([]byte, 1024)
		n, err := conn.Read(buf)
		if err != nil {
			t.Errorf("failed to read: %v", err)
			return
		}

		req := models.AgentRequest{}
		req.FromBytes(buf[:n])

		resp := models.AgentResponse{
			Status: "OK",
		}
		_, err = conn.Write(resp.ToBytes())
		if err != nil {
			t.Errorf("failed to write: %v", err)
			return
		}
	}()

	addr := listener.Addr().String()
	conn, err := NewAgentConnection(addr)
	if err != nil {
		t.Fatalf("failed to connect: %v", err)
	}
	defer conn.Close()

	req := models.AgentRequest{
		Step: "test_step",
	}
	err = conn.SendRequest(context.Background(), req)
	if err != nil {
		t.Errorf("failed to send request: %v", err)
	}

	resp, err := conn.ReceiveResponse(context.Background())
	if err != nil {
		t.Errorf("failed to receive response: %v", err)
	}

	if resp.Status != "OK" {
		t.Errorf("unexpected response status: got %v, want OK", resp.Status)
	}
}

func TestOrchestrator(t *testing.T) {
	agentAddrs := []string{"localhost:8080", "localhost:8081"}
	o, err := NewOrchestrator(agentAddrs)
	if err != nil {
		t.Fatalf("failed to create orchestrator: %v", err)
	}

	workflow := models.Workflow{
		Steps: []string{"step1", "step2"},
	}

	err = o.HandleWorkflow(workflow)
	if err != nil {
		t.Errorf("failed to handle workflow: %v", err)
	}
}