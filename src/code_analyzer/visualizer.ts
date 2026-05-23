import { ParserConflict } from '../types';

interface ConflictVisualizationProps {
  conflicts: ParserConflict[];
}

const ConflictVisualization: React.FC<ConflictVisualizationProps> = ({ conflicts }) => {
  return (
    <div>
      {conflicts.map((conflict, index) => (
        <div key={index}>
          <h3>Conflict at Line {conflict.line}</h3>
          <p>{conflict.message}</p>
          <button onClick={() => handleMitigation(conflict, 'Use Vercel SDK parser')}>Use Vercel SDK parser</button>
          <button onClick={() => handleMitigation(conflict, 'Remove redundant parser')}>Remove redundant parser</button>
          {/* Add more mitigation options as needed */}
        </div>
      ))}
    </div>
  );
};

const handleMitigation = (conflict: ParserConflict, option: string) => {
  // Implement mitigation logic here
  console.log(`Applying mitigation: ${option} for conflict at line ${conflict.line}`);
};

export default ConflictVisualization;