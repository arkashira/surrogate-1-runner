package models

type AgentRequest struct {
	Step string
}

func (r AgentRequest) ToBytes() []byte {
	// Serialize request to bytes
	return []byte(r.Step)
}

type AgentResponse struct {
	Status string
}

func (r *AgentResponse) FromBytes(data []byte) {
	// Deserialize bytes to response
	r.Status = string(data)
}

type Workflow struct {
	Steps []string
}