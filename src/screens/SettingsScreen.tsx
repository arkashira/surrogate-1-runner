import React, { useContext, useState } from 'react';
import { View, Switch, Text, StyleSheet } from 'react-native';
import { AppContext } from '../context/AppContext';
import { syncWorkflow, getSyncStatus } from '../services/syncService';

const SettingsScreen = () => {
  const { passcode } = useContext(AppContext);
  const [isSyncEnabled, setIsSyncEnabled] = useState(getSyncStatus(passcode)?.enabled || false);
  const [syncStatus, setSyncStatus] = useState(getSyncStatus(passcode));

  const toggleSync = async () => {
    setIsSyncEnabled(!isSyncEnabled);
    await syncWorkflow(passcode, !isSyncEnabled);
    setSyncStatus(getSyncStatus(passcode));
  };

  return (
    <View style={styles.container}>
      <View style={styles.row}>
        <Text style={styles.label}>Sync Workflows</Text>
        <Switch value={isSyncEnabled} onValueChange={toggleSync} />
      </View>
      {syncStatus && (
        <View style={styles.row}>
          <Text style={styles.label}>Last Backup:</Text>
          <Text style={styles.value}>{new Date(syncStatus.lastBackup).toLocaleString()}</Text>
        </View>
      )}
      {syncStatus && (
        <View style={styles.row}>
          <Text style={styles.label}>Size:</Text>
          <Text style={styles.value}>{syncStatus.size} bytes</Text>
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 16,
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  label: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  value: {
    fontSize: 16,
  },
});

export default SettingsScreen;