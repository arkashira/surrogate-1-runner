import React, { createContext, useContext, useState } from 'react';

interface SurrogateContextType {
  surrogateYaml: string;
  setSurrogateYaml: (yaml: string) => void;
}

const SurrogateContext = createContext<SurrogateContextType | undefined>(undefined);

export const SurrogateProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [surrogateYaml, setSurrogateYaml] = useState('');

  return (
    <SurrogateContext.Provider value={{ surrogateYaml, setSurrogateYaml }}>
      {children}
    </SurrogateContext.Provider>
  );
};

export const useSurrogateContext = () => {
  const context = useContext(SurrogateContext);
  if (!context) {
    throw new Error('useSurrogateContext must be used within a SurrogateProvider');
  }
  return context;
};