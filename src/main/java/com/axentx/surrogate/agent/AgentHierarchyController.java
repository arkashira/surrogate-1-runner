package com.axentx.surrogate.agent;

import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/agent-hierarchy")
public class AgentHierarchyController {
    private AgentHierarchyAPI agentHierarchyAPI;

    public AgentHierarchyController(AgentHierarchyAPI agentHierarchyAPI) {
        this.agentHierarchyAPI = agentHierarchyAPI;
    }

    @GetMapping("/root")
    public Agent getRootAgent() {
        return agentHierarchyAPI.getRootAgent();
    }

    @GetMapping("/children")
    public List<Agent> getChildAgents() {
        return agentHierarchyAPI.getChildAgents();
    }

    @PostMapping("/add-child")
    public void addChildAgent(@RequestBody Agent agent) {
        agentHierarchyAPI.addChildAgent(agent);
    }

    @DeleteMapping("/remove-child")
    public void removeChildAgent(@RequestBody Agent agent) {
        agentHierarchyAPI.removeChildAgent(agent);
    }
}