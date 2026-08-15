"use client";

import { useEffect, useRef, useState } from "react";
import type { GeoJSONFeature, GeoJSONFeatureCollection } from "@/lib/api";
import VenueTooltipCard from "./VenueTooltipCard";

interface MapProps {
  venues: GeoJSONFeatureCollection;
  selectedVenue: GeoJSONFeature | null;
  onSelectVenue: (venue: GeoJSONFeature | null) => void;
}

const DOWNTOWN_CAIRO_CENTER: [number, number] = [31.2389, 30.0444];

export default function MapLibreMap({ venues, selectedVenue, onSelectVenue }: MapProps) {
  const mapContainer = useRef<HTMLDivElement>(null);
  const mapRef = useRef<any>(null);
  const markersRef = useRef<any[]>([]);
  const [mapLoaded, setMapLoaded] = useState(false);

  useEffect(() => {
    if (!mapContainer.current || mapRef.current) return;

    let isMounted = true;

    async function initMap() {
      try {
        const maplibre = await import("maplibre-gl");
        import("maplibre-gl/dist/maplibre-gl.css");

        if (!isMounted || !mapContainer.current) return;

        const map = new maplibre.Map({
          container: mapContainer.current,
          style: {
            version: 8,
            name: "Khedivial Vintage Cairo",
            sources: {
              "osm-tiles": {
                type: "raster",
                tiles: ["https://tile.openstreetmap.org/{z}/{x}/{y}.png"],
                tileSize: 256,
                attribution: "© OpenStreetMap contributors",
              },
            },
            layers: [
              {
                id: "osm-tiles-layer",
                type: "raster",
                source: "osm-tiles",
                minzoom: 0,
                maxzoom: 19,
                paint: {
                  "raster-opacity": 0.45,
                  "raster-contrast": 0.15,
                  "raster-saturation": -0.75,
                },
              },
            ],
          },
          center: DOWNTOWN_CAIRO_CENTER,
          zoom: 14.5,
          pitch: 0,
        });

        map.addControl(
          new maplibre.NavigationControl({ showCompass: false }),
          "bottom-right",
        );

        map.on("load", () => {
          if (!isMounted) return;
          mapRef.current = map;
          setMapLoaded(true);
        });
      } catch (err) {
        console.warn("WebGL MapLibre init fallback mode active:", err);
      }
    }

    initMap();

    return () => {
      isMounted = false;
      if (mapRef.current) {
        mapRef.current.remove();
        mapRef.current = null;
      }
    };
  }, []);

  // Sync Markers on Map loaded or venues update
  useEffect(() => {
    if (!mapLoaded || !mapRef.current) return;

    const map = mapRef.current;
    let isMounted = true;

    async function renderMarkers() {
      const maplibre = await import("maplibre-gl");
      if (!isMounted) return;

      // Clear existing markers
      markersRef.current.forEach((m) => m.remove());
      markersRef.current = [];

      // Add markers dynamically
      venues.features.forEach((feature) => {
        const [lng, lat] = feature.geometry.coordinates;

        const el = document.createElement("div");
        el.className = "group relative cursor-pointer focus:outline-none";
        el.style.width = "44px";
        el.style.height = "44px";
        el.style.display = "flex";
        el.style.alignItems = "center";
        el.style.justifyContent = "center";

        const isSelected = selectedVenue?.properties.id === feature.properties.id;

        el.innerHTML = `
          <div class="relative flex items-center justify-center transition-transform duration-200 group-hover:scale-125 ${
            isSelected ? "scale-125 z-20" : "z-10"
          }">
            <span class="block size-6 rounded-full border-2 border-[#ede7d8] ${
              isSelected
                ? "bg-[#24332d] shadow-[0_0_8px_#ad793b]"
                : "bg-[#ad793b] shadow-[0_2px_0_#24332d]"
            }">
              <span class="absolute inset-1 rounded-full border border-[#ede7d8]/60"></span>
            </span>
          </div>
        `;

        el.addEventListener("click", (e) => {
          e.stopPropagation();
          onSelectVenue(feature);
          map.flyTo({ center: [lng, lat], zoom: 15.5, duration: 1000 });
        });

        const marker = new maplibre.Marker({ element: el })
          .setLngLat([lng, lat])
          .addTo(map);
        markersRef.current.push(marker);
      });
    }

    renderMarkers();

    return () => {
      isMounted = false;
    };
  }, [mapLoaded, venues, selectedVenue, onSelectVenue]);

  return (
    <div className="relative aspect-[1.1/1] overflow-hidden border border-primary/20 bg-[#d1c5a8] sm:aspect-[1.8/1] lg:aspect-[2.2/1]">
      <div ref={mapContainer} className="h-full w-full" />
      <span className="pointer-events-none absolute left-4 top-4 z-10 font-mono text-[9px] uppercase tracking-[0.2em] text-primary/80 bg-background/80 px-2 py-1 border border-primary/20">
        Downtown Cairo · WebGL Map
      </span>
      <span className="pointer-events-none absolute top-4 right-4 z-10 font-serif text-lg italic text-primary/80 bg-background/80 px-2 py-0.5 border border-primary/20">
        القاهرة
      </span>

      {/* Render Selected Venue Tooltip Card (Option A) */}
      {selectedVenue && (
        <VenueTooltipCard venue={selectedVenue} onClose={() => onSelectVenue(null)} />
      )}
    </div>
  );
}
