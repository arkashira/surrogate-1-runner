package surrogate1

import (
	"encoding/json"
	"net"
	"sync"
	"time"
)

type Agent struct {
	ID       string
	Conn     net.Conn
	Messages chan Message
	mu       sync.Mutex
}

type Message struct {
	To      string
	Content json.RawMessage
}

type AgentCoordinator struct {
	Agents map[string]*Agent
	mu     sync.Mutex
}

func NewAgentCoordinator() *AgentCoordinator {
	return &AgentCoordinator{
		Agents: make(map[string]*Agent),
	}
}

func (ac *AgentCoordinator) AddAgent(agent *Agent) {
	ac.mu.Lock()
	defer ac.mu.Unlock()
	ac.Agents[agent.ID] = agent
}

func (ac *AgentCoordinator) Broadcast(message Message) {
	ac.mu.Lock()
	defer ac.mu.Unlock()
	for _, agent := range ac.Agents {
		agent.Messages <- message
	}
}

func (ac *AgentCoordinator) Start() {
	ticker := time.NewTicker(10 * time.Millisecond)
	defer ticker.Stop()

	for range ticker.C {
		ac.mu.Lock()
		for _, agent := range ac.Agents {
			select {
			case msg := <-agent.Messages:
				ac.Broadcast(msg)
			default:
			}
		}
		ac.mu.Unlock()
	}
}

// Summary:
// - Implemented Agent and Message structs for real-time communication
// - Created AgentCoordinator struct to manage agents and broadcast messages
// - Added AddAgent method to coordinator to register new agents
// - Added Broadcast method to coordinator to send messages to all agents
// - Implemented Start method for coordinator to continuously check for new messages and broadcast them