import React, { createContext, useState, useEffect, ReactNode } from 'react';

export interface User {
  id: string;
  roles: string[];          // e.g. ['viewer', 'editor', 'admin']
}

export const UserContext = createContext<{ user: User | null }>({ user: null });

export const UserProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    // Replace this with your real auth‑fetch logic
    const fetchUser = async () => {
      const mock: User = { id: '123', roles: ['viewer', 'editor'] };
      setUser(mock);
    };
    fetchUser();
  }, []);

  return <UserContext.Provider value={{ user }}>{children}</UserContext.Provider>;
};