import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

/**
 * Provides the currently‑authenticated user (if any) to the component tree.
 * The backend must expose `/api/auth/check` that returns `{ user: { id, token, … } }`
 * and set an httpOnly cookie for session persistence.
 */
export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [authLoading, setAuthLoading] = useState(true);
  const [authError, setAuthError] = useState(null);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const { data } = await axios.get('/api/auth/check', {
          withCredentials: true, // send httpOnly cookie
        });
        setCurrentUser(data.user);
        setAuthError(null);
      } catch (err) {
        console.error('Auth check failed:', err);
        setCurrentUser(null);
        setAuthError(err.message);
      } finally {
        setAuthLoading(false);
      }
    };
    checkAuth();
  }, []);

  return (
    <AuthContext.Provider value={{ currentUser, authLoading, authError }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);