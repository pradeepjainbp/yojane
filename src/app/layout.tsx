import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Yojane — Plan Before You Build',
  description:
    'An interactive construction decision simulator for India. Make informed building decisions before you pour concrete.',
  keywords: ['construction', 'india', 'building', 'simulator', 'architect', 'house'],
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="h-full">
      <body className={`${inter.className} min-h-full`} data-gramm="false" data-gramm_editor="false" data-enable-grammarly="false">{children}</body>
    </html>
  )
}
