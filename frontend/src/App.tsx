import React, { useEffect, useMemo, useState } from 'react';
import './App.css';
import { ApiClient } from './ApiClient';
import { Login } from './Login';
import { StravaDashboard } from './StravaDashboard';
import { User } from './Types';
import { NavBar } from './NavBar';

function App() {
  const client = useMemo(() => ApiClient(), []);
  const [user, setUser] = useState<User | undefined>();
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    client.get("auth/").then(r => {
      setUser(r.data);
      setLoading(false);
    }).catch(err => {
      setUser(undefined);
      setLoading(false);
    });
  }, []);

  return (
    <div className="App">
      {loading ?
        <div id="loading" />
        :
        user ?
          <div>
            <NavBar user={user} setUser={setUser}></NavBar>
            <StravaDashboard />
          </div>
          :
          <Login/>
      }
    </div>
  );
}

export default App;
