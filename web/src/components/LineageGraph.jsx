import React, { useState, useCallback, useMemo } from 'react';
import {
  ReactFlow,
  addEdge,
  useNodesState,
  useEdgesState,
  Controls,
  MiniMap,
  Background,
  Node,
  Edge,
  NodeTypes,
  Handle,
  Position,
  useReactFlow,
} from 'reactflow';
import 'reactflow/dist/style.css';

const nodeTypes = {
  dataset: {
    render: (props) => (
      <Node {...props}>
        <Handle type="target" position={Position.Top} />
        <Handle type="source" position={Position.Bottom} />
        <div style={{ padding: '8px', background: '#e3f2fd', borderRadius: '4px', border: '1px solid #90caf9' }}>
          <strong>Dataset</strong>
          <div style={{ fontSize: '12px', marginTop: '4px' }}>{props.data.name}</div>
          <div style={{ fontSize: '11px', color: '#666' }}>{props.data.source}</div>
        </div>
      </Node>
    ),
  },
  job: {
    render: (props) => (
      <Node {...props}>
        <Handle type="target" position={Position.Top} />
        <Handle type="source" position={Position.Bottom} />
        <div style={{ padding: '8px', background: '#fff3e0', borderRadius: '4px', border: '1px solid #ffb74d' }}>
          <strong>Job</strong>
          <div style={{ fontSize: '12px', marginTop: '4px' }}>{props.data.name}</div>
          <div style={{ fontSize: '11px', color: '#666' }}>{props.data.type}</div>
        </div>
      </Node>
    ),
  },
  model: {
    render: (props) => (
      <Node {...props}>
        <Handle type="target" position={Position.Top} />
        <Handle type="source" position={Position.Bottom} />
        <div style={{ padding: '8px', background: '#e8f5e9', borderRadius: '4px', border: '1px solid #a5d6a7' }}>
          <strong>Model</strong>
          <div style={{ fontSize: '12px', marginTop: '4px' }}>{props.data.name}</div>
          <div style={{ fontSize: '11px', color: '#666' }}>v{props.data.version}</div>
        </div>
      </Node>
    ),
  },
};

const defaultEdgeOptions = {
  animated: true,
  style: { stroke: '#666', strokeWidth: 2 },
  targetHandle: 'source',
  sourceHandle: 'target',
};

const LineageGraph = ({ modelId, onNodeSelect }) => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [selectedNodeId, setSelectedNodeId] = useState(null);
  const { setNodes: setFlowNodes } = useReactFlow();

  const fetchLineageData = useCallback(async () => {
    try {
      const response = await fetch(`/api/lineage?model_id=${modelId}`);
      if (!response.ok) throw new Error('Failed to fetch lineage data');
      const data = await response.json();
      
      const newNodes = data.nodes.map((node) => ({
        id: node.id,
        type: node.type,
        position: node.position || { x: Math.random() * 400, y: Math.random() * 300 },
        data: node,
      }));

      const newEdges = data.edges.map((edge) => ({
        id: edge.id,
        source: edge.source,
        target: edge.target,
        type: 'default',
        animated: true,
      }));

      setNodes(newNodes);
      setEdges(newEdges);
    } catch (error) {
      console.error('Error fetching lineage:', error);
    }
  }, [modelId, setNodes, setEdges]);

  const handleNodeClick = useCallback((event, node) => {
    event.stopPropagation();
    setSelectedNodeId(node.id);
    onNodeSelect?.(node);
  }, [onNodeSelect]);

  const handleBackgroundClick = useCallback(() => {
    setSelectedNodeId(null);
  }, []);

  const highlightSelectedNodes = useMemo(() => {
    if (!selectedNodeId) return nodes;
    return nodes.map((node) => ({
      ...node,
      style: node.id === selectedNodeId
        ? { borderColor: '#ff5722', borderWidth: 3, zIndex: 10 }
        : { borderColor: node.type === 'model' ? '#a5d6a7' : node.type === 'job' ? '#ffb74d' : '#90caf9' },
    }));
  }, [nodes, selectedNodeId]);

  return (
    <div style={{ width: '100%', height: '100%', position: 'relative' }}>
      <ReactFlow
        nodes={highlightSelectedNodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onNodeClick={handleNodeClick}
        onBackgroundClick={handleBackgroundClick}
        nodeTypes={nodeTypes}
        fitView
        defaultEdgeOptions={defaultEdgeOptions}
        onInit={(instance) => {
          instance.setFitView({ padding: 0.1 });
        }}
        onMoveEnd={() => {
          instance.setFitView({ padding: 0.1 });
        }}
      >
        <Controls />
        <MiniMap style={{ border: '1px solid #ccc', borderRadius: '4px' }} />
        <Background variant="dots" gap={20} size={1} />
      </ReactFlow>
      
      {selectedNodeId && (
        <div style={{
          position: 'absolute',
          top: '10px',
          right: '10px',
          background: 'rgba(0,0,0,0.8)',
          color: 'white',
          padding: '10px 15px',
          borderRadius: '4px',
          zIndex: 100,
        }}>
          <strong>Selected Node:</strong>
          <div style={{ marginTop: '5px' }}>
            {nodes.find((n) => n.id === selectedNodeId)?.data.name}
          </div>
          <div style={{ fontSize: '12px', color: '#aaa' }}>
            Type: {nodes.find((n) => n.id === selectedNodeId)?.data.type}
          </div>
        </div>
      )}
    </div>
  );
};

export default LineageGraph;