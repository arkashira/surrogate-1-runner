import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, Alert, StyleSheet } from 'react-native';

const NodeItem = ({ node, onDelete, onSave }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [nodeName, setNodeName] = useState(node.name);

  const handleDelete = () => {
    Alert.alert(
      'Confirm Delete',
      'Are you sure you want to delete this node?',
      [
        { text: 'Cancel', style: 'cancel' },
        { text: 'OK', onPress: () => onDelete(node.id) },
      ],
      { cancelable: false }
    );
  };

  const handleSave = () => {
    onSave(node.id, nodeName);
    setIsEditing(false);
  };

  return (
    <View style={styles.container}>
      {isEditing ? (
        <TextInput
          style={styles.input}
          value={nodeName}
          onChangeText={setNodeName}
          onBlur={handleSave}
          autoFocus
        />
      ) : (
        <TouchableOpacity onPress={() => setIsEditing(true)}>
          <Text style={styles.nodeName}>{nodeName}</Text>
        </TouchableOpacity>
      )}
      <TouchableOpacity onPress={handleDelete} style={styles.deleteButton}>
        <Text style={styles.deleteText}>Delete</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#ccc',
  },
  input: {
    flex: 1,
    borderColor: 'gray',
    borderWidth: 1,
    padding: 5,
    marginRight: 10,
  },
  nodeName: {
    fontSize: 16,
    flex: 1,
  },
  deleteButton: {
    padding: 5,
  },
  deleteText: {
    color: 'red',
  },
});

export default NodeItem;