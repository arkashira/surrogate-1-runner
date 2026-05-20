import org.kiwix.kiwixengine.KiwiXEngine;
import org.kiwix.kiwixengine.config.Configuration;
import org.kiwix.kiwixengine.workflow.Workflow;
import org.kiwix.kiwixengine.workflow.WorkflowManager;

public class WorkflowEngine {
    private KiwiXEngine kiwiXEngine;
    private WorkflowManager workflowManager;

    public WorkflowEngine(Configuration config) {
        this.kiwiXEngine = new KiwiXEngine(config);
        this.workflowManager = new WorkflowManager(kiwiXEngine);
    }

    public void startWorkflow(Workflow workflow) {
        workflowManager.startWorkflow(workflow);
    }

    public void stopWorkflow(Workflow workflow) {
        workflowManager.stopWorkflow(workflow);
    }
}