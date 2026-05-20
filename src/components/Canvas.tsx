import React, { useRef, useState } from 'react';
import { View, PanResponder, Animated, StyleSheet, Dimensions, TouchableOpacity, Text } from 'react-native';
import { PinchGestureHandler } from 'react-native-gesture-handler';

const { width, height } = Dimensions.get('window');

const Canvas = () => {
  const [nodes, setNodes] = useState([]);
  const [scale, setScale] = useState(new Animated.Value(1));
  const [translateX, setTranslateX] = useState(new Animated.Value(0));
  const [translateY, setTranslateY] = useState(new Animated.Value(0));

  const panResponder = useRef(
    PanResponder.create({
      onMoveShouldSetPanResponder: (evt, gestureState) => {
        return Math.abs(gestureState.dx) > 10 || Math.abs(gestureState.dy) > 10;
      },
      onPanResponderMove: (evt, gestureState) => {
        translateX.setValue(gestureState.dx);
        translateY.setValue(gestureState.dy);
      },
      onPanResponderRelease: () => {
        translateX.setValue(0);
        translateY.setValue(0);
      },
    })
  ).current;

  const handleLongPress = (event) => {
    const newNode = {
      id: Date.now(),
      position: { x: event.nativeEvent.locationX, y: event.nativeEvent.locationY },
    };
    setNodes([...nodes, newNode]);
  };

  return (
    <View style={styles.container}>
      <PinchGestureHandler onGestureEvent={(event) => setScale(new Animated.Value(event.nativeEvent.scale))}>
        <Animated.View
          style={{
            transform: [
              { scale: scale },
              { translateX: translateX },
              { translateY: translateY },
            ],
          }}
          {...panResponder.panHandlers}
        >
          {nodes.map((node) => (
            <TouchableOpacity key={node.id} style={[styles.node, { left: node.position.x, top: node.position.y }]}>
              <Text>Node</Text>
            </TouchableOpacity>
          ))}
        </Animated.View>
      </PinchGestureHandler>
      <TouchableOpacity onLongPress={handleLongPress} style={styles.palette}>
        <Text>Add Node</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff',
  },
  node: {
    position: 'absolute',
    padding: 10,
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#000',
    borderRadius: 5,
  },
  palette: {
    position: 'absolute',
    bottom: 20,
    left: 20,
    padding: 10,
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#000',
    borderRadius: 5,
  },
});

export default Canvas;