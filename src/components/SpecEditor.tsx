import React, { useState } from 'react';
import { Button, Collapse, Alert, Badge } from '@axentx/ui';
import { useSpecPreview } from '../hooks/useSpecPreview';

interface SpecSection {
  id: string;
  title: string;
  content: string;
  hasWarning?: boolean;
  warningMessage?: string;
}

interface PreviewResult {
  sections: SpecSection[];
  hasHallucinations: boolean;
  totalWarnings: number;
}

export const SpecEditor: React.FC = () => {
  const [isPreviewOpen, setIsPreviewOpen] = useState(false);
  const [previewResult, setPreviewResult] = useState<PreviewResult | null>(null);
  
  const { runPreview, loading } = useSpecPreview();

  const handleRunPreview = async () => {
    setIsPreviewOpen(true);
    const result = await runPreview();
    setPreviewResult(result);
  };

  const sections: SpecSection[] = [
    {
      id: '1',
      title: 'Model Configuration',
      content: 'This section describes the model parameters and configuration.',
      hasWarning: previewResult?.hasHallucinations,
      warningMessage: 'Potential hallucination detected in model specifications'
    },
    {
      id: '2',
      title: 'Dataset Requirements',
      content: 'The dataset should contain specific features and labels.',
      hasWarning: previewResult?.hasHallucinations,
      warningMessage: 'Dataset requirements may be incomplete or inconsistent'
    },
    {
      id: '3',
      title: 'Training Parameters',
      content: 'Training will use batch size 32 and learning rate 0.001.',
      hasWarning: previewResult?.hasHallucinations,
      warningMessage: 'Training parameters may not be optimal for the task'
    }
  ];

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-bold">Model Specification</h2>
        <Button 
          onClick={handleRunPreview}
          disabled={loading}
        >
          {loading ? 'Previewing...' : 'Run Preview'}
        </Button>
      </div>

      <div className="space-y-3">
        {sections.map((section) => (
          <div key={section.id} className="border rounded-lg p-4">
            <div className="flex justify-between items-start">
              <h3 className="font-semibold">{section.title}</h3>
              {section.hasWarning && (
                <Badge variant="warning">
                  {section.warningMessage}
                </Badge>
              )}
            </div>
            <p className="mt-2 text-gray-600">{section.content}</p>
          </div>
        ))}
      </div>

      <Collapse in={isPreviewOpen} onChange={setIsPreviewOpen}>
        <div className="border rounded-lg p-4 bg-gray-50">
          <h3 className="font-semibold mb-3">Preview Results</h3>
          {previewResult?.hasHallucinations ? (
            <Alert variant="warning">
              <p>Warning: The model specification contains potential hallucinations or inconsistencies.</p>
              <p className="mt-2">Review the highlighted sections carefully before finalizing.</p>
            </Alert>
          ) : (
            <p className="text-green-600">No hallucinations detected in the model specification.</p>
          )}
          <div className="mt-3">
            <p>Total sections reviewed: {sections.length}</p>
            <p>Total warnings: {previewResult?.totalWarnings || 0}</p>
          </div>
        </div>
      </Collapse>
    </div>
  );
};

export default SpecEditor;