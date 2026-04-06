'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { createClient } from '@/lib/supabase/client'
import type { BuildingType, Persona, PlotConfig } from '@/types'
import PlotMapPicker from '@/components/onboarding/PlotMapPicker'

const CLIMATE_ZONES = [
  { id: 'composite', label: 'Composite', desc: 'Bangalore, Pune, Delhi — moderate all year' },
  { id: 'warm_humid', label: 'Warm & Humid', desc: 'Coastal Karnataka, Kerala, Chennai' },
  { id: 'hot_dry', label: 'Hot & Dry', desc: 'Rajasthan, parts of AP/Telangana' },
  { id: 'temperate', label: 'Temperate', desc: 'Coorg, Ooty, Shillong' },
  { id: 'cold', label: 'Cold', desc: 'Himalayan zones, Ladakh' },
]

const SEISMIC_ZONES = [
  { id: 'II', label: 'Zone II', desc: 'Low risk — most of south India' },
  { id: 'III', label: 'Zone III', desc: 'Moderate — Bangalore, coastal zones' },
  { id: 'IV', label: 'Zone IV', desc: 'High — parts of NE India, J&K' },
  { id: 'V', label: 'Zone V', desc: 'Very high — northeast India' },
]

const BUILDING_TYPES: { id: BuildingType; emoji: string; label: string; desc: string }[] = [
  { id: 'residential', emoji: '🏠', label: 'Individual House', desc: 'G, G+1, G+2 independent house. Full 45-decision depth.' },
  { id: 'apartment',   emoji: '🏢', label: 'Apartment Building', desc: 'Multi-unit, RCC frame, fire safety, common MEP.' },
  { id: 'commercial',  emoji: '🏪', label: 'Commercial', desc: 'Warehouse, showroom, or office space.' },
  { id: 'agricultural',emoji: '🌾', label: 'Agricultural', desc: 'Farm shed, poultry, cattle, greenhouse.' },
  { id: 'utility',     emoji: '🚗', label: 'Utility Structure', desc: 'Car shed, outhouse, guard room, garden shed.' },
]

const PERSONAS: { id: Persona; label: string; desc: string; for: BuildingType[] }[] = [
  { id: 'young_it_couple',   label: 'Young IT Couple',      desc: 'WFH-heavy, natural light, acoustic isolation', for: ['residential'] },
  { id: 'joint_family',      label: 'Joint Family',         desc: 'Elderly access, multiple kitchens, privacy gradients', for: ['residential'] },
  { id: 'retired_couple',    label: 'Retired Couple',       desc: 'Single floor, low maintenance, garden', for: ['residential'] },
  { id: 'budget_first_timer',label: 'Budget First-Timer',   desc: 'Optimise total cost of ownership, not just upfront', for: ['residential'] },
  { id: 'investor',          label: 'Investor / Rental',    desc: 'Durability, tenant-proofing over personal comfort', for: ['residential', 'apartment'] },
  { id: 'small_developer',   label: 'Small Developer',      desc: '4–8 units, cost optimisation', for: ['apartment'] },
  { id: 'premium_builder',   label: 'Premium Builder',      desc: '16+ units, amenity-rich', for: ['apartment'] },
  { id: 'small_farmer',      label: 'Small Farmer',         desc: '1–2 acre, budget-critical', for: ['agricultural'] },
]

const ORIENTATIONS = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'] as const

type Step = 'type' | 'plot' | 'parameters' | 'persona' | 'review'

