import React from 'react';
import { Message } from '../store/chatStore';

interface ChatMessageProps {
  message: Message;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isStreaming = selectors.useIsStreaming();
  const isLoadingFirstToken = selectors.useIsLoadingFirstToken();
  const currentStreamingMessage = selectors.useCurrentStreamingMessage();

  const isCurrentlyStreaming = 
    isStreaming && 
    currentStreamingMessage?.id === message.id;

  return (
    <div className={`chat-message chat-message-${message.role}`}>
      <div className="message-header">
        <span className="message-role">{message.role === 'user' ? 'You' : 'AI'}</span>
        <span className="message-timestamp">
          {new Date(message.timestamp).toLocaleTimeString()}
        </span>
      </div>
      <div className="message-content">
        {message.content}
        {isCurrentlyStreaming && (
          <span className="streaming-cursor">▊</span>
        )}
      </div>
      {isCurrentlyStreaming && isLoadingFirstToken && (
        <div className="loading-indicator">
          <span className="loading-dot">.</span>
          <span className="loading-dot">.</span>
          <span className="loading-dot">.</span>
        </div>
      )}
    </div>
  );
};