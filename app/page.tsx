"use client";

import { useEffect, useState } from "react";
import {
  ArrowUpRight,
  ChevronDown,
  Clock3,
  Compass,
  MapPin,
  Menu,
  Search,
  Sparkles,
  X,
  Tag,
  DollarSign,
} from "lucide-react";
import MapLibreMap from "@/components/map/MapLibreMap";
import {
  fetchVenuesGeoJSON,
  FALLBACK_VENUES,
  type GeoJSONFeature,
  type GeoJSONFeatureCollection,
} from "@/lib/api";
import PersonalCrawlCard from "@/components/ui/PersonalCrawlCard";
import { CONTACT_CONFIG } from "@/lib/config";

const VIBE_FILTERS = [
  { slug: "all", name: "All Vibes" },
  { slug: "fancy", name: "Fancy" },
  { slug: "ambient-music", name: "Ambient music" },
  { slug: "live-performance", name: "Live performance" },
  { slug: "oud-player", name: "Oud player" },
  { slug: "old-times", name: "Old times" },
  { slug: "dancy", name: "Dancy" },
  { slug: "flirty", name: "Flirty" },
];

const PRICE_FILTERS = [
  { slug: "all", name: "All Prices" },
  { slug: "$", name: "$ Budget" },
  { slug: "$$", name: "$$ Moderate" },
  { slug: "$$$", name: "$$$ Upscale" },
];

