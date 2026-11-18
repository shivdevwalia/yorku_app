import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Lassonde Atlas | Courses & Prerequisites',
  description: 'A source-linked, degree-filtered Lassonde course catalogue and prerequisite reference map.',
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
