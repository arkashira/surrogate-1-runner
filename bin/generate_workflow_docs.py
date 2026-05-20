import json
from pathlib import Path

def generate_markdown(workflow_data: dict) -> str:
    """
    Generates a Markdown string from a workflow data dictionary.
    Uses tables for parameters to improve readability.
    """
    lines = []
    
    # Workflow Header
    lines.append(f"# Workflow: {workflow_data.get('name', 'Untitled')}")
    lines.append("")
    
    if workflow_data.get('description'):
        lines.append(workflow_data['description'])
        lines.append("")
        
    lines.append(f"**ID:** `{workflow_data.get('id', 'N/A')}`")
    lines.append("")

    # Steps
    steps = workflow_data.get('steps', [])
    for index, step in enumerate(steps, 1):
        lines.append(f"## Step {index}: {step.get('name', 'Untitled Step')}")
        lines.append("")
        
        if step.get('description'):
            lines.append(step['description'])
            lines.append("")

        # Parameters Table
        params = step.get('parameters', [])
        if params:
            lines.append("**Parameters:**")
            lines.append("")
            # Table Header
            lines.append("| Name | Type | Required | Description |")
            lines.append("|------|------|----------|-------------|")
            
            # Table Rows
            for param in params:
                name = param.get('name', '')
                p_type = param.get('type', 'any')
                required = "Yes" if param.get('required') else "No"
                desc = param.get('description', '')
                
                # Escape pipes in description if necessary, or handle simple text
                desc = desc.replace('|', '\\|')
                
                lines.append(f"| **{name}** | `{p_type}` | {required} | {desc} |")
            lines.append("")
        else:
            lines.append("*No parameters required.*")
            lines.append("")
            
    return "\n".join(lines)

def main():
    workflow_path = Path(__file__).parent / "workflow.json"
    output_path = Path(__file__).parent / "workflow_docs.md"

    with open(workflow_path, 'r') as f:
        workflow_data = json.load(f)

    markdown_content = generate_markdown(workflow_data)

    with open(output_path, 'w') as f:
        f.write(markdown_content)
        
    print(f"Documentation generated successfully at {output_path}")

if __name__ == "__main__":
    main()