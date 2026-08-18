"use client";

import { lazy, Suspense } from "react";
import { useParams, Link } from "@tanstack/react-router";
import {
  ArrowLeft,
  ArrowUpRight,
  Clock3,
  Compass,
  MapPin,
  Tag,
} from "lucide-react";
import { useVenueDetailQuery } from "@/lib/hooks";
import { getVenueName, getVenueDescription, getVenueAddress } from "@/lib/api";

const MapLibreMap = lazy(() => import("@/components/map/MapLibreMap"));

export default function VenueDetailPage() {
  const params = useParams({ strict: false }) as { slug?: string };
  const slug = params.slug || "";

  const { data: feature, isLoading, error } = useVenueDetailQuery(slug);

  const props = feature?.properties;
  const coordinates = feature?.geometry?.coordinates || [31.2389, 30.0444];
  const [lng, lat] = coordinates;

  const title = getVenueName(props);
  const description = getVenueDescription(props);
  const address = getVenueAddress(props);
  const directionsUrl =
    props?.google_maps_url ||
    `https://www.google.com/maps/search/?api=1&query=${lat},${lng}`;

  if (isLoading) {
    return (
      <main className="min-h-screen bg-background text-foreground flex flex-col items-center justify-center p-6">
        <div className="flex flex-col items-center gap-4">
          <div className="size-10 border-2 border-accent border-t-transparent rounded-full animate-spin"></div>
          <p className="font-mono text-sm uppercase tracking-widest text-muted-foreground">
            Loading establishment details...
          </p>
        </div>
      </main>
    );
  }

  if (error || !feature || !props) {
    return (
      <main className="min-h-screen bg-background text-foreground flex flex-col items-center justify-center p-6">
        <div className="max-w-md text-center border border-border bg-card p-8 shadow-sm">
          <Compass className="size-10 mx-auto text-accent mb-4" />
          <h1 className="font-serif text-2xl font-semibold text-primary mb-2">
            Establishment Not Found
          </h1>
          <p className="text-muted-foreground text-sm mb-6">
            We couldn't locate a venue matching "<span className="font-mono">{slug}</span>" in our index.
          </p>
          <Link
            to="/"
            className="inline-flex items-center gap-2 border border-primary bg-primary px-5 py-2.5 text-sm font-mono uppercase tracking-wider text-primary-foreground transition-colors hover:bg-accent hover:border-accent"
          >
            <ArrowLeft className="size-4" /> Return to Index
          </Link>
        </div>
      </main>
    );
  }

  const singleFeatureCollection = {
    type: "FeatureCollection" as const,
    features: [feature],
  };

  return (
    <main className="min-h-screen bg-background text-foreground">
      {/* Header Navigation */}
      <header className="border-b border-border/70 bg-background/95 sticky top-0 z-30">
        <div className="mx-auto flex max-w-[1440px] items-center justify-between px-5 py-4 lg:px-10">
          <Link to="/" className="group flex items-center gap-3" aria-label="Bar in Cairo home">
            <span className="font-serif text-[1.75rem] font-semibold tracking-[-0.05em] text-primary">
              bar<span className="text-accent">in</span>cairo
            </span>
            <span className="hidden border-l border-border pl-3 font-mono text-[0.6875rem] uppercase tracking-[0.22em] text-muted-foreground sm:block">
              Downtown Index
            </span>
          </Link>

          <Link
            to="/"
            className="flex items-center gap-2 font-mono text-[0.75rem] uppercase tracking-[0.18em] text-muted-foreground transition-colors hover:text-primary"
          >
            <ArrowLeft className="size-4" /> Back to Index
          </Link>
        </div>
      </header>

      {/* Main Container */}
      <div className="mx-auto max-w-[1200px] px-5 py-8 lg:px-10 lg:py-12">
        {/* Top Breadcrumb & Metadata bar */}
        <div className="mb-6 flex flex-wrap items-center justify-between gap-4 border-b border-border pb-4">
          <div className="flex items-center gap-2 font-mono text-[0.75rem] uppercase tracking-wider text-muted-foreground">
            <span>Cairo</span>
            <span>/</span>
            <span>Downtown</span>
            <span>/</span>
            <span className="text-primary font-semibold">{props.category_name}</span>
          </div>

          <div className="flex items-center gap-3">
            <a
              href={directionsUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 border border-primary px-3 py-1.5 font-mono text-[0.75rem] uppercase tracking-wider text-primary transition-colors hover:bg-primary hover:text-primary-foreground"
            >
              Get Directions <ArrowUpRight className="size-3.5" />
            </a>
          </div>
        </div>

        {/* Hero & Title Grid */}
        <div className="grid gap-8 lg:grid-cols-[1.1fr_0.9fr] lg:items-start mb-12">
          {/* Photo Container */}
          <div className="relative aspect-[16/10] overflow-hidden border border-border bg-muted shadow-sm">
            <img
              src={
                props.photo_url ||
                "https://images.unsplash.com/photo-1514933651103-005eec06c04b?auto=format&fit=crop&w=1200&q=80"
              }
              alt={title}
              className="h-full w-full object-cover"
            />
            <div className="absolute left-4 top-4 flex flex-wrap gap-2">
              <span className="border border-background/40 bg-background/90 px-3 py-1 font-mono text-[0.6875rem] uppercase tracking-widest text-primary backdrop-blur-sm">
                {props.category_name}
              </span>
              <span className="border border-background/40 bg-accent px-3 py-1 font-mono text-[0.6875rem] font-bold uppercase tracking-widest text-accent-foreground backdrop-blur-sm">
                {props.price_range}
              </span>
            </div>
          </div>

          {/* Details Column */}
          <div className="flex flex-col justify-between h-full">
            <div>
              <h1 className="font-serif text-3xl font-bold tracking-tight text-primary sm:text-4xl lg:text-5xl mb-3">
                {title}
              </h1>

              {props.vibe_description && (
                <p className="font-serif text-lg italic text-accent mb-6">
                  "{props.vibe_description}"
                </p>
              )}

              {/* Vibe Badges */}
              {props.vibes && props.vibes.length > 0 && (
                <div className="mb-6 flex flex-wrap gap-2">
                  {props.vibes.map((vibe) => (
                    <span
                      key={vibe}
                      className="inline-flex items-center gap-1 border border-border bg-card px-2.5 py-1 font-mono text-[0.6875rem] uppercase tracking-wider text-foreground"
                    >
                      <Tag className="size-3 text-accent" /> {vibe}
                    </span>
                  ))}
                </div>
              )}

              {/* Description */}
              <div className="prose text-foreground/90 font-sans leading-relaxed mb-8">
                <p>{description || "A notable establishment in Downtown Cairo."}</p>
              </div>
            </div>

            {/* Quick Metadata Box */}
            <div className="border border-border bg-card p-5 space-y-3.5">
              <div className="flex items-start gap-3 text-sm">
                <MapPin className="size-4 shrink-0 text-accent mt-0.5" />
                <div>
                  <span className="font-mono text-[0.6875rem] uppercase tracking-widest text-muted-foreground block mb-0.5">
                    Address & Coordinates
                  </span>
                  <span className="font-medium text-foreground">{address}</span>
                  <span className="block font-mono text-[0.6875rem] text-muted-foreground mt-0.5">
                    {lat.toFixed(4)}°N, {lng.toFixed(4)}°E
                  </span>
                </div>
              </div>

              {props.working_hours && (
                <div className="flex items-start gap-3 text-sm border-t border-border/60 pt-3">
                  <Clock3 className="size-4 shrink-0 text-accent mt-0.5" />
                  <div>
                    <span className="font-mono text-[0.6875rem] uppercase tracking-widest text-muted-foreground block mb-0.5">
                      Working Hours
                    </span>
                    <span className="font-medium text-foreground">{props.working_hours}</span>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Embedded Map Section */}
        <section className="mb-12">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="font-serif text-xl font-semibold text-primary">
              Location Map
            </h2>
            <span className="font-mono text-[0.75rem] uppercase tracking-widest text-muted-foreground">
              Downtown Cairo Grid
            </span>
          </div>

          <div className="border border-border">
            <Suspense
              fallback={
                <div className="aspect-[1.8/1] w-full bg-muted flex items-center justify-center font-mono text-xs text-muted-foreground">
                  Loading map viewport...
                </div>
              }
            >
              <MapLibreMap
                venues={singleFeatureCollection}
                selectedVenue={feature}
                onSelectVenue={() => {}}
              />
            </Suspense>
          </div>
        </section>

        {/* Footer CTA */}
        <div className="border-t border-border pt-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <Link
            to="/"
            className="inline-flex items-center gap-2 font-mono text-[0.75rem] uppercase tracking-widest text-muted-foreground hover:text-primary transition-colors"
          >
            <ArrowLeft className="size-4" /> Explore all Downtown venues
          </Link>
          <a
            href={directionsUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 border border-primary bg-primary px-6 py-3 font-mono text-[0.75rem] uppercase tracking-widest text-primary-foreground hover:bg-accent hover:border-accent transition-colors"
          >
            Open in Google Maps <ArrowUpRight className="size-4" />
          </a>
        </div>
      </div>
    </main>
  );
}
