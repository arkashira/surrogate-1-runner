
# ... (existing code)

class WorkflowNode(Base):
    __tablename__ = "workflow_nodes"

    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"))
    workflows = relationship("Workflow", back_populates="current_node")
    # ... (existing columns)