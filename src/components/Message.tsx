import React, { useState, useEffect, useRef } from 'react';
import { useWebview } from '@axentx/ide-assistant-webview';
import './Message.css';

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  isStreaming?: boolean;   // true while the assistant is still typing
  timestamp?: number;
}

interface Props {
  message: Message;
  onStreamingComplete?: (id: string) => void;
}

export const Message: React.FC<Props> = ({
  message,
  onStreamingComplete,
}) => {
  const { aiResponse } = useWebview();          // token array from the webview
  const [displayed, setDisplayed] = useState(message.content);
  const [isLoading, setIsLoading] = useState(message.isStreaming ?? false);
  const [streamed, setStreamed] = useState('');
  const contentRef = useRef<HTMLDivElement>(null);

  /* ----------  Streaming logic  ---------- */
  useEffect(() => {
    if (!message.isStreaming) return;          // static message – nothing to stream

    // If the webview already sent us a token array, use it.
    // Otherwise fall back to the content string (useful for demos).
    const tokens = Array.isArray(aiResponse) ? aiResponse : message.content.split('');

    let idx = 0;
    const interval = setInterval(() => {
      if (idx < tokens.length) {
        const next = tokens[idx];
        const newText = streamed + next;
        setStreamed(newText);
        setDisplayed(newText);
        idx++;

        // Auto‑scroll as text grows
        if (contentRef.current) {
          contentRef.current.scrollTop = contentRef.current.scrollHeight;
        }
      } else {
        clearInterval(interval);
        setIsLoading(false);
        onStreamingComplete?.(message.id);
      }
    }, 20); // ~50 tokens/s

    return () => clearInterval(interval);
  }, [message.isStreaming, aiResponse, message.id, onStreamingComplete]);

  /* ----------  Rendering  ---------- */
  const isUser = message.role === 'user';
  const avatar = isUser ? '👤' : '🤖';

  return (
    <div
      className={`message ${isUser ? 'message-user' : 'message-assistant'} ${
        message.isStreaming ? 'message-streaming' : ''
      }`}
      data-message-id={message.id}
    >
      <div className="message-avatar">{avatar}</div>

      <div className="message-content-wrapper">
        {isLoading && !streamed && (
          <div className="message-loading">
            <span className="loading-dot" />
            <span className="loading-dot" />
            <span className="loading-dot" />
          </div>
        )}

        <div
          ref={contentRef}
          className="message-content"
          dangerouslySetInnerHTML={{ __html: formatContent(displayed) }}
        />

        {message.isStreaming && <span className="streaming-cursor">▊</span>}
      </div>
    </div>
  );
};

/* ----------  Markdown‑style formatter  ---------- */
function formatContent(content: string): string {
  return content
    // code fences
    .replace(
      /