export type InteractionStatus = 'success' | 'error' | 'timeout' | 'pending';
export interface IAgentInteraction {
    agentId: string;
    timestamp: Date;
    status: InteractionStatus;
    errorMessage?: string;
}

// src/agentInteraction.ts - Enhanced with type safety and immutability
export class AgentInteraction implements IAgentInteraction {
    constructor(
        public readonly agentId: string,
        public readonly timestamp: Date,
        public readonly status: InteractionStatus,
        public readonly errorMessage: string = ''
    ) {}

    // Factory method for easier creation
    static create(
        agentId: string,
        status: InteractionStatus,
        errorMessage: string = ''
    ): AgentInteraction {
        return new AgentInteraction(agentId, new Date(), status, errorMessage);
    }
}

// src/issue.ts - Improved issue detection with more robust logic
export class Issue {
    private readonly interactions: AgentInteraction[] = [];

    addInteraction(interaction: AgentInteraction): void {
        this.interactions.push(interaction);
    }

    getInteractions(): readonly AgentInteraction[] {
        return [...this.interactions]; // Return defensive copy
    }

    identifyIssue(): string {
        const errorInteractions = this.interactions.filter(
            i => i.status === 'error' || i.status === 'timeout'
        );

        if (errorInteractions.length === 0) {
            return 'No issues identified';
        }

        const errorMessages = errorInteractions.map(
            i => `${i.agentId}: ${i.errorMessage || i.status}`
        );

        return `Issues identified:\n${errorMessages.join('\n')}`;
    }
}

// src/visualization.ts - Enhanced with better formatting and error handling
export class Visualization {
    private readonly issues: Issue[] = [];

    addIssue(issue: Issue): void {
        this.issues.push(issue);
    }

    visualizeInteractions(): void {
        if (this.issues.length === 0) {
            console.log('No issues to visualize');
            return;
        }

        this.issues.forEach((issue, index) => {
            console.log(`\n=== Issue ${index + 1} ===`);
            console.log(issue.identifyIssue());

            issue.getInteractions().forEach(interaction => {
                console.log('\nInteraction Details:');
                console.log(`- Agent: ${interaction.agentId}`);
                console.log(`- Timestamp: ${interaction.timestamp.toISOString()}`);
                console.log(`- Status: ${interaction.status}`);

                if (interaction.status === 'error' || interaction.status === 'timeout') {
                    console.log(`- Error: ${interaction.errorMessage || 'No details'}`);
                }
            });

            console.log('\n' + '='.repeat(30));
        });
    }
}

// src/index.ts - Main execution with better organization
import { AgentInteraction, Issue, Visualization } from './modules';

function main() {
    // Create sample issues
    const issue1 = new Issue();
    issue1.addInteraction(AgentInteraction.create('agent1', 'success'));
    issue1.addInteraction(AgentInteraction.create('agent2', 'error', 'Timeout error'));

    const issue2 = new Issue();
    issue2.addInteraction(AgentInteraction.create('agent3', 'success'));
    issue2.addInteraction(AgentInteraction.create('agent4', 'timeout'));

    // Visualize results
    const visualization = new Visualization();
    visualization.addIssue(issue1);
    visualization.addIssue(issue2);
    visualization.visualizeInteractions();
}

main();