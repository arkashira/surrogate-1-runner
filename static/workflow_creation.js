document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("workflow-form");
    
    form.addEventListener("submit", function (e) {
        e.preventDefault(); // Prevent actual page reload
        
        // Retrieve values
        const workflowName = document.getElementById("workflow-name").value;
        const taskName = document.getElementById("task-name").value;
        const platform = document.getElementById("platforms").value;

        // Basic Validation Check (redundant with HTML 'required', but good for JS logic)
        if (!workflowName || !taskName || !platform) {
            alert("Please fill in all fields.");
            return;
        }

        // Logic to send data to backend would go here
        console.log(`Creating Workflow: ${workflowName}`);
        console.log(`Task: ${taskName} | Platform: ${platform}`);
        
        alert(`Success! Workflow "${workflowName}" created for ${platform}.`);
        
        // Optional: Reset form
        form.reset();
    });
});