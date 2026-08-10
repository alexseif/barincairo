'use client'

import { useState } from 'react'
import { ArrowUpRight, ChevronDown, Clock3, Compass, Mail, MapPin, Menu, Search, Sparkles, X } from 'lucide-react'

const bars = [
  { id: 'cairo-jazz', name: 'Cairo Jazz Club 610', arabic: 'كايرو جاز كلوب', type: 'Live music', address: '610, First New Cairo', vibe: 'Late-night / electric', top: '26%', left: '54%', photo: 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=900&q=80', description: 'A beloved institution for live sets, smoky corners, and the city’s most reliable midnight energy.' },
  { id: 'vent', name: 'Vent', arabic: 'فِنت', type: 'Cocktail bar', address: '12 El-Horeya, Downtown', vibe: 'Intimate / considered', top: '48%', left: '42%', photo: 'https://images.unsplash.com/photo-1515003197210-e0cd71810b5f?auto=format&fit=crop&w=900&q=80', description: 'A small, low-lit room for beautifully balanced drinks and long conversations.' },
  { id: 'homos', name: 'Horus', arabic: 'حورس', type: 'Rooftop', address: 'Talaat Harb Square', vibe: 'Golden hour / open-air', top: '37%', left: '66%', photo: 'https://images.unsplash.com/photo-1572116469696-31de0f17cc34?auto=format&fit=crop&w=900&q=80', description: 'Watch the downtown rooftops turn copper over a cold Sakara and a plate of mezze.' },
  { id: 'soma', name: 'Soma Caffe', arabic: 'سوما كافيه', type: 'Cafe bar', address: '26 Sherif Street', vibe: 'Quiet / all-day', top: '64%', left: '59%', photo: 'https://images.unsplash.com/photo-1514933651103-005eec06c04b?auto=format&fit=crop&w=900&q=80', description: 'A daytime cafe that quietly becomes one of Downtown’s favorite after-dark hideouts.' },
]

const attractions = [
  { name: 'Tahrir Square', arabic: 'ميدان التحرير', top: '67%', left: '28%' },
  { name: 'Egyptian Museum', arabic: 'المتحف المصري', top: '56%', left: '23%' },
  { name: 'Talaat Harb Sq.', arabic: 'ميدان طلعت حرب', top: '30%', left: '51%' },
]

export default function Home() {
  const [selected, setSelected] = useState(bars[1])
  const [mobileNav, setMobileNav] = useState(false)
  const [whatsapp, setWhatsapp] = useState('')
  const [subscribed, setSubscribed] = useState(false)

  function handleSubscribe(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (whatsapp.trim()) setSubscribed(true)
  }

  return (
    <main className="min-h-screen overflow-hidden bg-background text-foreground">
      <header className="relative z-20 border-b border-border/70 bg-background/95">
        <div className="mx-auto flex max-w-[1440px] items-center justify-between px-5 py-5 lg:px-10">
          <a href="#top" className="group flex items-center gap-3" aria-label="Bar in Cairo home">
            <span className="font-serif text-2xl font-semibold tracking-[-0.05em] text-primary">bar<span className="text-accent">in</span>cairo</span>
            <span className="hidden border-l border-border pl-3 font-mono text-[9px] uppercase tracking-[0.22em] text-muted-foreground sm:block">The downtown index</span>
          </a>
          <nav className={`${mobileNav ? 'flex' : 'hidden'} absolute left-0 right-0 top-full flex-col gap-5 border-b border-border bg-background px-5 py-5 font-mono text-[10px] uppercase tracking-[0.18em] md:static md:flex md:flex-row md:items-center md:gap-8 md:border-0 md:bg-transparent md:p-0`}>
            <a href="#map" className="text-muted-foreground transition-colors hover:text-primary">Explore the map</a>
            <a href="#bar-hops" className="text-muted-foreground transition-colors hover:text-primary">Bar hops</a>
            <a href="#about" className="text-muted-foreground transition-colors hover:text-primary">Our guide</a>
            <a href="#subscribe" className="border border-primary px-4 py-2 text-primary transition-colors hover:bg-primary hover:text-primary-foreground">WhatsApp Dispatch <ArrowUpRight className="ml-1 inline size-3" /></a>
          </nav>
          <button className="md:hidden" onClick={() => setMobileNav(!mobileNav)} aria-label={mobileNav ? 'Close menu' : 'Open menu'}>{mobileNav ? <X /> : <Menu />}</button>
        </div>
      </header>

      <section id="top" className="mx-auto grid max-w-[1440px] gap-10 px-5 pb-14 pt-14 lg:grid-cols-[0.9fr_1.1fr] lg:items-end lg:px-10 lg:pb-20 lg:pt-24">
        <div>
          <p className="mb-5 flex items-center gap-2 font-mono text-[10px] uppercase tracking-[0.22em] text-accent"><Compass className="size-3" /> Cairo / Egypt / 30°02′N</p>
          <h1 className="max-w-3xl font-serif text-[clamp(3.8rem,8vw,8.6rem)] font-semibold leading-[0.82] tracking-[-0.075em] text-primary">The night<br /><em className="font-normal text-accent">has a map.</em></h1>
        </div>
        <div className="flex max-w-lg flex-col gap-6 lg:pb-2 lg:pl-14">
          <p className="font-serif text-xl leading-relaxed text-primary/80 lg:text-2xl">A living guide to the bars, backrooms, hotel lounges, and rooftop corners of Cairo.</p>
          <div className="flex items-center gap-3 border-t border-border pt-4 font-mono text-[10px] uppercase tracking-[0.18em] text-muted-foreground"><span className="size-2 rounded-full bg-accent" /> First edition · Downtown Cairo</div>
        </div>
      </section>

      <section id="map" className="relative border-y border-primary/25 bg-card">
        <div className="mx-auto max-w-[1440px] px-5 py-5 lg:px-10">
          <div className="flex flex-wrap items-center justify-between gap-4 border-b border-primary/20 pb-4">
            <div className="flex items-center gap-3"><span className="font-mono text-[10px] uppercase tracking-[0.2em] text-primary">Plate 01</span><span className="text-muted-foreground">/</span><span className="font-mono text-[10px] uppercase tracking-[0.2em] text-muted-foreground">Downtown · 4 spots indexed</span></div>
            <div className="flex items-center gap-5 font-mono text-[10px] uppercase tracking-[0.16em] text-muted-foreground"><span><span className="mr-2 inline-block size-2 rounded-full bg-accent" /> Bar</span><span><span className="mr-2 inline-block size-2 border border-primary" /> Landmark</span><span className="hidden sm:inline">Updated 08.26</span></div>
          </div>
          <div className="relative mt-5 aspect-[1.1/1] overflow-hidden border border-primary/20 bg-[#d1c5a8] sm:aspect-[1.8/1] lg:aspect-[2.2/1]">
            <div className="map-grid absolute inset-0 opacity-35" />
            <div className="river absolute -right-[8%] top-[-15%] h-[140%] w-[16%] rotate-[12deg] bg-primary/10 blur-[2px]" />
            <div className="street street-one" /><div className="street street-two" /><div className="street street-three" /><div className="street street-four" /><div className="street street-five" />
            <span className="absolute left-4 top-4 font-mono text-[9px] uppercase tracking-[0.2em] text-primary/60">Downtown Cairo</span>
            <span className="absolute bottom-4 right-4 font-serif text-lg italic text-primary/60">القاهرة</span>
            {attractions.map((place) => <div key={place.name} className="absolute -translate-x-1/2 -translate-y-1/2 text-center" style={{ top: place.top, left: place.left }}><div className="mx-auto mb-1 size-3 rotate-45 border border-primary bg-card/60" /><p className="whitespace-nowrap font-mono text-[8px] uppercase tracking-[0.12em] text-primary">{place.name}</p><p className="font-serif text-[11px] text-primary/70">{place.arabic}</p></div>)}
            {bars.map((bar) => <button key={bar.id} onClick={() => setSelected(bar)} className={`group absolute -translate-x-1/2 -translate-y-1/2 text-left transition-transform hover:scale-110 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent ${selected.id === bar.id ? 'z-10 scale-110' : ''}`} style={{ top: bar.top, left: bar.left }} aria-label={`View ${bar.name}`}><span className="relative block size-7 rounded-full border-2 border-card bg-accent shadow-[0_2px_0_theme(colors.primary)]"><span className="absolute inset-1 rounded-full border border-primary/60" /></span><span className="mt-2 block whitespace-nowrap bg-card/90 px-1 font-mono text-[9px] uppercase tracking-[0.12em] text-primary opacity-0 transition-opacity group-hover:opacity-100 group-focus-visible:opacity-100">{bar.name}</span></button>)}
            <div className="absolute bottom-4 left-4 flex items-center gap-2 font-mono text-[9px] uppercase tracking-[0.14em] text-primary"><span className="block h-px w-16 bg-primary" /> 500m</div>
          </div>
        </div>
      </section>

      <section className="mx-auto grid max-w-[1440px] gap-10 px-5 py-16 lg:grid-cols-[0.7fr_1.3fr] lg:px-10 lg:py-24">
        <div className="flex flex-col justify-between gap-8"><div><p className="mb-4 font-mono text-[10px] uppercase tracking-[0.2em] text-accent">Selected from the map</p><h2 className="font-serif text-5xl leading-[0.9] tracking-[-0.06em] text-primary lg:text-7xl">A good place<br /><em className="font-normal">to begin.</em></h2></div><p className="max-w-xs font-serif text-lg leading-relaxed text-muted-foreground">Start with the old centre. Let the streets decide what comes next.</p></div>
        <article className="grid overflow-hidden border border-primary/25 bg-card sm:grid-cols-[0.85fr_1.15fr]"><div className="min-h-72 bg-cover bg-center" style={{ backgroundImage: `url(${selected.photo})` }} role="img" aria-label={`${selected.name} atmosphere`} /><div className="flex flex-col justify-between gap-8 p-6 lg:p-9"><div><div className="mb-5 flex items-start justify-between gap-3"><div><p className="font-mono text-[10px] uppercase tracking-[0.16em] text-accent">{selected.type}</p><h3 className="mt-2 font-serif text-4xl leading-none tracking-[-0.05em] text-primary">{selected.name}</h3><p className="mt-1 font-serif text-lg text-muted-foreground">{selected.arabic}</p></div><button className="border border-primary/30 p-2 text-primary transition-colors hover:bg-primary hover:text-primary-foreground" aria-label="Search this bar"><Search className="size-4" /></button></div><p className="max-w-md font-serif text-lg leading-relaxed text-primary/80">{selected.description}</p></div><div><div className="mb-5 flex flex-wrap gap-2"><span className="border border-primary/25 px-3 py-1 font-mono text-[9px] uppercase tracking-[0.13em] text-primary">{selected.vibe}</span><span className="border border-primary/25 px-3 py-1 font-mono text-[9px] uppercase tracking-[0.13em] text-primary"><MapPin className="mr-1 inline size-3" /> {selected.address}</span></div><button className="flex items-center gap-2 font-mono text-[10px] uppercase tracking-[0.16em] text-accent hover:text-primary">Open full listing <ArrowUpRight className="size-3" /></button></div></div></article>
      </section>

      <section id="bar-hops" className="border-y border-primary/25 bg-primary px-5 py-16 text-primary-foreground lg:px-10 lg:py-24"><div className="mx-auto grid max-w-[1440px] gap-10 lg:grid-cols-[1fr_1fr] lg:items-center"><div><p className="mb-5 flex items-center gap-2 font-mono text-[10px] uppercase tracking-[0.2em] text-accent"><Sparkles className="size-3" /> Coming up next</p><h2 className="font-serif text-5xl leading-[0.88] tracking-[-0.06em] lg:text-7xl">Don’t go home<br /><em className="font-normal text-accent">just yet.</em></h2></div><div className="max-w-lg lg:justify-self-end"><p className="mb-6 font-serif text-xl leading-relaxed text-primary-foreground/80">Join a small group of curious people as we follow a handpicked trail through Downtown’s after-hours institutions.</p><div className="flex flex-wrap gap-4 font-mono text-[10px] uppercase tracking-[0.16em] text-primary-foreground/70"><span className="flex items-center gap-2"><Clock3 className="size-4 text-accent" /> 4 hours</span><span className="flex items-center gap-2"><MapPin className="size-4 text-accent" /> 4 stops</span><a href="#subscribe" className="flex items-center gap-2 text-accent hover:text-primary-foreground">Register interest <ArrowUpRight className="size-3" /></a></div></div></div></section>

      <section id="subscribe" className="mx-auto grid max-w-[1440px] gap-10 px-5 py-16 lg:grid-cols-[0.7fr_1.3fr] lg:px-10 lg:py-24"><div><p className="mb-4 font-mono text-[10px] uppercase tracking-[0.2em] text-accent">WhatsApp Dispatch</p><h2 className="font-serif text-5xl leading-[0.9] tracking-[-0.06em] text-primary lg:text-6xl">Know where<br /><em className="font-normal">to go next.</em></h2></div><div className="flex max-w-xl flex-col justify-end gap-6 lg:justify-self-end"><p className="font-serif text-xl leading-relaxed text-primary/80">New openings, old favourites, and the occasional invitation directly to your WhatsApp. One thoughtful note, never noise.</p>{subscribed ? <p className="border-b border-primary py-4 font-mono text-[10px] uppercase tracking-[0.16em] text-accent">You’re on the WhatsApp dispatch. Ahla wa sahla.</p> : <form onSubmit={handleSubscribe} className="flex border-b border-primary py-2"><label htmlFor="whatsapp" className="sr-only">Your WhatsApp number</label><input id="whatsapp" type="tel" required value={whatsapp} onChange={(event) => setWhatsapp(event.target.value)} placeholder="WhatsApp number (e.g. +20 100 000 0000)" className="min-w-0 flex-1 bg-transparent font-serif text-lg text-primary outline-none placeholder:text-muted-foreground" /><button type="submit" className="flex items-center gap-2 font-mono text-[10px] uppercase tracking-[0.16em] text-accent hover:text-primary">Subscribe <ArrowUpRight className="size-3" /></button></form>}</div></section>

      <footer id="about" className="border-t border-border px-5 py-8 lg:px-10"><div className="mx-auto flex max-w-[1440px] flex-col justify-between gap-5 sm:flex-row sm:items-center"><span className="font-serif text-lg font-semibold tracking-[-0.04em] text-primary">bar<span className="text-accent">in</span>cairo</span><p className="font-mono text-[9px] uppercase tracking-[0.16em] text-muted-foreground">Made for the curious · Cairo, Egypt · 2026</p><a href="#top" className="font-mono text-[9px] uppercase tracking-[0.16em] text-muted-foreground hover:text-primary">Back to top <ChevronDown className="ml-1 inline size-3 rotate-180" /></a></div></footer>
    </main>
  )
}
