import React, { useRef, useEffect, useState, useCallback } from 'react';
import PropTypes from 'prop-types';
import MonacoEditor from 'react-monaco-editor';
import { validatePipeline } from '../services/validation';
import ValidationBadge from './ValidationBadge';
import './CodeEditor.css';

/**
 * CodeEditor component that validates pipeline.yaml on save and
 * displays inline markers and a validation badge.
 *
 * @param {Object} props
 * @param {string} props.value - The current editor content.
 * @param {function} props.onChange - Callback when content changes.
 */
export default function CodeEditor({ value, onChange }) {
  const editorRef = useRef(null);
  const [validation, setValidation] = useState({ errors: [], warnings: [] });
  const [decorations, setDecorations] = useState([]);

  // Debounced validation trigger
  const debounceTimer = useRef(null);
  const runValidation = useCallback(
    async (content) => {
      const result = await validatePipeline(content);
      setValidation(result);

      // Prepare Monaco decorations
      const newDecorations = [
        ...result.errors.map((e) => ({
          range: new window.monaco.Range(e.lineNumber, e.column, e.lineNumber, e.column + 5),
          options: { isWholeLine: false, className: 'validation-error', glyphMarginClassName: 'validation-error-glyph' },
        })),
        ...result.warnings.map((w) => ({
          range: new window.monaco.Range(w.lineNumber, w.column, w.lineNumber, w.column + 5),
          options: { isWholeLine: false, className: 'validation-warning', glyphMarginClassName: 'validation-warning-glyph' },
        })),
      ];

      const editor = editorRef.current?.editor;
      if (editor) {
        const newDecos = editor.deltaDecorations(decorations, newDecorations);
        setDecorations(newDecos);
      }
    },
    [decorations]
  );

  useEffect(() => {
    // Trigger validation after user stops typing for 500ms
    if (debounceTimer.current) clearTimeout(debounceTimer.current);
    debounceTimer.current = setTimeout(() => {
      runValidation(value);
    }, 500);

    return () => {
      if (debounceTimer.current) clearTimeout(debounceTimer.current);
    };
  }, [value, runValidation]);

  const editorDidMount = (editor) => {
    editorRef.current = { editor };
  };

  const handleEditorChange = (newValue) => {
    onChange(newValue);
  };

  const isValid = validation.errors.length === 0;

  return (
    <div className="code-editor-container">
      <div className="editor-header">
        <span>pipeline.yaml</span>
        <ValidationBadge isValid={isValid} />
      </div>
      <MonacoEditor
        width="100%"
        height="500"
        language="yaml"
        theme="vs-dark"
        value={value}
        options={{
          automaticLayout: true,
          glyphMargin: true,
          lineNumbers: 'on',
        }}
        onChange={handleEditorChange}
        editorDidMount={editorDidMount}
      />
    </div>
  );
}

CodeEditor.propTypes = {
  value: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired,
};