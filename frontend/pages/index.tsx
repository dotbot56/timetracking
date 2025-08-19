import { useEffect, useState } from 'react';

interface TimeEntry {
  id: number;
  user_id: number;
  site_id: number;
  date: string;
  start_time: string;
  end_time: string;
  lunch_flat_applied: boolean;
  travel_minutes: number;
}

export default function Home() {
  const [entries, setEntries] = useState<TimeEntry[]>([]);
  const [error, setError] = useState(false);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/time-entries`)
      .then(res => res.json())
      .then(setEntries)
      .catch(() => {
        setError(true);
        setEntries([]);
      });
  }, []);

  return (
    <main>
      <h1>Time Entries</h1>
      {error && <p>Backend nicht erreichbar</p>}
      <ul>
        {entries.map(e => (
          <li key={e.id}>
            {e.date}: {e.start_time} - {e.end_time} (travel {e.travel_minutes} min)
          </li>
        ))}
      </ul>
    </main>
  );
}
