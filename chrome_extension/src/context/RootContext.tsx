import { ReactNode } from 'react';
import { createContext, useContext } from 'react';

const RootContext = createContext(false);

interface Props {
    children: ReactNode
    value: boolean
}

export function RootProvider({ children, value }: Props) {

  return (
    <RootContext.Provider value={value}>
      {children}
    </RootContext.Provider>
  );

}

export function useRootContext(): boolean {
    return useContext(RootContext);
}