export default function Home() {
  const [venuesData, setVenuesData] = useState<GeoJSONFeatureCollection>(FALLBACK_VENUES);
  const [selectedFeature, setSelectedFeature] = useState<GeoJSONFeature | null>(null);
  const [activeVibeFilter, setActiveVibeFilter] = useState("all");
  const [activePriceFilter, setActivePriceFilter] = useState("all");

  const [mobileNav, setMobileNav] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadVenues() {
      setLoading(true);
      const data = await fetchVenuesGeoJSON({
        vibe: activeVibeFilter !== "all" ? activeVibeFilter : undefined,
        price_range: activePriceFilter !== "all" ? activePriceFilter : undefined,
      });
      setVenuesData(data);
      if (data.features.length > 0) {
        setSelectedFeature(data.features[0]);
      } else {
        setSelectedFeature(null);
      }
      setLoading(false);
    }

    loadVenues();
  }, [activeVibeFilter, activePriceFilter]);

  const selectedProps = selectedFeature?.properties;

  return (
    <main className="min-h-screen overflow-hidden bg-background text-foreground">
      {/* Header Navigation */}
      <header className="relative z-20 border-b border-border/70 bg-background/95">
        <div className="mx-auto flex max-w-[1440px] items-center justify-between px-5 py-5 lg:px-10">
          <a
            href="#top"
            className="group flex items-center gap-3"
            aria-label="Bar in Cairo home"
          >
            <span className="font-serif text-2xl font-semibold tracking-[-0.05em] text-primary">
              bar<span className="text-accent">in</span>cairo
            </span>
            <span className="hidden border-l border-border pl-3 font-mono text-[9px] uppercase tracking-[0.22em] text-muted-foreground sm:block">
              The Downtown Index
            </span>
          </a>

          <nav
            className={`${mobileNav ? "flex" : "hidden"} absolute left-0 right-0 top-full flex-col gap-5 border-b border-border bg-background px-5 py-5 font-mono text-[10px] uppercase tracking-[0.18em] md:static md:flex md:flex-row md:items-center md:gap-8 md:border-0 md:bg-transparent md:p-0`}
          >
            <a
              href="#map"
              className="text-muted-foreground transition-colors hover:text-primary"
            >
              Explore the map
            </a>
            <a
              href="#bar-hops"
              className="text-muted-foreground transition-colors hover:text-primary"
            >
              Bar Hops
            </a>
            <a
              href="#about"
              className="text-muted-foreground transition-colors hover:text-primary"
            >
              Our Guide
            </a>
            <a
              href="#subscribe"
              className="border border-primary px-4 py-2 text-primary transition-colors hover:bg-primary hover:text-primary-foreground"
            >
              WhatsApp Dispatch <ArrowUpRight className="ml-1 inline size-3" />
            </a>
          </nav>

          <button
            className="md:hidden p-2 min-h-[44px] min-w-[44px] flex items-center justify-center"
            onClick={() => setMobileNav(!mobileNav)}
            aria-label={mobileNav ? "Close menu" : "Open menu"}
          >
            {mobileNav ? <X /> : <Menu />}
          </button>
        </div>
      </header>

      {/* Hero Section */}
      <section
        id="top"
        className="mx-auto grid max-w-[1440px] gap-10 px-5 pb-14 pt-14 lg:grid-cols-[0.9fr_1.1fr] lg:items-end lg:px-10 lg:pb-20 lg:pt-24"
      >
        <div>
          <p className="mb-5 flex items-center gap-2 font-mono text-[10px] uppercase tracking-[0.22em] text-accent">
            <Compass className="size-3" /> Cairo / Egypt / 30°02′N
          </p>
          <h1 className="max-w-3xl font-serif text-[clamp(3.8rem,8vw,8.6rem)] font-semibold leading-[0.82] tracking-[-0.075em] text-primary">
            The night
            <br />
            <em className="font-normal text-accent">has a map.</em>
          </h1>
        </div>

        <div className="flex max-w-lg flex-col gap-6 lg:pb-2 lg:pl-14">
          <p className="font-serif text-xl leading-relaxed text-primary/80 lg:text-2xl">
            A living spatial index to the bars, backrooms, rooftop corners, and historic
            spots of Wust El Balad, Cairo.
          </p>
          <div className="flex items-center gap-3 border-t border-border pt-4 font-mono text-[10px] uppercase tracking-[0.18em] text-muted-foreground">
            <span className="size-2 rounded-full bg-accent" /> First Edition · PostGIS
            Vector Stream
          </div>
        </div>
      </section>

      {/* Interactive WebGL Spatial Map & Filter Controls */}
      <section id="map" className="relative border-y border-primary/25 bg-card">
        <div className="mx-auto max-w-[1440px] px-5 py-5 lg:px-10">
          <div className="flex flex-wrap items-center justify-between gap-4 border-b border-primary/20 pb-4">
            <div className="flex items-center gap-3">
              <span className="font-mono text-[10px] uppercase tracking-[0.2em] text-primary">
                Plate 01
              </span>
              <span className="text-muted-foreground">/</span>
              <span className="font-mono text-[10px] uppercase tracking-[0.2em] text-muted-foreground">
                Downtown · {venuesData.features.length} Spots Indexed
              </span>
            </div>

            {/* Price Range Filter Pills */}
            <div className="flex flex-wrap items-center gap-2 font-mono text-[10px] uppercase tracking-[0.16em]">
              <span className="text-muted-foreground flex items-center gap-1 mr-1">
                <DollarSign className="size-3" /> Price:
              </span>
              {PRICE_FILTERS.map((p) => (
                <button
                  key={p.slug}
                  onClick={() => setActivePriceFilter(p.slug)}
                  className={`min-h-[44px] px-3 py-1 border transition-colors ${
                    activePriceFilter === p.slug
                      ? "border-primary bg-primary text-primary-foreground font-semibold"
                      : "border-primary/30 text-muted-foreground hover:border-primary hover:text-primary"
                  }`}
                >
                  {p.name}
                </button>
              ))}
            </div>
          </div>

          {/* Vibe Tag Filter Pills */}
          <div className="my-4 flex flex-wrap items-center gap-2 font-mono text-[10px] uppercase tracking-[0.14em]">
            <span className="text-muted-foreground flex items-center gap-1 mr-1">
              <Tag className="size-3 text-accent" /> Vibes:
            </span>
            {VIBE_FILTERS.map((v) => (
              <button
                key={v.slug}
                onClick={() => setActiveVibeFilter(v.slug)}
                className={`min-h-[44px] px-3 py-1 border transition-colors ${
                  activeVibeFilter === v.slug
                    ? "border-accent bg-accent text-primary-foreground font-semibold"
                    : "border-primary/25 text-muted-foreground hover:border-accent hover:text-primary"
                }`}
              >
                {v.name}
              </button>
            ))}
          </div>

          {/* MapLibre Vector Map Canvas */}
          <MapLibreMap
            venues={venuesData}
            selectedVenue={selectedFeature}
            onSelectVenue={(venue) => setSelectedFeature(venue)}
          />
        </div>
      </section>

      {/* Selected Venue Detail Card */}
      <section className="mx-auto grid max-w-[1440px] gap-10 px-5 py-16 lg:grid-cols-[0.7fr_1.3fr] lg:px-10 lg:py-24">
        <div className="flex flex-col justify-between gap-8">
          <div>
            <p className="mb-4 font-mono text-[10px] uppercase tracking-[0.2em] text-accent">
              Selected from the map
            </p>
            <h2 className="font-serif text-5xl leading-[0.9] tracking-[-0.06em] text-primary lg:text-7xl">
              A good place
              <br />
              <em className="font-normal">to begin.</em>
            </h2>
          </div>
          <p className="max-w-xs font-serif text-lg leading-relaxed text-muted-foreground">
            Start with the old centre. Let the streets decide what comes next.
          </p>
        </div>

        {selectedProps && (
          <article className="grid overflow-hidden border border-primary/25 bg-card sm:grid-cols-[0.85fr_1.15fr]">
            <div
              className="min-h-72 bg-cover bg-center"
              style={{
                backgroundImage: `url(${selectedProps.photo_url || "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=900&q=80"})`,
              }}
              role="img"
              aria-label={`${selectedProps.name_en} atmosphere`}
            />

            <div className="flex flex-col justify-between gap-8 p-6 lg:p-9">
              <div>
                <div className="mb-5 flex items-start justify-between gap-3">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-[10px] uppercase tracking-[0.16em] text-accent">
                        {selectedProps.category_name}
                      </span>
                      <span className="font-mono text-[10px] font-bold text-primary border border-primary/30 px-1.5 py-0.5">
                        {selectedProps.price_range}
                      </span>
                    </div>
                    <h3 className="mt-2 font-serif text-4xl leading-none tracking-[-0.05em] text-primary">
                      {selectedProps.name_en}
                    </h3>
                    <p className="mt-1 font-serif text-lg text-muted-foreground">
                      {selectedProps.name_ar}
                    </p>
                  </div>

                  <button
                    className="border border-primary/30 p-2 min-h-[44px] min-w-[44px] flex items-center justify-center text-primary transition-colors hover:bg-primary hover:text-primary-foreground"
                    aria-label="Search venue details"
                  >
                    <Search className="size-4" />
                  </button>
                </div>

                <p className="max-w-md font-serif text-lg leading-relaxed text-primary/80">
                  {selectedProps.description_en}
                </p>
              </div>

              <div>
                <div className="mb-5 flex flex-wrap gap-2">
                  <span className="border border-primary/25 px-3 py-1 font-mono text-[9px] uppercase tracking-[0.13em] text-primary">
                    {selectedProps.vibe_description || "Downtown Vibe"}
                  </span>

                  {selectedProps.vibes.map((vibeSlug) => (
                    <span
                      key={vibeSlug}
                      className="border border-accent/40 bg-accent/10 px-2 py-1 font-mono text-[9px] uppercase tracking-[0.13em] text-accent"
                    >
                      #{vibeSlug}
                    </span>
                  ))}

                  <span className="border border-primary/25 px-3 py-1 font-mono text-[9px] uppercase tracking-[0.13em] text-primary">
                    <MapPin className="mr-1 inline size-3" /> {selectedProps.address_en}
                  </span>
                </div>

                <button className="flex items-center gap-2 font-mono text-[10px] uppercase tracking-[0.16em] text-accent hover:text-primary">
                  Open full listing <ArrowUpRight className="size-3" />
                </button>
              </div>
            </div>
          </article>
        )}
      </section>

      {/* Bar Hops Trail Banner */}
      <section
        id="bar-hops"
        className="border-y border-primary/25 bg-primary px-5 py-16 text-primary-foreground lg:px-10 lg:py-24"
      >
        <div className="mx-auto grid max-w-[1440px] gap-10 lg:grid-cols-[1fr_1fr] lg:items-center">
          <div>
            <p className="mb-5 flex items-center gap-2 font-mono text-[10px] uppercase tracking-[0.2em] text-accent">
              <Sparkles className="size-3" /> Coming Up Next
            </p>
            <h2 className="font-serif text-5xl leading-[0.88] tracking-[-0.06em] lg:text-7xl">
              Don’t go home
              <br />
              <em className="font-normal text-accent">just yet.</em>
            </h2>
          </div>

          <div className="max-w-lg lg:justify-self-end">
            <p className="mb-6 font-serif text-xl leading-relaxed text-primary-foreground/80">
              Join a small group of curious people as we follow a handpicked trail through
              Downtown’s after-hours institutions.
            </p>
            <div className="flex flex-wrap gap-4 font-mono text-[10px] uppercase tracking-[0.16em] text-primary-foreground/70">
              <span className="flex items-center gap-2">
                <Clock3 className="size-4 text-accent" /> 4 hours
              </span>
              <span className="flex items-center gap-2">
                <MapPin className="size-4 text-accent" /> 4 stops
              </span>
              <a
                href="#subscribe"
                className="flex items-center gap-2 text-accent hover:text-primary-foreground"
              >
                Register interest <ArrowUpRight className="size-3" />
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* WhatsApp Dispatch & Personal Bar Crawl Section */}
      <section className="mx-auto max-w-[1440px] px-5 py-16 lg:px-10 lg:py-24">
        <PersonalCrawlCard
          whatsappNumber={CONTACT_CONFIG.WHATSAPP_NUMBER}
          contactEmail={CONTACT_CONFIG.CONTACT_EMAIL}
        />
      </section>

      {/* Footer */}
      <footer id="about" className="border-t border-border px-5 py-8 lg:px-10">
        <div className="mx-auto flex max-w-[1440px] flex-col justify-between gap-5 sm:flex-row sm:items-center">
          <span className="font-serif text-lg font-semibold tracking-[-0.04em] text-primary">
            bar<span className="text-accent">in</span>cairo
          </span>
          <p className="font-mono text-[9px] uppercase tracking-[0.16em] text-muted-foreground">
            Made for the curious · Cairo, Egypt · 2026
          </p>
          <a
            href="#top"
            className="font-mono text-[9px] uppercase tracking-[0.16em] text-muted-foreground hover:text-primary"
          >
            Back to top <ChevronDown className="ml-1 inline size-3 rotate-180" />
          </a>
        </div>
      </footer>
    </main>
  );
}
