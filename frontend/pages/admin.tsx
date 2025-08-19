import { useEffect, useState } from 'react';

interface PendingUser {
  username: string;
}

export default function Admin() {
  const [pending, setPending] = useState<PendingUser[]>([]);
  const [role, setRole] = useState<Record<string, string>>({});
  const [message, setMessage] = useState('');

  const load = () => {
    fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/users/pending`)
      .then(res => res.json())
      .then(setPending);
  };

  useEffect(() => {
    load();
  }, []);

  const approve = async (username: string) => {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/users/approve`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, role: role[username] || 'mitarbeiter' })
    });
    if (res.ok) {
      setMessage(`${username} freigeschaltet`);
      load();
    } else {
      const data = await res.json();
      setMessage(data.detail || 'Fehler bei Freigabe');
    }
  };

  return (
    <main>
      <h1>Admin</h1>
      {message && <p>{message}</p>}
      <ul>
        {pending.map(u => (
          <li key={u.username}>
            {u.username}
            <select value={role[u.username] || 'mitarbeiter'} onChange={e => setRole({ ...role, [u.username]: e.target.value })}>
              <option value="admin">admin</option>
              <option value="vorgesetzter">vorgesetzter</option>
              <option value="mitarbeiter">mitarbeiter</option>
            </select>
            <button onClick={() => approve(u.username)}>Freigeben</button>
          </li>
        ))}
      </ul>
    </main>
  );
}
