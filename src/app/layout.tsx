import './globals.css'
import '@/lib/fontawesome' // Initialize FontAwesome
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Psychological Journey - AI-Powered Self Assessment',
  description: 'An immersive psychological self-assessment website with personalized AI insights for anxiety, OCD, anger management, and general wellbeing.',
  keywords: 'psychology, mental health, self-assessment, AI, therapy, anxiety, OCD, anger management, wellbeing',
  authors: [{ name: 'Psychological Journey Team' }],
  viewport: 'width=device-width, initial-scale=1',
  robots: 'index, follow',
  openGraph: {
    title: 'Psychological Journey - AI-Powered Self Assessment',
    description: 'Discover personalized insights about your mental health through an immersive assessment journey.',
    type: 'website',
    locale: 'en_US',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="scroll-smooth">
      <body className={`${inter.className} antialiased`}>
        <div className="min-h-screen bg-gradient-to-br from-calm-50 to-primary-50">
          {children}
        </div>
      </body>
    </html>
  )
}