export default function NewBuildPage() {
  const router = useRouter()
  const supabase = createClient()
  const [step, setStep] = useState<Step>('type')
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Form state
  const [buildName, setBuildName] = useState('My Build')
  const [buildingType, setBuildingType] = useState<BuildingType>('residential')
  const [persona, setPersona] = useState<Persona>('young_it_couple')
  const [plotConfig, setPlotConfig] = useState<Partial<PlotConfig>>({
    lat: 12.9716,
    lng: 77.5946,
    climate_zone: 'composite',
    seismic_zone: 'III',
    wind_speed_zone: '33m/s',
    rainfall_mm: 900,
    soil_type: 'red_laterite',
    elevation_m: 920,
    city_tier: 'tier1',
    plot_length_ft: 40,
    plot_width_ft: 60,
    plot_area_sqft: 2400,
    floors: 1,
    road_facing: 'E',
    target_budget_inr: null,
    vastu_enabled: false,
    setback_front_ft: 10,
    setback_side_ft: 5,
    setback_rear_ft: 5,
  })

  function updatePlot(partial: Partial<PlotConfig>) {
    setPlotConfig(prev => {
      const next = { ...prev, ...partial }
      if (partial.plot_length_ft || partial.plot_width_ft) {
        next.plot_area_sqft = (next.plot_length_ft ?? 0) * (next.plot_width_ft ?? 0)
      }
      return next
    })
  }

  async function createBuild() {
    setSaving(true)
    setError(null)
    try {
      const { data: { user } } = await supabase.auth.getUser()
      if (!user) { router.push('/login'); return }

      const { data, error: err } = await supabase
        .from('builds')
        .insert({
          user_id: user.id,
          name: buildName,
          building_type: buildingType,
          persona,
          status: 'draft',
          plot_config: plotConfig,
        })
        .select()
        .single()

      if (err) throw err
      router.push(`/build/${data.id}`)
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Something went wrong')
      setSaving(false)
    }
  }

  const steps: Step[] = ['type', 'plot', 'parameters', 'persona', 'review']
  const stepIdx = steps.indexOf(step)

  return (
    <div className="min-h-screen flex flex-col" style={{ background: '#0d1117' }}>
      {/* Header */}
      <header className="border-b" style={{ borderColor: '#21262d', background: '#161b22' }}>
        <div className="max-w-3xl mx-auto px-4 h-14 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded flex items-center justify-center text-sm font-bold"
              style={{ background: 'linear-gradient(135deg, #4ade80, #22c55e)', color: '#0d1117' }}>ಯ</div>
            <span className="font-semibold text-sm" style={{ color: '#e6edf3' }}>New Build</span>
          </div>
          {/* Progress */}
          <div className="flex items-center gap-1">
            {steps.map((s, i) => (
              <div key={s} className="w-6 h-1.5 rounded-full transition-colors"
                style={{ background: i <= stepIdx ? '#4ade80' : '#30363d' }} />
            ))}
          </div>
        </div>
      </header>

      <main className="flex-1 max-w-3xl mx-auto w-full px-4 py-10">

        {/* Step: Building Type */}
        {step === 'type' && (
          <div>
            <h2 className="text-xl font-bold mb-2" style={{ color: '#e6edf3' }}>What are you building?</h2>
            <p className="text-sm mb-6" style={{ color: '#7d8590' }}>This reshapes the entire decision tree — materials, stages, scoring weights.</p>
            <div className="grid gap-3 mb-6">
              {BUILDING_TYPES.map(t => (
                <button key={t.id} onClick={() => setBuildingType(t.id)}
                  className="flex items-center gap-4 p-4 rounded-xl border text-left transition-all cursor-pointer"
                  style={{
                    background: buildingType === t.id ? '#1c2128' : '#161b22',
                    borderColor: buildingType === t.id ? '#4ade80' : '#30363d',
                  }}>
                  <span className="text-2xl">{t.emoji}</span>
                  <div>
                    <p className="font-medium text-sm" style={{ color: '#e6edf3' }}>{t.label}</p>
                    <p className="text-xs" style={{ color: '#7d8590' }}>{t.desc}</p>
                  </div>
                  {buildingType === t.id && <span className="ml-auto text-green-400">✓</span>}
                </button>
              ))}
            </div>
            <button onClick={() => setStep('plot')}
              className="w-full py-3 rounded-lg font-medium text-sm cursor-pointer"
              style={{ background: '#4ade80', color: '#0d1117' }}>
              Continue →
            </button>
          </div>
        )}

        {/* Step: Plot Location */}
        {step === 'plot' && (
          <div>
            <h2 className="text-xl font-bold mb-2" style={{ color: '#e6edf3' }}>Where is your plot?</h2>
            <p className="text-sm mb-6" style={{ color: '#7d8590' }}>
              Environmental parameters are derived from location — climate zone, seismic zone, rainfall, soil type.
            </p>

            {/* Map */}
            <div className="mb-6">
              <PlotMapPicker
                initialLat={plotConfig.lat ?? 12.9716}
                initialLng={plotConfig.lng ?? 77.5946}
                onLocationChange={(lat, lng, derived) => updatePlot({
                  lat, lng,
                  climate_zone: derived.climate_zone as PlotConfig['climate_zone'],
                  seismic_zone: derived.seismic_zone as PlotConfig['seismic_zone'],
                  rainfall_mm: derived.rainfall_mm,
                })}
              />
            </div>

            {/* Climate zone override */}
            <div className="mb-4">
              <label className="block text-sm font-medium mb-2" style={{ color: '#e6edf3' }}>
                Climate Zone <span className="font-normal text-xs" style={{ color: '#7d8590' }}>— override if auto-detect is wrong</span>
              </label>
              <div className="grid gap-2">
                {CLIMATE_ZONES.map(z => (
                  <button key={z.id} onClick={() => updatePlot({ climate_zone: z.id as PlotConfig['climate_zone'] })}
                    className="flex items-center justify-between px-4 py-2.5 rounded-lg border text-left cursor-pointer"
                    style={{
                      background: plotConfig.climate_zone === z.id ? '#1c2128' : '#161b22',
                      borderColor: plotConfig.climate_zone === z.id ? '#4ade80' : '#30363d',
                    }}>
                    <div>
                      <span className="text-sm font-medium" style={{ color: '#e6edf3' }}>{z.label}</span>
                      <span className="text-xs ml-2" style={{ color: '#7d8590' }}>{z.desc}</span>
                    </div>
                    {plotConfig.climate_zone === z.id && <span className="text-green-400 text-xs">✓</span>}
                  </button>
                ))}
              </div>
            </div>

            {/* Seismic zone */}
            <div className="mb-6">
              <label className="block text-sm font-medium mb-2" style={{ color: '#e6edf3' }}>
                Seismic Zone (IS 1893) <span className="font-normal text-xs" style={{ color: '#7d8590' }}>— override if needed</span>
              </label>
              <div className="grid grid-cols-2 gap-2">
                {SEISMIC_ZONES.map(z => (
                  <button key={z.id} onClick={() => updatePlot({ seismic_zone: z.id as PlotConfig['seismic_zone'] })}
                    className="px-3 py-2 rounded-lg border text-left cursor-pointer"
                    style={{
                      background: plotConfig.seismic_zone === z.id ? '#1c2128' : '#161b22',
                      borderColor: plotConfig.seismic_zone === z.id ? '#4ade80' : '#30363d',
                    }}>
                    <p className="text-sm font-medium" style={{ color: '#e6edf3' }}>{z.label}</p>
                    <p className="text-xs" style={{ color: '#7d8590' }}>{z.desc}</p>
                  </button>
                ))}
              </div>
            </div>

            <div className="flex gap-3">
              <button onClick={() => setStep('type')} className="flex-1 py-3 rounded-lg border text-sm cursor-pointer"
                style={{ borderColor: '#30363d', color: '#7d8590' }}>← Back</button>
              <button onClick={() => setStep('parameters')} className="flex-1 py-3 rounded-lg font-medium text-sm cursor-pointer"
                style={{ background: '#4ade80', color: '#0d1117' }}>Continue →</button>
            </div>
          </div>
        )}

        {/* Step: Building Parameters */}
        {step === 'parameters' && (
          <div>
            <h2 className="text-xl font-bold mb-2" style={{ color: '#e6edf3' }}>Plot & Building Details</h2>
            <p className="text-sm mb-6" style={{ color: '#7d8590' }}>These numbers drive cost estimates and the scoring engine.</p>

            <div className="space-y-4 mb-6">
              {/* Build name */}
              <Field label="Build Name">
                <input value={buildName} onChange={e => setBuildName(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg border text-sm"
                  style={{ background: '#1c2128', borderColor: '#30363d', color: '#e6edf3' }} />
              </Field>

              {/* Plot dimensions */}
              <div className="grid grid-cols-2 gap-3">
                <Field label="Plot Length (ft)">
                  <input type="number" value={plotConfig.plot_length_ft ?? ''} onChange={e => updatePlot({ plot_length_ft: +e.target.value })}
                    className="w-full px-3 py-2 rounded-lg border text-sm"
                    style={{ background: '#1c2128', borderColor: '#30363d', color: '#e6edf3' }} />
                </Field>
                <Field label="Plot Width (ft)">
                  <input type="number" value={plotConfig.plot_width_ft ?? ''} onChange={e => updatePlot({ plot_width_ft: +e.target.value })}
                    className="w-full px-3 py-2 rounded-lg border text-sm"
                    style={{ background: '#1c2128', borderColor: '#30363d', color: '#e6edf3' }} />
                </Field>
              </div>
              <div className="text-xs font-mono" style={{ color: '#4ade80' }}>
                Area: {plotConfig.plot_area_sqft?.toLocaleString()} sqft ({((plotConfig.plot_area_sqft ?? 0) * 0.0929).toFixed(1)} m²)
              </div>

              {/* Floors */}
              <Field label="Number of Floors">
                <div className="flex gap-2">
                  {[1, 2, 3, 4, 5].map(f => (
                    <button key={f} onClick={() => updatePlot({ floors: f })}
                      className="flex-1 py-2 rounded-lg border text-sm font-medium cursor-pointer"
                      style={{
                        background: plotConfig.floors === f ? '#4ade80' : '#1c2128',
                        borderColor: plotConfig.floors === f ? '#4ade80' : '#30363d',
                        color: plotConfig.floors === f ? '#0d1117' : '#7d8590',
                      }}>
                      G{f > 1 ? `+${f - 1}` : ''}
                    </button>
                  ))}
                </div>
              </Field>

              {/* Road facing */}
              <Field label="Road Facing Direction">
                <div className="grid grid-cols-4 gap-2">
                  {ORIENTATIONS.map(o => (
                    <button key={o} onClick={() => updatePlot({ road_facing: o })}
                      className="py-2 rounded-lg border text-xs font-mono cursor-pointer"
                      style={{
                        background: plotConfig.road_facing === o ? '#4ade80' : '#1c2128',
                        borderColor: plotConfig.road_facing === o ? '#4ade80' : '#30363d',
                        color: plotConfig.road_facing === o ? '#0d1117' : '#7d8590',
                      }}>{o}</button>
                  ))}
                </div>
              </Field>

              {/* Budget */}
              <Field label="Target Budget (₹) — optional">
                <input type="number" placeholder="e.g. 4500000"
                  value={plotConfig.target_budget_inr ?? ''}
                  onChange={e => updatePlot({ target_budget_inr: e.target.value ? +e.target.value : null })}
                  className="w-full px-3 py-2 rounded-lg border text-sm"
                  style={{ background: '#1c2128', borderColor: '#30363d', color: '#e6edf3' }} />
                {plotConfig.target_budget_inr && (
                  <p className="text-xs mt-1 font-mono" style={{ color: '#4ade80' }}>
                    ₹{(plotConfig.target_budget_inr / 100000).toFixed(1)}L
                    {plotConfig.plot_area_sqft ? ` · ₹${Math.round(plotConfig.target_budget_inr / (plotConfig.plot_area_sqft * (plotConfig.floors ?? 1)))} /sqft` : ''}
                  </p>
                )}
              </Field>

              {/* Vastu */}
              <div className="flex items-center justify-between p-3 rounded-lg border"
                style={{ background: '#1c2128', borderColor: '#30363d' }}>
                <div>
                  <p className="text-sm font-medium" style={{ color: '#e6edf3' }}>Apply Vastu Guidelines</p>
                  <p className="text-xs" style={{ color: '#7d8590' }}>Overlays Vastu at relevant decision points and flags conflicts with optimal choices</p>
                </div>
                <button onClick={() => updatePlot({ vastu_enabled: !plotConfig.vastu_enabled })}
                  className="w-10 h-6 rounded-full transition-colors relative cursor-pointer"
                  style={{ background: plotConfig.vastu_enabled ? '#4ade80' : '#30363d' }}>
                  <span className="absolute top-1 w-4 h-4 rounded-full transition-transform"
                    style={{ background: '#fff', left: plotConfig.vastu_enabled ? '22px' : '4px' }} />
                </button>
              </div>
            </div>

            <div className="flex gap-3">
              <button onClick={() => setStep('plot')} className="flex-1 py-3 rounded-lg border text-sm cursor-pointer"
                style={{ borderColor: '#30363d', color: '#7d8590' }}>← Back</button>
              <button onClick={() => setStep('persona')} className="flex-1 py-3 rounded-lg font-medium text-sm cursor-pointer"
                style={{ background: '#4ade80', color: '#0d1117' }}>Continue →</button>
            </div>
          </div>
        )}

        {/* Step: Persona */}
        {step === 'persona' && (
          <div>
            <h2 className="text-xl font-bold mb-2" style={{ color: '#e6edf3' }}>Who is this build for?</h2>
            <p className="text-sm mb-6" style={{ color: '#7d8590' }}>
              Persona adjusts score weights and default recommendations. There is no "best" build — only the best build for a specific life situation.
            </p>
            <div className="grid gap-3 mb-6">
              {PERSONAS.filter(p => p.for.includes(buildingType)).map(p => (
                <button key={p.id} onClick={() => setPersona(p.id)}
                  className="flex items-center gap-4 p-4 rounded-xl border text-left cursor-pointer transition-all"
                  style={{
                    background: persona === p.id ? '#1c2128' : '#161b22',
                    borderColor: persona === p.id ? '#4ade80' : '#30363d',
                  }}>
                  <div className="flex-1">
                    <p className="font-medium text-sm" style={{ color: '#e6edf3' }}>{p.label}</p>
                    <p className="text-xs" style={{ color: '#7d8590' }}>{p.desc}</p>
                  </div>
                  {persona === p.id && <span className="text-green-400">✓</span>}
                </button>
              ))}
            </div>
            <div className="flex gap-3">
              <button onClick={() => setStep('parameters')} className="flex-1 py-3 rounded-lg border text-sm cursor-pointer"
                style={{ borderColor: '#30363d', color: '#7d8590' }}>← Back</button>
              <button onClick={() => setStep('review')} className="flex-1 py-3 rounded-lg font-medium text-sm cursor-pointer"
                style={{ background: '#4ade80', color: '#0d1117' }}>Review →</button>
            </div>
          </div>
        )}

        {/* Step: Review */}
        {step === 'review' && (
          <div>
            <h2 className="text-xl font-bold mb-2" style={{ color: '#e6edf3' }}>Ready to build.</h2>
            <p className="text-sm mb-6" style={{ color: '#7d8590' }}>Review your configuration, then dive into the 6 construction stages.</p>

            <div className="rounded-xl border p-5 mb-6 space-y-3" style={{ background: '#161b22', borderColor: '#30363d' }}>
              <ReviewRow label="Build Name" value={buildName} />
              <ReviewRow label="Building Type" value={BUILDING_TYPES.find(t => t.id === buildingType)?.label ?? buildingType} />
              <ReviewRow label="Persona" value={PERSONAS.find(p => p.id === persona)?.label ?? persona} />
              <ReviewRow label="Plot" value={`${plotConfig.plot_length_ft}×${plotConfig.plot_width_ft} ft = ${plotConfig.plot_area_sqft?.toLocaleString()} sqft`} />
              <ReviewRow label="Floors" value={`G${(plotConfig.floors ?? 1) > 1 ? '+' + ((plotConfig.floors ?? 1) - 1) : ''}`} />
              <ReviewRow label="Road Facing" value={plotConfig.road_facing ?? '—'} />
              <ReviewRow label="Climate Zone" value={CLIMATE_ZONES.find(z => z.id === plotConfig.climate_zone)?.label ?? plotConfig.climate_zone ?? '—'} />
              <ReviewRow label="Seismic Zone" value={plotConfig.seismic_zone ?? '—'} />
              <ReviewRow label="Target Budget" value={plotConfig.target_budget_inr ? `₹${(plotConfig.target_budget_inr / 100000).toFixed(1)}L` : 'Not set'} />
              <ReviewRow label="Vastu" value={plotConfig.vastu_enabled ? 'On' : 'Off'} />
            </div>

            {error && (
              <div className="mb-4 p-3 rounded-lg text-sm" style={{ background: '#ef444420', color: '#ef4444' }}>
                {error}
              </div>
            )}

            <div className="flex gap-3">
              <button onClick={() => setStep('persona')} className="flex-1 py-3 rounded-lg border text-sm cursor-pointer"
                style={{ borderColor: '#30363d', color: '#7d8590' }}>← Back</button>
              <button onClick={createBuild} disabled={saving}
                className="flex-1 py-3 rounded-lg font-medium text-sm cursor-pointer disabled:opacity-60"
                style={{ background: '#4ade80', color: '#0d1117' }}>
                {saving ? 'Creating…' : 'Start Building →'}
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div>
      <label className="block text-sm font-medium mb-1.5" style={{ color: '#e6edf3' }}>{label}</label>
      {children}
    </div>
  )
}

function ReviewRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex justify-between text-sm">
      <span style={{ color: '#7d8590' }}>{label}</span>
      <span style={{ color: '#e6edf3' }}>{value}</span>
    </div>
  )
}
