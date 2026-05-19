import React, { createContext, useContext, useEffect, useRef, useState } from 'react';
import { ServerEvent } from './types';

interface WSContextProps {
  socket: WebSocket | null;
  isConnected: boolean;
  sendMessage: (msg: any) => void;
  lastMessage: MessageEvent | null;
}

const WSContext = createContext<WSContextProps | undefined>(undefined);

export const WebSocketProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<MessageEvent | null>(null);

  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const ws = new WebSocket(process.env.REACT_APP_WS_URL ?? 'ws://localhost:8080');
    wsRef.current = ws;

    ws.onopen = () => setIsConnected(true);
    ws.onclose = () => setIsConnected(false);
    ws.onerror = () => setIsConnected(false);

    ws.onmessage = (msg) => setLastMessage(msg);

    setSocket(ws);

    return () => {
      ws.close();
      setSocket(null);
    };
  }, []);

  const sendMessage = (msg: any) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(msg));
    }
  };

  return (
    <WSContext.Provider value={{ socket, isConnected, sendMessage, lastMessage }}>
      {children}
    </WSContext.Provider>
  );
};

export const useWebSocket = () => {
  const ctx = useContext(WSContext);
  if (!ctx) throw new Error('useWebSocket must be used within a WebSocketProvider');
  return ctx;
};