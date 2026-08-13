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
    <div className={`flex flex-col gap-16 ${className}`}>
      {/* Section 1: WhatsApp Dispatch Direct Contact */}
      <section id="subscribe" className="grid gap-10 border-t border-primary/25 pt-12 lg:grid-cols-[0.7fr_1.3fr]">
        <div>
          <p className="mb-4 font-mono text-[10px] uppercase tracking-[0.2em] text-accent">
            WhatsApp Dispatch
          </p>
          <h2 className="font-serif text-5xl leading-[0.9] tracking-[-0.06em] text-primary lg:text-6xl">
            Know where<br />
            <em className="font-normal">to go next.</em>
          </h2>
        </div>

        <div className="flex max-w-xl flex-col justify-between gap-8 lg:justify-self-end">
          <p className="font-serif text-xl leading-relaxed text-primary/80">
            We’re currently building automated curated bar hop experiences. For now, reach out directly to us on WhatsApp or Email to plan a personal, tailored crawl for your evening!
          </p>

          <div className="flex flex-wrap items-center gap-4">
            <a
              href={waUrl}
              target="_blank"
              rel="noopener noreferrer"
              aria-label="Chat on WhatsApp to plan a curated Cairo bar crawl"
              className="flex h-12 min-h-[44px] min-w-[44px] items-center justify-center gap-2 bg-[#24332d] px-6 font-mono text-[11px] uppercase tracking-[0.16em] text-[#ede7d8] transition-colors hover:bg-accent hover:text-primary-foreground"
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
      </section>

      {/* Section 2: Ground Rules for the Night */}
      <section className="grid gap-10 border-t border-primary/25 pt-12 lg:grid-cols-[0.7fr_1.3fr]">
        <div>
          <p className="mb-4 font-mono text-[10px] uppercase tracking-[0.2em] text-accent">
            Bar Crawl Guidelines
          </p>
          <h2 className="font-serif text-5xl leading-[0.9] tracking-[-0.06em] text-primary lg:text-6xl">
            Ground rules<br />
            <em className="font-normal">for the night.</em>
          </h2>
        </div>

        <div className="max-w-xl lg:justify-self-end">
          <ul className="flex flex-col gap-6 font-serif text-base leading-relaxed text-primary/90">
            <li className="flex items-start gap-4">
              <span className="flex size-8 shrink-0 items-center justify-center border border-accent/40 bg-accent/10 font-mono text-xs font-bold text-accent">
                01
              </span>
              <div>
                <strong className="font-semibold text-primary">Intimate Groups (Max 6–8 people):</strong>
                <p className="mt-1 text-primary/80">
                  Downtown Cairo’s historic bars and backroom bistros have limited seating. Keeping groups small ensures everyone gets a cozy table.
                </p>
              </div>
            </li>
            <li className="flex items-start gap-4">
              <span className="flex size-8 shrink-0 items-center justify-center border border-accent/40 bg-accent/10 font-mono text-xs font-bold text-accent">
                02
              </span>
              <div>
                <strong className="font-semibold text-primary">Experience Over Drinking:</strong>
                <p className="mt-1 text-primary/80">
                  You don’t have to finish every beer and you don’t have to drink alcohol—this walk is about heritage, architecture, atmosphere, and good company.
                </p>
              </div>
            </li>
            <li className="flex items-start gap-4">
              <span className="flex size-8 shrink-0 items-center justify-center border border-accent/40 bg-accent/10 font-mono text-xs font-bold text-accent">
                03
              </span>
              <div>
                <strong className="font-semibold text-primary">Local Respect:</strong>
                <p className="mt-1 text-primary/80">
                  We honor local venue staff, historic atmosphere, and neighborhood character as welcoming guests in Downtown Cairo.
                </p>
              </div>
            </li>
          </ul>
        </div>
      </section>
    </div>
  )
}
