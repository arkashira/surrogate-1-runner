import React, { useState, useEffect } from "react";
import { CostEstimator } from "../services/cost_estimator";

interface PromptEditorProps {
  initialPrompt: string;
  modelName: string;
}

const PromptEditor: React.FC<PromptEditorProps> = ({ initialPrompt, modelName }) => {
  const [prompt, setPrompt] = useState(initialPrompt);
  const [cost, setCost] = useState<number | null>(null);
  const costEstimator = new CostEstimator(modelName);

  useEffect(() => {
    const estimatedCost = costEstimator.estimate_cost(prompt, modelName);
    setCost(estimatedCost);
  }, [prompt, modelName]);

  const handlePromptChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setPrompt(event.target.value);
  };

  return (
    <div>
      <textarea value={prompt} onChange={handlePromptChange} />
      {cost !== null && <p>Estimated cost: ${cost.toFixed(6)}</p>}
    </div>
  );
};

export default PromptEditor;