import './globals.css';
import { ReactNode } from 'react';

export const metadata = { title: 'Time Tracking' };

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="de">
      <body style={{margin:0}}>{children}</body>
    </html>
  );
}
