"use client";

import { lazy, Suspense, useEffect, useState } from "react";
import {
  ArrowUpRight,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
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
const MapLibreMap = lazy(() => import("@/components/map/MapLibreMap"));
import {
  fetchVenuesGeoJSON,
  getVenueName,
  getVenueDescription,
  getVenueAddress,
  type GeoJSONFeature,
  type GeoJSONFeatureCollection,
} from "@/lib/api";
import PersonalCrawlCard from "@/components/ui/PersonalCrawlCard";
import ComingSoonModal from "@/components/ui/ComingSoonModal";
import { CONTACT_CONFIG } from "@/lib/config";

import { useVenuesQuery } from "@/lib/hooks";
import { useSearch, useNavigate, Link } from "@tanstack/react-router";

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
  const [selectedFeature, setSelectedFeature] = useState<GeoJSONFeature | null>(null);
  const [carouselIndex, setCarouselIndex] = useState(0);

  const search = useSearch({ strict: false }) as { vibe?: string; price_range?: string };
  const navigate = useNavigate({ from: '/' });

  const activeVibeFilter = search.vibe || "all";
  const activePriceFilter = search.price_range || "all";

  const setActiveVibeFilter = (vibe: string) => {
    navigate({
      search: (prev: Record<string, unknown>) => ({
        ...prev,
        vibe: vibe !== "all" ? vibe : undefined,
      }),
      replace: true,
    });
  };

  const setActivePriceFilter = (price: string) => {
    navigate({
      search: (prev: Record<string, unknown>) => ({
        ...prev,
        price_range: price !== "all" ? price : undefined,
      }),
      replace: true,
    });
  };

  const [mobileNav, setMobileNav] = useState(false);

  const filters = {
    vibe: activeVibeFilter !== "all" ? activeVibeFilter : undefined,
    price_range: activePriceFilter !== "all" ? activePriceFilter : undefined,
  };

  const { data: venuesData = { type: "FeatureCollection", features: [] }, isLoading: loading } = useVenuesQuery(filters);

  useEffect(() => {
    if (venuesData.features.length > 0) {
      setSelectedFeature((prev) => {
        if (prev && venuesData.features.some((f) => f.properties.id === prev.properties.id)) {
          return prev;
        }
        return venuesData.features[0];
      });
      setCarouselIndex(0);
    } else {
      setSelectedFeature(null);
      setCarouselIndex(0);
    }
  }, [venuesData]);

  // Selected Carousel Features (Top 3 venues or filtered features)
  const carouselVenues = venuesData.features.slice(0, 3);
  const activeCarouselFeature =
    selectedFeature || carouselVenues[carouselIndex] || venuesData.features[0] || null;
  const selectedProps = activeCarouselFeature?.properties;

  const handlePrevCarousel = () => {
    if (carouselVenues.length === 0) return;
    const nextIdx = (carouselIndex - 1 + carouselVenues.length) % carouselVenues.length;
    setCarouselIndex(nextIdx);
    setSelectedFeature(carouselVenues[nextIdx]);
  };

  const handleNextCarousel = () => {
    if (carouselVenues.length === 0) return;
    const nextIdx = (carouselIndex + 1) % carouselVenues.length;
    setCarouselIndex(nextIdx);
    setSelectedFeature(carouselVenues[nextIdx]);
  };

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
            {/* Header Site Title: 2rem (32px) */}
            <span className="font-serif text-[2rem] font-semibold tracking-[-0.05em] text-primary">
              bar<span className="text-accent">in</span>cairo
            </span>
            {/* Header Site Tagline: 11px (0.6875rem) */}
            <span className="hidden border-l border-border pl-3 font-mono text-[0.6875rem] uppercase tracking-[0.22em] text-muted-foreground sm:block">
              The Downtown Index
            </span>
          </a>

          {/* Header Menu: 12px (0.75rem) */}
          <nav
            className={`${
              mobileNav ? "flex" : "hidden"
            } absolute left-0 right-0 top-full flex-col gap-5 border-b border-border bg-background px-5 py-5 font-mono text-[0.75rem] uppercase tracking-[0.18em] md:static md:flex md:flex-row md:items-center md:gap-8 md:border-0 md:bg-transparent md:p-0`}
          >
            <a
              href="#map"
              onClick={() => setMobileNav(false)}
              className="text-muted-foreground transition-colors hover:text-primary"
            >
              Explore the map
            </a>
            <a
              href="#bar-hops"
              onClick={() => setMobileNav(false)}
              className="text-muted-foreground transition-colors hover:text-primary"
            >
              Bar Hops
            </a>
            <a
              href="#our-guide"
              onClick={() => setMobileNav(false)}
              className="text-muted-foreground transition-colors hover:text-primary"
            >
              Our Guide
            </a>
            <a
              href="#subscribe"
              onClick={() => setMobileNav(false)}
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
          <p className="mb-5 flex items-center gap-2 font-mono text-[0.625rem] uppercase tracking-[0.22em] text-accent">
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
            spots of{" "}
            {/* Hero tooltip for Wust El Balad -> Downtown */}
            <span className="group relative cursor-help underline decoration-accent decoration-dotted underline-offset-4 font-medium text-primary">
              Wust El Balad
              <span className="pointer-events-none absolute bottom-full left-1/2 -translate-x-1/2 mb-2 hidden group-hover:block bg-[#24332d] text-[#ede7d8] font-mono text-[0.6875rem] uppercase tracking-wider px-2.5 py-1 shadow-md whitespace-nowrap rounded-none border border-accent">
                Downtown
              </span>
            </span>
            , Cairo.
          </p>
          <div className="flex items-center gap-3 border-t border-border pt-4 font-mono text-[0.625rem] uppercase tracking-[0.18em] text-muted-foreground">
            <span className="size-2 rounded-full bg-accent" /> First Edition · Python API
            Live Stream
          </div>
        </div>
      </section>

      {/* Interactive WebGL Map & Filter Controls */}
      <section id="map" className="relative border-y border-primary/25 bg-card">
        <div className="mx-auto max-w-[1440px] px-5 py-5 lg:px-10">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-primary/20 pb-4">
            <div className="flex items-center gap-3">
              <span className="font-mono text-[0.625rem] uppercase tracking-[0.2em] text-primary">
                Plate 01
              </span>
              <span className="text-muted-foreground">/</span>
              <span className="font-mono text-[0.625rem] uppercase tracking-[0.2em] text-muted-foreground">
                Downtown · {venuesData.features.length} Spots Indexed
              </span>
            </div>

            {/* Mobile View: Combobox Dropdown for Filters to Save Space */}
            <div className="flex sm:hidden flex-col gap-2">
              <div className="flex items-center gap-2">
                <label htmlFor="price-select" className="font-mono text-[0.6875rem] uppercase tracking-wider text-muted-foreground flex items-center gap-1 w-20">
                  <DollarSign className="size-3" /> Price:
                </label>
                <select
                  id="price-select"
                  value={activePriceFilter}
                  onChange={(e) => setActivePriceFilter(e.target.value)}
                  className="flex-1 bg-background border border-primary/30 px-3 py-2 font-mono text-[0.75rem] uppercase text-primary focus:outline-none focus:border-accent"
                >
                  {PRICE_FILTERS.map((p) => (
                    <option key={p.slug} value={p.slug}>
                      {p.name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="flex items-center gap-2">
                <label htmlFor="vibe-select" className="font-mono text-[0.6875rem] uppercase tracking-wider text-muted-foreground flex items-center gap-1 w-20">
                  <Tag className="size-3 text-accent" /> Vibe:
                </label>
                <select
                  id="vibe-select"
                  value={activeVibeFilter}
                  onChange={(e) => setActiveVibeFilter(e.target.value)}
                  className="flex-1 bg-background border border-primary/30 px-3 py-2 font-mono text-[0.75rem] uppercase text-primary focus:outline-none focus:border-accent"
                >
                  {VIBE_FILTERS.map((v) => (
                    <option key={v.slug} value={v.slug}>
                      {v.name}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* Desktop View: Pill Filters */}
            <div className="hidden sm:flex flex-wrap items-center gap-2 font-mono text-[0.625rem] uppercase tracking-[0.16em]">
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

          {/* Desktop Vibe Tag Filter Pills */}
          <div className="hidden sm:flex my-4 flex-wrap items-center gap-2 font-mono text-[0.625rem] uppercase tracking-[0.14em]">
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

          {/* MapLibre Map Container */}
          <div className="mt-4">
            <Suspense
              fallback={
                <div className="h-[400px] w-full rounded-2xl bg-neutral-900/60 border border-amber-900/20 flex items-center justify-center text-amber-200/50 animate-pulse">
                  <span className="text-sm font-medium">Loading interactive Cairo map...</span>
                </div>
              }
            >
              <MapLibreMap
                venues={venuesData}
                selectedVenue={selectedFeature}
                onSelectVenue={(venue) => {
                  setSelectedFeature(venue);
                  if (venue) {
                    const idx = carouselVenues.findIndex(
                      (f) => f.properties.id === venue.properties.id
                    );
                    if (idx !== -1) setCarouselIndex(idx);
                  }
                }}
              />
            </Suspense>
          </div>
        </div>
      </section>

      {/* A Good Place to Start Section (3-Venue Carousel) */}
      <section className="mx-auto grid max-w-[1440px] gap-10 px-5 py-16 lg:grid-cols-[0.7fr_1.3fr] lg:px-10 lg:py-24">
        <div className="flex flex-col justify-between gap-8">
          <div>
            {/* Requirement 6.1: "Selected for the night" */}
            <p className="mb-4 font-mono text-[0.6875rem] uppercase tracking-[0.2em] text-accent">
              Selected for the night
            </p>
            <h2 className="font-serif text-5xl leading-[0.9] tracking-[-0.06em] text-primary lg:text-7xl">
              A good place
              <br />
              <em className="font-normal">to begin.</em>
            </h2>
          </div>

          <div className="flex flex-col gap-4">
            <p className="max-w-xs font-serif text-lg leading-relaxed text-muted-foreground">
              Start with the old centre. Let the streets decide what comes next.
            </p>

            {/* Carousel Navigation Controls */}
            {carouselVenues.length > 1 && (
              <div className="flex items-center gap-3">
                <button
                  onClick={handlePrevCarousel}
                  className="flex h-11 w-11 items-center justify-center border border-primary/30 text-primary transition-colors hover:bg-primary hover:text-primary-foreground"
                  aria-label="Previous venue"
                >
                  <ChevronLeft className="size-5" />
                </button>

                <span className="font-mono text-[0.75rem] text-primary/70 uppercase tracking-widest">
                  0{carouselIndex + 1} / 0{carouselVenues.length}
                </span>

                <button
                  onClick={handleNextCarousel}
                  className="flex h-11 w-11 items-center justify-center border border-primary/30 text-primary transition-colors hover:bg-primary hover:text-primary-foreground"
                  aria-label="Next venue"
                >
                  <ChevronRight className="size-5" />
                </button>
              </div>
            )}
          </div>
        </div>

        {selectedProps ? (
          <article className="grid overflow-hidden border border-primary/25 bg-card sm:grid-cols-[0.85fr_1.15fr] min-h-[480px] sm:min-h-[520px]">
            <div
              className="h-full min-h-[260px] sm:min-h-full bg-cover bg-center"
              style={{
                backgroundImage: `url(${
                  selectedProps.photo_url ||
                  "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=900&q=80"
                })`,
              }}
              role="img"
              aria-label={`${getVenueName(selectedProps)} atmosphere`}
            />

            <div className="flex flex-col justify-between gap-6 p-6 lg:p-9 h-full">
              <div>
                {/* Mobile View Layout (8.3): Category, Pricing & Search button top row, Venue Name full width underneath */}
                <div className="mb-4 flex flex-col gap-3">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-[0.6875rem] uppercase tracking-[0.16em] text-accent">
                        {selectedProps.category_name}
                      </span>
                      <span className="font-mono text-[0.6875rem] font-bold text-primary border border-primary/30 px-1.5 py-0.5">
                        {selectedProps.price_range}
                      </span>
                    </div>

                    <button
                      className="border border-primary/30 p-2 min-h-[44px] min-w-[44px] flex items-center justify-center text-primary transition-colors hover:bg-primary hover:text-primary-foreground"
                      aria-label="Search venue details"
                    >
                      <Search className="size-4" />
                    </button>
                  </div>

                  {/* Venue Name full width under category/pricing/search button */}
                  <div className="w-full">
                    <h3 className="font-serif text-3xl sm:text-4xl leading-tight tracking-[-0.05em] text-primary">
                      {getVenueName(selectedProps)}
                    </h3>
                    {selectedProps.name_ar && (
                      <p className="mt-1 font-serif text-lg text-muted-foreground" lang="ar" dir="rtl">
                        {selectedProps.name_ar}
                      </p>
                    )}
                  </div>
                </div>

                <p className="max-w-md font-serif text-lg leading-relaxed text-primary/80 line-clamp-4">
                  {getVenueDescription(selectedProps)}
                </p>
              </div>

              <div>
                <div className="mb-5 flex flex-wrap gap-2">
                  <span className="border border-primary/25 px-3 py-1 font-mono text-[0.625rem] uppercase tracking-[0.13em] text-primary">
                    {selectedProps.vibe_description || "Downtown Vibe"}
                  </span>

                  {selectedProps.vibes &&
                    selectedProps.vibes.map((vibeSlug) => (
                      <span
                        key={vibeSlug}
                        className="border border-accent/40 bg-accent/10 px-2 py-1 font-mono text-[0.625rem] uppercase tracking-[0.13em] text-accent"
                      >
                        #{vibeSlug}
                      </span>
                    ))}

                  {getVenueAddress(selectedProps) && (
                    <span className="border border-primary/25 px-3 py-1 font-mono text-[0.625rem] uppercase tracking-[0.13em] text-primary">
                      <MapPin className="mr-1 inline size-3" /> {getVenueAddress(selectedProps)}
                    </span>
                  )}
                </div>

                <Link
                  to="/venue/$slug"
                  params={{ slug: selectedProps.slug }}
                  className="inline-flex items-center gap-2 font-mono text-[0.75rem] uppercase tracking-[0.16em] text-accent hover:text-primary"
                >
                  Open full listing <ArrowUpRight className="size-3" />
                </Link>
              </div>
            </div>
          </article>
        ) : (
          <div className="flex min-h-[300px] items-center justify-center border border-dashed border-primary/30 p-8 text-center font-mono text-[0.75rem] uppercase tracking-widest text-muted-foreground">
            No venues found matching selected filters. Try clearing filters.
          </div>
        )}
      </section>

      {/* Bar Hops Trail Banner */}
      <section
        id="bar-hops"
        className="border-y border-primary/25 bg-primary px-5 py-16 text-primary-foreground lg:px-10 lg:py-24"
      >
        <div className="mx-auto grid max-w-[1440px] gap-10 lg:grid-cols-[1fr_1fr] lg:items-center">
          <div>
            <p className="mb-5 flex items-center gap-2 font-mono text-[0.6875rem] uppercase tracking-[0.2em] text-accent">
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
            <div className="flex flex-wrap gap-4 font-mono text-[0.75rem] uppercase tracking-[0.16em] text-primary-foreground/70">
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

      {/* Ground Rules & WhatsApp Dispatch Section */}
      <div id="our-guide" className="scroll-mt-12">
        <section className="mx-auto max-w-[1440px] px-5 py-16 lg:px-10 lg:py-24">
          <PersonalCrawlCard
            whatsappNumber={CONTACT_CONFIG.WHATSAPP_NUMBER}
            contactEmail={CONTACT_CONFIG.CONTACT_EMAIL}
          />
        </section>
      </div>

      {/* Footer */}
      <footer id="about" className="border-t border-border px-5 py-8 lg:px-10">
        <div className="mx-auto flex max-w-[1440px] flex-col justify-between gap-5 sm:flex-row sm:items-center">
          <span className="font-serif text-lg font-semibold tracking-[-0.04em] text-primary">
            bar<span className="text-accent">in</span>cairo
          </span>
          <p className="font-mono text-[0.625rem] uppercase tracking-[0.16em] text-muted-foreground">
            Made for the curious · Cairo, Egypt · 2026
          </p>
          <a
            href="#top"
            className="font-mono text-[0.625rem] uppercase tracking-[0.16em] text-muted-foreground hover:text-primary"
          >
            Back to top <ChevronDown className="ml-1 inline size-3 rotate-180" />
          </a>
        </div>
      </footer>
      <ComingSoonModal />
    </main>
  );
}
