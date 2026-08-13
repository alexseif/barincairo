import React from 'react'
import { MessageCircle, Mail, ArrowUpRight, Users, HeartHandshake, ShieldCheck } from 'lucide-react'
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
      className={`grid gap-10 border border-primary/25 bg-card p-6 lg:grid-cols-[0.7fr_1.3fr] lg:p-12 ${className}`}
    >
      {/* Left Column */}
      <div>
        <p className="mb-4 font-mono text-[10px] uppercase tracking-[0.2em] text-accent">
          WhatsApp Dispatch
        </p>
        <h2 className="font-serif text-5xl leading-[0.9] tracking-[-0.06em] text-primary lg:text-6xl">
          Know where<br />
          <em className="font-normal">to go next.</em>
        </h2>
      </div>

      {/* Right Column */}
      <div className="flex flex-col gap-8 lg:justify-self-end lg:max-w-xl">
        <p className="font-serif text-xl leading-relaxed text-primary/80">
          We’re currently building automated curated bar hop experiences for Downtown Cairo. In the meantime, connect with us directly on WhatsApp or Email—we’d love to organize a personal, tailored crawl for your evening!
        </p>

        {/* Ground Rules */}
        <div className="border-y border-primary/20 py-6">
          <p className="mb-4 font-mono text-[10px] uppercase tracking-[0.18em] text-accent">
            Our Bar Crawl Guidelines
          </p>
          <ul className="flex flex-col gap-4 font-serif text-sm leading-snug text-primary/90">
            <li className="flex items-start gap-3">
              <Users className="mt-0.5 size-4 shrink-0 text-accent" />
              <span>
                <strong className="font-semibold text-primary">Intimate Groups:</strong> Max 6–8 people per walk so everyone fits at Downtown Cairo’s historic, cozy bar tables.
              </span>
            </li>
            <li className="flex items-start gap-3">
              <HeartHandshake className="mt-0.5 size-4 shrink-0 text-accent" />
              <span>
                <strong className="font-semibold text-primary">Experience Over Drinking:</strong> Zero pressure to finish every drink or consume alcohol—our focus is heritage, architecture, and great conversation.
              </span>
            </li>
            <li className="flex items-start gap-3">
              <ShieldCheck className="mt-0.5 size-4 shrink-0 text-accent" />
              <span>
                <strong className="font-semibold text-primary">Local Respect:</strong> We honor local venue staff, historic atmosphere, and neighborhood character.
              </span>
            </li>
          </ul>
        </div>

        {/* Direct Action CTAs */}
        <div className="flex flex-wrap items-center gap-4">
          <a
            href={waUrl}
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Chat on WhatsApp to plan a curated Cairo bar crawl"
            className="flex h-12 min-h-[44px] min-w-[44px] items-center justify-center gap-2 bg-primary px-6 font-mono text-[11px] uppercase tracking-[0.16em] text-primary-foreground transition-colors hover:bg-accent hover:text-primary-foreground"
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
            className="flex h-12 min-h-[44px] min-w-[44px] items-center justify-center gap-2 border border-primary px-6 font-mono text-[11px] uppercase tracking-[0.16em] text-primary transition-colors hover:bg-primary hover:text-primary-foreground"
          >
            <Mail className="size-4" />
            <span>Or send an email</span>
          </a>
        </div>
      </div>
    </article>
  )
}
