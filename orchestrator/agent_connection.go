package orchestrator

import (
	"context"
	"net"
	"sync"
	"time"

	"github.com/axentx/surrogate-1/models"
)

type AgentConnection struct {
	conn net.Conn
}

func NewAgentConnection(addr string) (*AgentConnection, error) {
	conn, err := net.Dial("tcp", addr)
	if err != nil {
		return nil, err
	}
	return &AgentConnection{conn: conn}, nil
}

func (ac *AgentConnection) SendRequest(ctx context.Context, req models.AgentRequest) error {
	deadline := time.Now().Add(200 * time.Millisecond)
	ctx, cancel := context.WithDeadline(ctx, deadline)
	defer cancel()

	err := ac.conn.SetWriteDeadline(deadline)
	if err != nil {
		return err
	}

	_, err = ac.conn.Write(req.ToBytes())
	return err
}

func (ac *AgentConnection) ReceiveResponse(ctx context.Context) (models.AgentResponse, error) {
	var resp models.AgentResponse
	deadline := time.Now().Add(200 * time.Millisecond)
	ctx, cancel := context.WithDeadline(ctx, deadline)
	defer cancel()

	err := ac.conn.SetReadDeadline(deadline)
	if err != nil {
		return resp, err
	}

	buf := make([]byte, 1024)
	n, err := ac.conn.Read(buf)
	if err != nil {
		return resp, err
	}

	resp.FromBytes(buf[:n])
	return resp, nil
}

func (ac *AgentConnection) Close() error {
	return ac.conn.Close()
}

type Orchestrator struct {
	agents []*AgentConnection
	mu     sync.Mutex
}

func NewOrchestrator(agentAddrs []string) (*Orchestrator, error) {
	o := &Orchestrator{}
	for _, addr := range agentAddrs {
		agentConn, err := NewAgentConnection(addr)
		if err != nil {
			return nil, err
		}
		o.agents = append(o.agents, agentConn)
	}
	return o, nil
}

func (o *Orchestrator) HandleWorkflow(workflow models.Workflow) error {
	o.mu.Lock()
	defer o.mu.Unlock()

	for _, step := range workflow.Steps {
		for _, agent := range o.agents {
			req := models.AgentRequest{
				Step: step,
			}
			err := agent.SendRequest(context.Background(), req)
			if err != nil {
				return err
			}

			resp, err := agent.ReceiveResponse(context.Background())
			if err != nil {
				return err
			}

			// Process response...
		}
	}
	return nil
}