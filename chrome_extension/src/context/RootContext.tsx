import { ReactNode } from 'react';
import { createContext, useContext } from 'react';
import { UserInfo } from '../helpers/types';

const RootContext = createContext<UserInfo | undefined>(undefined);

interface Props {
    children: ReactNode
    userInfo: UserInfo | undefined
}

export function RootProvider({ children, userInfo }: Props) {

  return (
    <RootContext.Provider value={userInfo}>
      {children}
    </RootContext.Provider>
  );
}

export function useRootContext(): UserInfo | undefined {
    return useContext(RootContext);
}
