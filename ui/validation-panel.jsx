import React, { useState } from "react";
import yaml from "js-yaml";

/**
 * ValidationPanel
 *
 * A simple UI that lets a learner paste a Kubernetes manifest (YAML),
 * validates the syntax client‑side, and shows real‑time feedback.
 *
 * Features:
 *   • Textarea for manifest input
 *   • "Validate" button (also validates on every change)
 *   • Displays parsed JSON on success
 *   • Shows error message with line/column when parsing fails
 *   • Sample manifest placeholder (Node.js + PostgreSQL)
 */
export default function ValidationPanel() {
  const [manifest, setManifest] = useState(sampleManifest);
  const [error, setError] = useState(null);
  const [parsed, setParsed] = useState(null);

  // Validate whenever the manifest changes (real‑time feedback)
  const validate = (value) => {
    try {
      const doc = yaml.loadAll(value);
      setParsed(doc);
      setError(null);
    } catch (e) {
      // js-yaml error messages already contain line/column info
      setParsed(null);
      setError(e.message);
    }
  };

  const handleChange = (e) => {
    const value = e.target.value;
    setManifest(value);
    validate(value);
  };

  const handleValidateClick = () => {
    validate(manifest);
  };

  return (
    <div style={styles.container}>
      <h2>Kubernetes Manifest Validator</h2>
      <textarea
        style={styles.textarea}
        value={manifest}
        onChange={handleChange}
        placeholder="Paste your Kubernetes YAML manifest here..."
        rows={20}
      />
      <div style={styles.actions}>
        <button onClick={handleValidateClick} style={styles.button}>
          Validate
        </button>
      </div>
      {error && (
        <pre style={styles.error}>Error: {error}</pre>
      )}
      {parsed && (
        <pre style={styles.success}>
          Parsed Manifest (JSON):
          {JSON.stringify(parsed, null, 2)}
        </pre>
      )}
    </div>
  );
}

// A minimal sample manifest (Node.js app + PostgreSQL) to help learners get started
const sampleManifest = `apiVersion: apps/v1
kind: Deployment
metadata:
  name: nodejs-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nodejs-app
  template:
    metadata:
      labels:
        app: nodejs-app
    spec:
      containers:
        - name: nodejs
          image: node:14-alpine
          ports:
            - containerPort: 3000
          env:
            - name: DATABASE_URL
              value: postgres://postgres:password@postgres-service:5432/db
---
apiVersion: v1
kind: Service
metadata:
  name: nodejs-service
spec:
  selector:
    app: nodejs-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 3000
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
        - name: postgres
          image: postgres:13
          env:
            - name: POSTGRES_PASSWORD
              value: password
          ports:
            - containerPort: 5432
---
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
spec:
  selector:
    app: postgres
  ports:
    - protocol: TCP
      port: 5432
      targetPort: 5432
`;

const styles = {
  container: {
    maxWidth: "800px",
    margin: "0 auto",
    fontFamily: "Arial, sans-serif",
  },
  textarea: {
    width: "100%",
    fontFamily: "monospace",
    fontSize: "14px",
    padding: "8px",
    border: "1px solid #ccc",
    borderRadius: "4px",
    boxSizing: "border-box",
  },
  actions: {
    marginTop: "8px",
    textAlign: "right",
  },
  button: {
    padding: "6px 12px",
    fontSize: "14px",
    cursor: "pointer",
  },
  error: {
    marginTop: "12px",
    color: "#b00020",
    backgroundColor: "#fdd",
    padding: "8px",
    borderRadius: "4px",
    whiteSpace: "pre-wrap",
  },
  success: {
    marginTop: "12px",
    color: "#006400",
    backgroundColor: "#e6ffe6",
    padding: "8px",
    borderRadius: "4px",
    whiteSpace: "pre-wrap",
  },
};