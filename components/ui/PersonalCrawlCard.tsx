import React from 'react'
import { MessageCircle, Mail, ArrowUpRight } from 'lucide-react'
import { CONTACT_CONFIG } from '@/lib/config'

export interface PersonalCrawlCardProps {
  whatsappNumber: string
  contactEmail: string
  className?: string
}

export default function PersonalCrawlCard({
  whatsappNumber,
  contactEmail,
  className = '',
}: PersonalCrawlCardProps) {
  const cleanPhone = whatsappNumber.replace(/[^0-9]/g, '')
  const waUrl = cleanPhone
    ? `https://wa.me/${cleanPhone}?text=${encodeURIComponent(CONTACT_CONFIG.DEFAULT_WA_MESSAGE)}`
    : `https://wa.me/?text=${encodeURIComponent(CONTACT_CONFIG.DEFAULT_WA_MESSAGE)}`

  const mailtoUrl = `mailto:${encodeURIComponent(contactEmail)}?subject=${encodeURIComponent('Curated Cairo Bar Hop')}`

  return (
    <article
      id="subscribe"
      className={`border-2 border-[#24332d] bg-[#ede7d8] p-6 lg:p-10 shadow-[4px_4px_0px_#24332d] ${className}`}
    >
      <div className="flex flex-col gap-6">
        <div>
          <p className="mb-3 font-mono text-[10px] uppercase tracking-[0.2em] text-[#ad793b]">
            Personal Nightlife Concierge
          </p>
          <h2 className="font-serif text-3xl font-semibold leading-tight text-[#24332d] lg:text-5xl">
            Want a Personal Downtown Cairo Bar Hop?
          </h2>
        </div>

        <p className="font-serif text-lg leading-relaxed text-[#24332d]/80 lg:text-xl">
          Hey there! We love Downtown Cairo&apos;s historic bars, hidden passage bistros, and rooftop breezes. Looking for a friendly, curated night out? Message us directly on WhatsApp and let&apos;s plan a fun bar crawl tailored to your vibe!
        </p>

        <div className="flex flex-wrap items-center gap-4 pt-2">
          <a
            href={waUrl}
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Chat on WhatsApp to plan a curated Cairo bar crawl"
            className="flex h-12 min-h-[44px] min-w-[44px] items-center justify-center gap-2 bg-[#24332d] px-6 font-mono text-[11px] uppercase tracking-[0.16em] text-[#ede7d8] transition-colors hover:bg-[#ad793b]"
          >
            <MessageCircle className="size-4" />
            <span>Chat on WhatsApp</span>
            <ArrowUpRight className="size-4" />
          </a>

          <a
            href={mailtoUrl}
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Send an email to organize a Cairo bar crawl"
            className="flex h-12 min-h-[44px] min-w-[44px] items-center justify-center gap-2 border border-[#24332d] px-6 font-mono text-[11px] uppercase tracking-[0.16em] text-[#24332d] transition-colors hover:bg-[#24332d] hover:text-[#ede7d8]"
          >
            <Mail className="size-4" />
            <span>Or send an email</span>
          </a>
        </div>
      </div>
    </article>
  )
}
