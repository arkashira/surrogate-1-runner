import telemetry from './services/Telemetry';

// Initialize telemetry
telemetry.start();

// Example usage:
telemetry.suggestionRequested({ suggestionId: '123' });
telemetry.suggestionAccepted({ suggestionId: '123', timeTaken: 5000 });
telemetry.suggestionRejected({ suggestionId: '123', reason: 'not_relevant' });