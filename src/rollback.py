from .audit_trail import AuditTrail

class RollbackManager:
    def __init__(self, audit_trail: AuditTrail):
        self.audit_trail = audit_trail

    def rollback_model_version(self):
        previous_entry = self.audit_trail.get_previous_entry()
        if previous_entry:
            print(f"Rolling back to previous model version: {previous_entry['model_version']}")
            # Implement logic to revert model version here
        else:
            print("No previous model version found.")

    def rollback_prompt_state(self):
        previous_entry = self.audit_trail.get_previous_entry()
        if previous_entry:
            print(f"Rolling back to previous prompt state: {previous_entry['prompt_state']}")
            # Implement logic to revert prompt state here
        else:
            print("No previous prompt state found.")