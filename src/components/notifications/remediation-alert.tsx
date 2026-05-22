import React from 'react';
import { Alert, AlertTitle, AlertDescription } from '@/components/ui/alert';

interface RemediationAlertProps {
  title: string;
  description: string;
  type: 'info' | 'warning' | 'error' | 'success';
  onClose?: () => void;
  timestamp?: string; // Added for better context
  actionDetails?: {
    resourceId: string;
    policyName: string;
  }; // Added for additional context
}

export const RemediationAlert: React.FC<RemediationAlertProps> = ({
  title,
  description,
  type = 'info',
  onClose,
  timestamp,
  actionDetails
}) => {
  const alertTypeClasses = {
    info: 'border-blue-500 bg-blue-50 text-blue-800',
    warning: 'border-yellow-500 bg-yellow-50 text-yellow-800',
    error: 'border-red-500 bg-red-50 text-red-800',
    success: 'border-green-500 bg-green-50 text-green-800'
  };

  return (
    <Alert className={`relative border-l-4 p-4 rounded-md ${alertTypeClasses[type]}`}>
      <AlertTitle className="font-bold">{title}</AlertTitle>
      <AlertDescription className="mt-2">
        {description}
        {timestamp && <div className="mt-1 text-xs text-gray-500">Occurred at: {timestamp}</div>}
        {actionDetails && (
          <div className="mt-1 text-xs">
            <div>Resource: {actionDetails.resourceId}</div>
            <div>Policy: {actionDetails.policyName}</div>
          </div>
        )}
      </AlertDescription>
      {onClose && (
        <button
          onClick={onClose}
          className="absolute top-2 right-2 text-current hover:text-gray-500"
          aria-label="Close alert"
        >
          ✕
        </button>
      )}
    </Alert>
  );
};