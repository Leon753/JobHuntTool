import MainFrame from './components/MainFrame'
import "./App.css";
import { RootProvider } from './context/RootContext';
import { getAuthToken, getUserEmail } from './chrome/utils';
import { useEffect, useState } from 'react';
import { UserInfo } from './helpers/types';

const getUserInfo = async () => {
  const userEmail = await getUserEmail();
  const token = await getAuthToken();
  const userInfo = await fetch(
      `http://127.0.0.1:8080/user/get-user-excel?user_id=${userEmail}`,
      {
          method: "GET",
          headers: {
              "Content-Type": 'application/json',
              "Authorization": `Bearer ${token}`
          },
      }
  );

  const userObject = await userInfo.json();
  console.log("userObject", userObject);
  return userObject;
}

function App() {
  const [userInfo, setUserInfo] = useState<UserInfo | undefined>();

  useEffect(() => {
    getUserInfo().then((res) => {
      setUserInfo(res);
    })
  }, [])
  
  return (
    <RootProvider userInfo={userInfo}>
      <div className="App">
          <MainFrame />
      </div>
    </RootProvider>
  );
}

export default App;
