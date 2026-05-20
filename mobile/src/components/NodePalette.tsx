import React, { useState } from 'react';
import { View, Text, PanResponder, StyleSheet } from 'react-native';

const NodePalette = () => {
  const [isDragging, setIsDragging] = useState(false);
  const [draggedNode, setDraggedNode] = useState(null);

  const panResponder = PanResponder.create({
    onStartShouldSetPanResponder: () => true,
    onPanResponderGrant: (evt, gestureState) => {
      setIsDragging(true);
      // Logic to identify the node being dragged
      const node = identifyNode(evt.nativeEvent);
      setDraggedNode(node);
    },
    onPanResponderMove: (evt, gestureState) => {
      // Logic to move the dragged node
      if (isDragging) {
        moveNode(draggedNode, gestureState.moveX, gestureState.moveY);
      }
    },
    onPanResponderRelease: () => {
      setIsDragging(false);
      // Logic to drop the node
      dropNode(draggedNode);
      setDraggedNode(null);
    },
  });

  const identifyNode = (event) => {
    // Placeholder function to identify node based on event
    return { id: 'node1', name: 'Node 1' }; // Example node
  };

  const moveNode = (node, x, y) => {
    // Logic to visually move the node on the canvas
    console.log(`Moving ${node.name} to (${x}, ${y})`);
  };

  const dropNode = (node) => {
    // Logic to finalize the drop action
    console.log(`Dropped ${node.name}`);
  };

  return (
    <View style={styles.palette} {...panResponder.panHandlers}>
      <Text style={styles.title}>Node Palette</Text>
      {/* Render nodes here */}
      <View style={styles.node}>
        <Text>Node 1</Text>
      </View>
      <View style={styles.node}>
        <Text>Node 2</Text>
      </View>
      {/* More nodes */}
    </View>
  );
};

const styles = StyleSheet.create({
  palette: {
    flex: 1,
    backgroundColor: '#f0f0f0',
    padding: 10,
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  node: {
    padding: 10,
    margin: 5,
    backgroundColor: '#ffffff',
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 5,
  },
});

export default NodePalette;