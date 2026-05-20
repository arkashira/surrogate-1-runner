import React, { createContext, useContext, useState, ReactNode, useCallback, useRef } from 'react';

export type FeedbackType = 'info' | 'success' | 'error' | 'warning';

export interface FeedbackMessage {
  id: number;
  type: FeedbackType;
  text: string;
  ttl?: number; // milliseconds before auto-dismiss (default: 5000)
}

interface FeedbackContextValue {
  addMessage: (msg: Omit<FeedbackMessage, 'id'>) => void;
  removeMessage: (id: number) => void;
  messages: FeedbackMessage[];
}

const FeedbackContext = createContext<FeedbackContextValue | undefined>(undefined);

export const useFeedback = (): FeedbackContextValue => {
  const ctx = useContext(FeedbackContext);
  if (!ctx) {
    throw new Error('useFeedback must be used within a FeedbackProvider');
  }
  return ctx;
};

export const FeedbackProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [messages, setMessages] = useState<FeedbackMessage[]>([]);
  const nextIdRef = useRef(0);

  const addMessage = useCallback((msg: Omit<FeedbackMessage, 'id'>) => {
    const id = nextIdRef.current++;
    const ttl = msg.ttl ?? 5000; // Default 5 seconds
    setMessages(prev => [...prev, { ...msg, id }]);

    if (ttl > 0) {
      setTimeout(() => {
        setMessages(prev => prev.filter(m => m.id !== id));
      }, ttl);
    }
  }, []);

  const removeMessage = useCallback((id: number) => {
    setMessages(prev => prev.filter(m => m.id !== id));
  }, []);

  return (
    <FeedbackContext.Provider value={{ addMessage, removeMessage, messages }}>
      {children}
    </FeedbackContext.Provider>
  );
};

// FeedbackToast.tsx
import React from 'react';
import { FeedbackMessage, useFeedback } from './FeedbackContext';
import './FeedbackToast.css';

const Toast: React.FC<{ msg: FeedbackMessage }> = ({ msg }) => {
  const { removeMessage } = useFeedback();
  return (
    <div className={`toast toast-${msg.type}`} role="alert" aria-live="assertive">
      <span>{msg.text}</span>
      <button
        className="toast-close"
        aria-label="Dismiss"
        onClick={() => removeMessage(msg.id)}
      >
        ×
      </button>
    </div>
  );
};

export const FeedbackToastContainer: React.FC = () => {
  const { messages } = useFeedback();
  return (
    <div className="toast-container" data-testid="toast-container">
      {messages.map(msg => (
        <Toast key={msg.id} msg={msg} />
      ))}
    </div>
  );
};

// useAuthFeedback.ts
import { useCallback } from 'react';
import { useFeedback, FeedbackType } from './FeedbackContext';

export const useAuthFeedback = () => {
  const { addMessage } = useFeedback();

  const onLoginSuccess = useCallback(() => {
    addMessage({
      type: 'success',
      text: 'Authentication successful. Welcome!',
    });
  }, [addMessage]);

  const onLoginError = useCallback((err?: unknown) => {
    const msg = err instanceof Error ? err.message : 'Authentication failed.';
    addMessage({
      type: 'error',
      text: msg,
    });
  }, [addMessage]);

  const onLogout = useCallback(() => {
    addMessage({
      type: 'info',
      text: 'You have been logged out.',
    });
  }, [addMessage]);

  const onSessionExpired = useCallback(() => {
    addMessage({
      type: 'warning',
      text: 'Your session has expired. Please log in again.',
    });
  }, [addMessage]);

  return { onLoginSuccess, onLoginError, onLogout, onSessionExpired };
};

// FeedbackToast.css
.toast-container {
  position: fixed;
  top: 1rem;
  right: 1rem;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.toast {
  min-width: 250px;
  padding: 0.75rem 1rem;
  border-radius: 4px;
  color: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
  font-family: sans-serif;
}

.toast-info { background: #2196F3; }
.toast-success { background: #4CAF50; }
.toast-error { background: #F44336; }
.toast-warning { background: #FF9800; }

.toast-close {
  background: transparent;
  border: none;
  color: inherit;
  font-size: 1.2rem;
  cursor: pointer;
}

// index.ts
export {
  FeedbackProvider,
  useFeedback,
  FeedbackMessage,
  FeedbackType,
} from './FeedbackContext';
export { FeedbackToastContainer } from './FeedbackToast';
export { useAuthFeedback } from './useAuthFeedback';