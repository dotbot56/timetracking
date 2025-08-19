import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';

export default function Home() {
  const router = useRouter();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  useEffect(() => {
    const stored = localStorage.getItem('user');
    if (stored) {
      router.replace('/dashboard');
    }
  }, [router]);

  const login = async () => {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    const data = await res.json();
    if (res.ok) {
      localStorage.setItem('user', JSON.stringify(data));
      router.push('/dashboard');
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
    <main style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'linear-gradient(135deg,#8A2BE2,#DA70D6)'
    }}>
      <div style={{
        background: 'white',
        padding: '2rem',
        borderRadius: '1rem',
        boxShadow: '0 4px 15px rgba(0,0,0,0.1)',
        width: '100%',
        maxWidth: '400px',
        textAlign: 'center'
      }}>
        <h1 style={{marginBottom: '1.5rem'}}>Zeit Erfassung</h1>
        <input
          style={{width: '100%', padding: '0.5rem', marginBottom: '0.5rem'}}
          value={username}
          onChange={e => setUsername(e.target.value)}
          placeholder="Benutzername"
        />
        <input
          style={{width: '100%', padding: '0.5rem', marginBottom: '0.5rem'}}
          type="password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          placeholder="Passwort"
        />
        <div style={{display: 'flex', justifyContent: 'space-between'}}>
          <button
            onClick={login}
            style={{flex: 1, marginRight: '0.5rem', padding: '0.5rem', background:'#8A2BE2', color:'white', border:'none', borderRadius:'0.5rem'}}
          >
            Login
          </button>
          <button
            onClick={register}
            style={{flex: 1, marginLeft: '0.5rem', padding: '0.5rem', background:'#DA70D6', color:'white', border:'none', borderRadius:'0.5rem'}}
          >
            Registrieren
          </button>
        </div>
        {message && <p style={{marginTop:'1rem'}}>{message}</p>}
      </div>
    </main>
  );
}
