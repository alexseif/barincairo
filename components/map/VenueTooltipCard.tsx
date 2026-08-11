'use client'

import { ArrowUpRight, MapPin, Tag, X } from 'lucide-react'
import type { GeoJSONFeature } from '@/lib/api'

interface VenueTooltipCardProps {
  venue: GeoJSONFeature
  onClose: () => void
}

export default function VenueTooltipCard({ venue, onClose }: VenueTooltipCardProps) {
  const p = venue.properties
  const [lng, lat] = venue.geometry.coordinates

  return (
    <div className="absolute bottom-4 left-4 right-4 z-30 max-w-md border-2 border-[#24332d] bg-[#ede7d8] p-5 shadow-[4px_4px_0px_#24332d] sm:bottom-6 sm:left-auto sm:right-6 sm:w-96">
      {/* Top Header Bar */}
      <div className="mb-3 flex items-start justify-between border-b border-[#24332d]/20 pb-2">
        <div>
          <span className="font-mono text-[9px] uppercase tracking-[0.22em] text-[#ad793b]">
            {p.category_name || 'Historic Venue'}
          </span>
          <h3 className="font-serif text-xl font-bold tracking-tight text-[#24332d]">
            {p.name_en}
          </h3>
          <p className="font-serif text-sm text-[#24332d]/80" lang="ar" dir="rtl">
            {p.name_ar}
          </p>
        </div>
        <button
          onClick={onClose}
          className="flex h-11 w-11 items-center justify-center border border-[#24332d]/30 text-[#24332d] transition-colors hover:bg-[#24332d] hover:text-[#ede7d8]"
          aria-label="Close tooltip"
        >
          <X className="size-5" />
        </button>
      </div>

      {/* Description */}
      {p.description_en && (
        <p className="mb-3 text-xs leading-relaxed text-[#24332d]/90 font-sans">
          {p.description_en}
        </p>
      )}

      {/* Address & Coordinates */}
      <div className="mb-3 flex items-center gap-2 font-mono text-[10px] text-[#24332d]/70">
        <MapPin className="size-3 shrink-0 text-[#ad793b]" />
        <span className="truncate">{p.address_en}</span>
      </div>

      {/* Vibe Tags & Price */}
      <div className="mb-4 flex flex-wrap items-center gap-1.5">
        <span className="border border-[#24332d]/30 bg-[#24332d]/5 px-2 py-0.5 font-mono text-[9px] uppercase tracking-wider text-[#24332d]">
          {p.price_range}
        </span>
        {p.vibes &&
          p.vibes.map((vibe) => (
            <span
              key={vibe}
              className="flex items-center gap-1 border border-[#24332d]/20 px-2 py-0.5 font-mono text-[9px] uppercase tracking-wider text-[#24332d]/80"
            >
              <Tag className="size-2.5 text-[#ad793b]" />
              {vibe.replace('-', ' ')}
            </span>
          ))}
      </div>

      {/* Actions */}
      <div className="flex items-center justify-between border-t border-[#24332d]/20 pt-3">
        <a
          href={`https://www.google.com/maps/search/?api=1&query=${lat},${lng}`}
          target="_blank"
          rel="noopener noreferrer"
          className="flex h-11 items-center gap-1 border border-[#24332d] px-4 font-mono text-[10px] uppercase tracking-widest text-[#24332d] transition-colors hover:bg-[#24332d] hover:text-[#ede7d8]"
        >
          Directions <ArrowUpRight className="size-3" />
        </a>

        <span className="font-mono text-[9px] text-[#24332d]/60">
          {lat.toFixed(4)}°N, {lng.toFixed(4)}°E
        </span>
      </div>
    </div>
  )
}
