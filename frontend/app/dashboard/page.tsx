'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

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

export default function Dashboard() {
  const router = useRouter();
  const [weekly, setWeekly] = useState(0);
  const [monthly, setMonthly] = useState(0);

  useEffect(() => {
    const stored = localStorage.getItem('user');
    if (!stored) {
      router.replace('/');
      return;
    }
    fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/time-entries`)
      .then(res => res.json())
      .then((entries: TimeEntry[]) => {
        const now = new Date();
        const weekStart = new Date(now);
        const day = now.getDay() === 0 ? 7 : now.getDay();
        weekStart.setDate(now.getDate() - day + 1); // Monday first
        const monthStart = new Date(now.getFullYear(), now.getMonth(), 1);
        let week = 0;
        let month = 0;
        entries.forEach(e => {
          const start = new Date(`${e.date}T${e.start_time}`);
          const end = new Date(`${e.date}T${e.end_time}`);
          const hours = (end.getTime() - start.getTime()) / (1000 * 60 * 60);
          const d = new Date(e.date);
          if (d >= weekStart) week += hours;
          if (d >= monthStart) month += hours;
        });
        setWeekly(week);
        setMonthly(month);
      });
  }, [router]);

  return (
    <main style={{padding: '2rem'}}>
      <h1>Dashboard</h1>
      <p>Diese Woche: {weekly.toFixed(2)} h</p>
      <p>Diesen Monat: {monthly.toFixed(2)} h</p>
      <button
        style={{marginTop: '2rem', padding: '0.75rem 1rem', background:'#8A2BE2', color:'white', border:'none', borderRadius:'0.5rem'}}
        onClick={() => router.push('/new-entry')}
      >
        Neue Arbeitszeit erfassen
      </button>
    </main>
  );
}
