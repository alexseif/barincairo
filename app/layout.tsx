import { Analytics } from '@vercel/analytics/next'
import type { Metadata, Viewport } from 'next'
import { Cormorant_Garamond, DM_Mono, DM_Sans } from 'next/font/google'
import './globals.css'

const serif = Cormorant_Garamond({ subsets: ['latin'], variable: '--font-serif', display: 'swap' })
const sans = DM_Sans({ subsets: ['latin'], variable: '--font-sans', display: 'swap' })
const mono = DM_Mono({ subsets: ['latin'], weight: ['400', '500'], variable: '--font-mono', display: 'swap' })

export const metadata: Metadata = {
  title: 'barincairo.com — The Downtown Cairo Nightlife Index (Wust El Balad)',
  description: 'A curated cartographic guide to historic bars, rooftop lounges, backroom spots, and after-hours institutions in Downtown Cairo (Wust El Balad), Egypt.',
  keywords: ['bar in cairo', 'bars in cairo', 'wust el balad nightlife', 'downtown cairo bars', 'rooftop bar cairo', 'cairo jazz club'],
  openGraph: {
    title: 'barincairo.com — Downtown Cairo Nightlife Index',
    description: 'A living cartographic guide to the historic establishments, rooftops, and backroom lounges of Downtown Cairo.',
    url: 'https://barincairo.com',
    siteName: 'barincairo.com',
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'barincairo.com — Downtown Cairo Nightlife Index',
    description: 'A living cartographic guide to historic bars and rooftops in Wust El Balad, Cairo.',
  },
}

export const viewport: Viewport = {
  colorScheme: 'light',
  themeColor: '#ede7d8',
  width: 'device-width',
  initialScale: 1,
}

const jsonLdSchema = {
  '@context': 'https://schema.org',
  '@type': 'ItemList',
  'name': 'Downtown Cairo Nightlife Establishments',
  'description': 'Curated index of bars, rooftops, and historic establishments in Downtown Cairo (Wust El Balad).',
  'url': 'https://barincairo.com',
  'itemListElement': [
    {
      '@type': 'ListItem',
      'position': 1,
      'item': {
        '@type': 'BarOrPub',
        'name': 'Cairo Jazz Club 610',
        'address': {
          '@type': 'PostalAddress',
          'addressLocality': 'Downtown / Wust El Balad',
          'addressCountry': 'EG',
        },
        'geo': {
          '@type': 'GeoCoordinates',
          'latitude': 30.0444,
          'longitude': 31.2357,
        },
        'priceRange': '$$',
      },
    },
    {
      '@type': 'ListItem',
      'position': 2,
      'item': {
        '@type': 'BarOrPub',
        'name': 'Vent',
        'address': {
          '@type': 'PostalAddress',
          'streetAddress': '12 El-Horeya',
          'addressLocality': 'Downtown / Wust El Balad',
          'addressCountry': 'EG',
        },
        'geo': {
          '@type': 'GeoCoordinates',
          'latitude': 30.0418,
          'longitude': 31.2392,
        },
        'priceRange': '$$',
      },
    },
    {
      '@type': 'ListItem',
      'position': 3,
      'item': {
        '@type': 'BarOrPub',
        'name': 'Horus Rooftop',
        'address': {
          '@type': 'PostalAddress',
          'streetAddress': 'Talaat Harb Square',
          'addressLocality': 'Downtown / Wust El Balad',
          'addressCountry': 'EG',
        },
        'geo': {
          '@type': 'GeoCoordinates',
          'latitude': 30.0461,
          'longitude': 31.2388,
        },
        'priceRange': '$$',
      },
    },
  ],
}

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className={`${serif.variable} ${sans.variable} ${mono.variable}`}>
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLdSchema) }}
        />
      </head>
      <body className="antialiased">
        {children}
        {process.env.NODE_ENV === 'production' && <Analytics />}
      </body>
    </html>
  )
}
