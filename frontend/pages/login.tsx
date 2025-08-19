import { useState } from 'react';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const login = async () => {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    const data = await res.json();
    if (res.ok) {
      setMessage(`Angemeldet als ${data.username} (${data.role})`);
    } else {
      setMessage(data.detail || 'Login fehlgeschlagen');
    }
  };

  const register = async () => {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    if (res.ok) {
      setMessage('Registriert. Bitte auf Freigabe warten.');
    } else {
      const data = await res.json();
      setMessage(data.detail || 'Registrierung fehlgeschlagen');
    }
  };

  return (
    <main>
      <h1>Login</h1>
      <input value={username} onChange={e => setUsername(e.target.value)} placeholder="Benutzername" />
      <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Passwort" />
      <div>
        <button onClick={login}>Login</button>
        <button onClick={register}>Registrieren</button>
      </div>
      {message && <p>{message}</p>}
    </main>
  );
}
