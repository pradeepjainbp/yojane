'use client'

import { useEffect, useRef, useState } from 'react'

export interface DerivedLocation {
  climate_zone: string
  seismic_zone: string
  rainfall_mm: number
}

interface Props {
  initialLat: number
  initialLng: number
  onLocationChange: (lat: number, lng: number, derived: DerivedLocation) => void
}

// ── Coordinate-based derivation for India ─────────────────────

function deriveClimateZone(lat: number, lng: number): string {
  if (lat >= 32) return 'cold'
  // Temperate: Coorg, Nilgiris, NE highlands
  if (lat >= 10 && lat <= 13 && lng >= 75 && lng <= 77.5) return 'temperate'
  if (lat >= 25 && lng >= 88 && lat <= 30) return 'temperate'
  // Warm & humid: West coast + East coast
  if (lng <= 76.5 && lat >= 8 && lat <= 20) return 'warm_humid'
  if (lng >= 79.5 && lat >= 8 && lat <= 20) return 'warm_humid'
  // Hot & dry: Rajasthan + interior AP/Telangana
  if (lat >= 24 && lng <= 76) return 'hot_dry'
  if (lat >= 14 && lat <= 18 && lng >= 77 && lng <= 81) return 'hot_dry'
  return 'composite'
}

function deriveSeismicZone(lat: number, lng: number): string {
  if (lat >= 24 && lng >= 90) return 'V'
  if (lat >= 30 || (lat >= 26 && lng >= 87)) return 'IV'
  if ((lat >= 12 && lat <= 15 && lng >= 77 && lng <= 78.5) ||
      (lat >= 18 && lng <= 74)) return 'III'
  return 'II'
}

function estimateRainfall(lat: number, lng: number): number {
  if (lng <= 76.5 && lat >= 8 && lat <= 18) return 2800   // West coast
  if (lng >= 90 && lat >= 22) return 3000                   // Northeast
  if (lat >= 24 && lng <= 75) return 300                    // Rajasthan
  if (lat >= 12 && lat <= 14 && lng >= 77 && lng <= 78) return 900  // Bangalore
  if (lat >= 18 && lat <= 20 && lng >= 72 && lng <= 74) return 2400 // Mumbai
  return 700
}

function derive(lat: number, lng: number): DerivedLocation {
  return {
    climate_zone: deriveClimateZone(lat, lng),
    seismic_zone: deriveSeismicZone(lat, lng),
    rainfall_mm: estimateRainfall(lat, lng),
  }
}

// ── Dark map style ─────────────────────────────────────────────
const DARK_STYLES = [
  { elementType: 'geometry', stylers: [{ color: '#1c2128' }] },
  { elementType: 'labels.text.stroke', stylers: [{ color: '#0d1117' }] },
  { elementType: 'labels.text.fill', stylers: [{ color: '#7d8590' }] },
  { featureType: 'road', elementType: 'geometry', stylers: [{ color: '#30363d' }] },
  { featureType: 'road', elementType: 'geometry.stroke', stylers: [{ color: '#21262d' }] },
  { featureType: 'road', elementType: 'labels.text.fill', stylers: [{ color: '#7d8590' }] },
  { featureType: 'water', elementType: 'geometry', stylers: [{ color: '#0d1117' }] },
  { featureType: 'poi', elementType: 'geometry', stylers: [{ color: '#161b22' }] },
  { featureType: 'poi', elementType: 'labels.text.fill', stylers: [{ color: '#7d8590' }] },
  { featureType: 'administrative', elementType: 'geometry.stroke', stylers: [{ color: '#30363d' }] },
]

