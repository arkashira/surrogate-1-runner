
# ... (existing code)

class Workflow(Base):
    __tablename__ = "workflows"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    paused = Column(Boolean, default=False)
    current_node_id = Column(Integer, ForeignKey("workflow_nodes.id"))
    current_node = relationship("WorkflowNode", back_populates="workflows")

    # ... (existing columns)