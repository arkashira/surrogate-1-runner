import React, { createContext, useState, useEffect, ReactNode } from 'react';

type AuthContextType = {
  isAuthenticated: boolean;
  user: { name: string } | null;
};

export const AuthContext = createContext<AuthContextType>({
  isAuthenticated: false,
  user: null,
});

type Props = { children: ReactNode };

export const AuthProvider = ({ children }: Props) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<{ name: string } | null>(null);

  // 👉 Replace this mock logic with your real auth check (e.g. JWT, OAuth, etc.)
  useEffect(() => {
    const token = localStorage.getItem('authToken');
    if (token) {
      setIsAuthenticated(true);
      setUser({ name: 'Demo User' });
    }
  }, []);

  return (
    <AuthContext.Provider value={{ isAuthenticated, user }}>
      {children}
    </AuthContext.Provider>
  );
};