export default function PlotMapPicker({ initialLat, initialLng, onLocationChange }: Props) {
  const mapDivRef = useRef<HTMLDivElement>(null)
  const [mapLoaded, setMapLoaded] = useState(false)
  const [currentLat, setCurrentLat] = useState(initialLat)
  const [currentLng, setCurrentLng] = useState(initialLng)
  const [detected, setDetected] = useState<DerivedLocation>(derive(initialLat, initialLng))

  useEffect(() => {
    const apiKey = process.env.NEXT_PUBLIC_GOOGLE_MAPS_KEY
    if (!apiKey) return

    // Already loaded
    if ((window as { google?: unknown }).google) {
      setMapLoaded(true)
      return
    }

    // Script already injected
    if (document.getElementById('gmap-script')) return

    ;(window as { __gmapInit?: () => void }).__gmapInit = () => setMapLoaded(true)

    const script = document.createElement('script')
    script.id = 'gmap-script'
    script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=places&callback=__gmapInit`
    script.async = true
    document.head.appendChild(script)

    return () => {
      delete (window as { __gmapInit?: () => void }).__gmapInit
    }
  }, [])

  useEffect(() => {
    if (!mapLoaded || !mapDivRef.current) return

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const g = (window as any).google.maps

    const map = new g.Map(mapDivRef.current, {
      center: { lat: initialLat, lng: initialLng },
      zoom: 15,
      disableDefaultUI: true,
      zoomControl: true,
      styles: DARK_STYLES,
    })

    const marker = new g.Marker({
      position: { lat: initialLat, lng: initialLng },
      map,
      draggable: true,
      title: 'Drag to your exact plot',
      icon: {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        path: (g.SymbolPath as any).CIRCLE,
        fillColor: '#4ade80',
        fillOpacity: 1,
        strokeColor: '#0d1117',
        strokeWeight: 3,
        scale: 10,
      },
    })

    function applyNewPos(lat: number, lng: number) {
      setCurrentLat(lat)
      setCurrentLng(lng)
      const d = derive(lat, lng)
      setDetected(d)
      onLocationChange(lat, lng, d)
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    marker.addListener('dragend', () => {
      const p = marker.getPosition()
      if (p) applyNewPos(p.lat(), p.lng())
    })

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    map.addListener('click', (e: any) => {
      if (!e.latLng) return
      marker.setPosition(e.latLng)
      applyNewPos(e.latLng.lat(), e.latLng.lng())
    })

    // Places Autocomplete
    const input = document.getElementById('plot-search') as HTMLInputElement | null
    if (input) {
      const ac = new g.places.Autocomplete(input, {
        componentRestrictions: { country: 'in' },
        fields: ['geometry', 'name'],
      })
      ac.addListener('place_changed', () => {
        const place = ac.getPlace()
        if (!place.geometry?.location) return
        const lat = place.geometry.location.lat()
        const lng = place.geometry.location.lng()
        map.panTo({ lat, lng })
        map.setZoom(16)
        marker.setPosition({ lat, lng })
        applyNewPos(lat, lng)
      })
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [mapLoaded])

  const CLIMATE_LABELS: Record<string, string> = {
    composite: 'Composite', warm_humid: 'Warm & Humid',
    hot_dry: 'Hot & Dry', temperate: 'Temperate', cold: 'Cold',
  }

  return (
    <div>
      {/* Search bar */}
      <input
        id="plot-search"
        type="text"
        placeholder="Search your plot address…"
        className="w-full px-3 py-2.5 rounded-lg text-sm mb-2"
        style={{ background: '#1c2128', border: '1px solid #30363d', color: '#e6edf3' }}
      />

      {/* Map */}
      <div ref={mapDivRef} className="rounded-xl overflow-hidden mb-3"
        style={{ height: 280, background: '#1c2128', border: '1px solid #30363d' }}>
        {!mapLoaded && (
          <div className="h-full flex flex-col items-center justify-center gap-2">
            <div className="w-6 h-6 rounded-full border-2 border-t-transparent animate-spin"
              style={{ borderColor: '#4ade80', borderTopColor: 'transparent' }} />
            <p className="text-xs" style={{ color: '#7d8590' }}>Loading map…</p>
          </div>
        )}
      </div>

      {/* Auto-detected values */}
      <div className="rounded-lg p-3 text-xs"
        style={{ background: '#161b22', border: '1px solid #30363d' }}>
        <p className="font-medium mb-2" style={{ color: '#7d8590' }}>
          📍 Auto-detected from pin · <span className="font-mono">{currentLat.toFixed(4)}, {currentLng.toFixed(4)}</span>
        </p>
        <div className="grid grid-cols-3 gap-2">
          <div>
            <p style={{ color: '#7d8590' }}>Climate</p>
            <p className="font-medium" style={{ color: '#4ade80' }}>{CLIMATE_LABELS[detected.climate_zone] ?? detected.climate_zone}</p>
          </div>
          <div>
            <p style={{ color: '#7d8590' }}>Seismic</p>
            <p className="font-medium" style={{ color: '#4ade80' }}>Zone {detected.seismic_zone}</p>
          </div>
          <div>
            <p style={{ color: '#7d8590' }}>Rainfall</p>
            <p className="font-medium" style={{ color: '#4ade80' }}>{detected.rainfall_mm} mm/yr</p>
          </div>
        </div>
        <p className="mt-2" style={{ color: '#7d8590' }}>
          Tap the map or drag the pin to your exact plot. Override below if needed.
        </p>
      </div>
    </div>
  )
}
