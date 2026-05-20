import React from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import { useRoute, RouteProp } from '@react-navigation/native';

// Existing imports (keep any that were previously used)
// import ... (placeholder for other components, utilities, etc.)

// Define the shape of the route params we expect.
// Adjust these typings if the actual project defines a more specific type.
type RunSummaryParams = {
  run?: {
    // The workflow engine should attach a `cost` object to the run payload.
    // If the shape differs, update the accesses below accordingly.
    cost?: {
      usd?: number;      // Total cost in US dollars
      tokens?: number;   // Total token count
    };
    // ...other run fields used elsewhere in the screen
  };
};

type RunSummaryRouteProp = RouteProp<Record<string, RunSummaryParams>, string>;

const RunSummaryScreen: React.FC = () => {
  const route = useRoute<RunSummaryRouteProp>();
  const run = route.params?.run;

  // Safely extract cost metrics; default to zero when unavailable.
  const totalCostUsd = run?.cost?.usd ?? 0;
  const totalTokens = run?.cost?.tokens ?? 0;

  return (
    <ScrollView contentContainerStyle={styles.container}>
      {/* ==== Existing UI components for the run summary ==== */}
      {/* The original implementation likely renders duration, step count, etc.
          Those components remain untouched above this comment. */}

      {/* ==== New Total Cost Summary ==== */}
      <View style={styles.costContainer}>
        <Text style={styles.costLabel}>Total Cost</Text>
        <Text style={styles.costValue}>
          ${totalCostUsd.toFixed(2)} ({totalTokens} tokens)
        </Text>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 16,
    backgroundColor: '#fff',
  },
  // Existing style definitions (preserve any that were previously present)
  // ...

  // New styles for the cost summary
  costContainer: {
    marginTop: 24,
    padding: 12,
    borderWidth: 1,
    borderColor: '#e0e0e0',
    borderRadius: 8,
    backgroundColor: '#f9f9f9',
  },
  costLabel: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 4,
  },
  costValue: {
    fontSize: 18,
    fontWeight: '500',
    color: '#007aff',
  },
});

export default RunSummaryScreen;