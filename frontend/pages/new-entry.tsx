import { useState } from 'react';
import { useRouter } from 'next/router';

export default function NewEntry() {
  const router = useRouter();
  const [date, setDate] = useState('');
  const [start, setStart] = useState('');
  const [end, setEnd] = useState('');
  const [travel, setTravel] = useState(0);
  const [message, setMessage] = useState('');

  const submit = async () => {
    const entry = {
      id: Date.now(),
      user_id: 1,
      site_id: 1,
      date,
      start_time: start,
      end_time: end,
      lunch_flat_applied: false,
      travel_minutes: travel,
      expenses: []
    };
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/time-entries`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(entry)
    });
    if (res.ok) {
      router.push('/dashboard');
    } else {
      const data = await res.json();
      setMessage(data.detail || 'Speichern fehlgeschlagen');
    }
  };

  return (
    <main style={{padding: '2rem'}}>
      <h1>Neue Arbeitszeit</h1>
      <div style={{display:'flex', flexDirection:'column', maxWidth:'300px'}}>
        <input type="date" value={date} onChange={e => setDate(e.target.value)} style={{marginBottom:'0.5rem'}} />
        <input type="time" value={start} onChange={e => setStart(e.target.value)} style={{marginBottom:'0.5rem'}} />
        <input type="time" value={end} onChange={e => setEnd(e.target.value)} style={{marginBottom:'0.5rem'}} />
        <input type="number" value={travel} onChange={e => setTravel(parseInt(e.target.value))} style={{marginBottom:'0.5rem'}} placeholder="Reisezeit (Minuten)" />
        <button onClick={submit} style={{padding:'0.5rem', background:'#8A2BE2', color:'white', border:'none', borderRadius:'0.5rem'}}>Speichern</button>
      </div>
      {message && <p style={{marginTop:'1rem'}}>{message}</p>}
    </main>
  );
}
