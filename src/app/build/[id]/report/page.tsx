import { redirect, notFound } from 'next/navigation'
import { createClient } from '@/lib/supabase/server'
import Link from 'next/link'
import { allDecisions } from '@/data/decision-points'
import { calculateTCOBreakdown } from '@/engine/scoring'
import DownloadPdfButton from '@/components/simulator/DownloadPdfButton'
import type { Build, Component, Decision, BuildScores } from '@/types'

export default async function ReportPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) redirect('/login')

  const [{ data: build }, { data: decisions }, { data: scores }, { data: components }] = await Promise.all([
    supabase.from('builds').select('*').eq('id', id).eq('user_id', user.id).single(),
    supabase.from('decisions').select('*').eq('build_id', id).order('decision_id'),
    supabase.from('build_scores').select('*').eq('build_id', id).single(),
    supabase.from('components').select('*').eq('status', 'Active'),
  ])

  if (!build) notFound()

  const b     = build as Build
  const decs  = (decisions ?? []) as Decision[]
  const s     = scores as BuildScores | null
  const comps = (components ?? []) as Component[]

  // Index components by component_id for O(1) lookup
  const compById = Object.fromEntries(comps.map(c => [c.component_id, c]))

  // Pre-compute TCO breakdown for the report
  const tcoBreakdown = calculateTCOBreakdown(decs, b.plot_config, comps)

  const criticalDecisions  = allDecisions.filter(d => d.classification === 'critical')
  const completedCritical  = criticalDecisions.filter(d => decs.some(dec => dec.decision_id === d.id))

  return (
    <div className="min-h-screen" style={{ background: '#0d1117' }}>
      {/* Header */}
      <header style={{ borderBottom: '1px solid #21262d', background: '#161b22' }}>
        <div className="max-w-4xl mx-auto px-4 h-14 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Link href="/dashboard" className="text-sm" style={{ color: '#7d8590' }}>← Builds</Link>
            <span style={{ color: '#30363d' }}>|</span>
            <span className="text-sm font-semibold" style={{ color: '#e6edf3' }}>{b.name} — Report</span>
          </div>
          <div className="flex gap-2">
            <Link href={`/build/${id}`}
              className="px-3 py-1.5 rounded-lg text-xs"
              style={{ border: '1px solid #30363d', color: '#7d8590' }}>
              ← Back to Simulator
            </Link>
            <DownloadPdfButton buildName={b.name} />
          </div>
        </div>
      </header>

      <main id="yojane-report" className="max-w-4xl mx-auto px-4 py-8 space-y-8">

        {/* Hero */}
        <div className="rounded-2xl p-8 text-center"
          style={{ background: 'linear-gradient(135deg, #0d1f0d, #1a2e1a)', border: '1px solid #4ade8030' }}>
          <div className="text-4xl mb-3">🏗</div>
          <h1 className="text-2xl font-bold mb-1" style={{ color: '#e6edf3' }}>{b.name}</h1>
          <p className="text-sm mb-4" style={{ color: '#7d8590' }}>
            {b.plot_config?.plot_area_sqft?.toLocaleString()} sqft ·{' '}
            G{(b.plot_config?.floors ?? 1) > 1 ? `+${(b.plot_config?.floors ?? 1) - 1}` : ''} ·{' '}
            {b.plot_config?.road_facing} facing ·{' '}
            {b.plot_config?.climate_zone?.replace('_', ' ')}
          </p>
          <p className="text-xs font-mono" style={{ color: '#4ade80' }}>
            {completedCritical.length} of {criticalDecisions.length} critical decisions · {decs.length} total decisions
          </p>
        </div>

        {/* Score Cards */}
        {s && (
          <section>
            <h2 className="text-sm font-semibold uppercase tracking-widest mb-4" style={{ color: '#7d8590' }}>
              Build Scores
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              <ScoreCard label="Comfort"    value={`${s.comfort}/100`}             color="#4ade80" icon="🌡" desc="Thermal · Light · Ventilation · Acoustic · Spatial" />
              <ScoreCard label="Durability" value={`${s.durability}/100`}          color="#60a5fa" icon="🏛" desc="Expected life across all components" />
              <ScoreCard label="Resilience" value={`${s.resilience}/100`}          color="#a78bfa" icon="🛡" desc="Monsoon · Seismic · Wind · Termite" />
              <ScoreCard label="20-yr TCO"  value={`₹${s.tco?.toLocaleString()}/sqft`} color="#f59e0b" icon="💰" desc="Construction + maintenance + energy" />
              <ScoreCard label="Carbon"     value={`${s.carbon} kg/sqft`}          color="#a3e635" icon="🌿" desc="Embodied + 20-yr operational CO₂" />
              {b.plot_config?.target_budget_inr && (
                <ScoreCard label="Target Budget" value={`₹${(b.plot_config.target_budget_inr / 100000).toFixed(1)}L`} color="#e6edf3" icon="🎯" desc="Your stated budget" />
              )}
            </div>
          </section>
        )}

        {/* Section A: Project Summary */}
        <section>
          <SectionHeader letter="A" title="Project Summary" />
          <div className="rounded-xl p-5 grid grid-cols-2 md:grid-cols-3 gap-4"
            style={{ background: '#161b22', border: '1px solid #30363d' }}>
            {[
              ['Building Type', b.building_type],
              ['Persona', b.persona?.replace(/_/g, ' ') ?? '—'],
              ['Plot Size', `${b.plot_config?.plot_length_ft}×${b.plot_config?.plot_width_ft} ft`],
              ['Built-up Area', `${b.plot_config?.plot_area_sqft?.toLocaleString()} sqft`],
              ['Floors', `G${(b.plot_config?.floors ?? 1) > 1 ? '+' + ((b.plot_config?.floors ?? 1) - 1) : ''}`],
              ['Orientation', `${b.plot_config?.road_facing} facing road`],
              ['Climate Zone', b.plot_config?.climate_zone?.replace('_', ' ') ?? '—'],
              ['Seismic Zone', b.plot_config?.seismic_zone ?? '—'],
              ['Vastu', b.plot_config?.vastu_enabled ? 'Enabled' : 'Disabled'],
            ].map(([k, v]) => (
              <div key={k}>
                <p className="text-xs" style={{ color: '#7d8590' }}>{k}</p>
                <p className="text-sm font-medium capitalize" style={{ color: '#e6edf3' }}>{v}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Section B: Decision Log */}
        <section>
          <SectionHeader letter="B" title="Decision Log" />
          <div className="space-y-2">
            {(['A', 'B', 'C', 'D', 'E', 'F'] as const).map(stage => {
              const stageDecs = decs.filter(d => d.stage === stage)
              if (stageDecs.length === 0) return null
              const stageLabels: Record<string, string> = {
                A: 'Foundation', B: 'Walls', C: 'Roofing', D: 'Interiors', E: 'MEP', F: 'Landscape'
              }
              const stageColors: Record<string, string> = {
                A: '#f59e0b', B: '#60a5fa', C: '#818cf8', D: '#f472b6', E: '#34d399', F: '#a3e635'
              }
              return (
                <div key={stage} className="rounded-xl overflow-hidden" style={{ border: '1px solid #30363d' }}>
                  <div className="px-4 py-2.5 flex items-center gap-2" style={{ background: '#1c2128' }}>
                    <span className="text-xs font-mono font-bold" style={{ color: stageColors[stage] }}>{stage}</span>
                    <span className="text-xs font-medium" style={{ color: '#e6edf3' }}>{stageLabels[stage]}</span>
                    <span className="text-xs ml-auto" style={{ color: '#7d8590' }}>{stageDecs.length} decisions</span>
                  </div>
                  <div className="divide-y" style={{ borderColor: '#21262d' }}>
                    {stageDecs.map(dec => {
                      const dp   = allDecisions.find(d => d.id === dec.decision_id)
                      const comp = compById[dec.chosen_option_id] ?? null
                      const totalCost = comp
                        ? (comp.base_cost_per_sqft_inr ?? 0) + (comp.installation_cost_per_sqft_inr ?? 0)
                        : null
                      return (
                        <div key={dec.decision_id} className="px-4 py-3 flex items-start justify-between gap-4">
                          <div className="flex-1">
                            <div className="flex items-center gap-2 flex-wrap">
                              <span className="text-xs font-mono" style={{ color: stageColors[stage] }}>
                                {dec.decision_id}
                              </span>
                              {dp?.classification === 'critical' && (
                                <span className="text-xs px-1.5 rounded"
                                  style={{ background: '#f59e0b15', color: '#f59e0b' }}>CRITICAL</span>
                              )}
                              <span className="text-xs" style={{ color: '#e6edf3' }}>{dp?.label}</span>
                            </div>
                            <p className="text-xs mt-0.5" style={{ color: '#7d8590' }}>
                              → {comp?.display_name ?? dec.chosen_option_id}
                            </p>
                            {comp?.durability_score !== null && comp && (
                              <p className="text-xs mt-0.5 font-mono" style={{ color: '#7d8590' }}>
                                Durability {comp.durability_score}/10 · Life {comp.expected_lifespan_years}yr
                              </p>
                            )}
                          </div>
                          {totalCost !== null && totalCost > 0 && (
                            <div className="text-right flex-shrink-0">
                              <p className="text-xs font-mono" style={{ color: '#e6edf3' }}>₹{totalCost}/sqft</p>
                              <p className="text-xs" style={{ color: '#7d8590' }}>mat + labour</p>
                            </div>
                          )}
                        </div>
                      )
                    })}
                  </div>
                </div>
              )
            })}
          </div>
        </section>

        {/* Section C: Cost Breakdown */}
        <section>
          <SectionHeader letter="C" title="Cost Estimate Breakdown" />

          {/* How it's calculated */}
          <div className="rounded-xl p-4 mb-4 text-xs"
            style={{ background: '#161b2210', border: '1px solid #f59e0b30' }}>
            <p className="font-medium mb-1" style={{ color: '#f59e0b' }}>How this estimate is calculated</p>
            <p style={{ color: '#7d8590' }}>
              Each material&apos;s registry cost (₹/sqft of its own area) is scaled to your built-up area of{' '}
              <span style={{ color: '#e6edf3' }}>{(b.plot_config.plot_area_sqft * b.plot_config.floors).toLocaleString()} sqft</span>.
              Small-area items (windows, doors, waterproofing) apply a coverage fraction so they aren&apos;t overstated.
              Running costs use a 7% discount rate over 20 years.
              This is an indicative estimate — contractor quotes may vary ±20%.
            </p>
          </div>

          {/* TCO breakdown table */}
          <div className="rounded-xl overflow-hidden mb-4" style={{ border: '1px solid #30363d' }}>
            <div className="px-4 py-2.5" style={{ background: '#1c2128', borderBottom: '1px solid #30363d' }}>
              <p className="text-xs font-semibold" style={{ color: '#e6edf3' }}>20-Year Cost Breakdown</p>
            </div>
            {[
              {
                label: 'Year 0 — Construction Cost',
                hint: `${tcoBreakdown.componentCount} chosen materials × built-up area (with coverage factors)`,
                value: `₹${(tcoBreakdown.constructionCostTotal / 100000).toFixed(2)} L`,
                subvalue: `₹${tcoBreakdown.constructionCostPerSqft.toLocaleString()}/sqft`,
                color: '#60a5fa',
              },
              {
                label: 'Annual Maintenance',
                hint: `Avg ${(tcoBreakdown.avgMaintFactor * 100).toFixed(1)}% of construction cost/yr (minor repairs, servicing)`,
                value: `₹${(tcoBreakdown.annualMaint / 1000).toFixed(0)}K / year`,
                subvalue: null,
                color: '#a78bfa',
              },
              {
                label: 'Annual Energy Cost',
                hint: `Base 1,800 kWh/1000sqft at ₹7.5/kWh BESCOM · energy modifier: ${tcoBreakdown.avgEnergyMod > 0 ? '+' : ''}${tcoBreakdown.avgEnergyMod}`,
                value: `₹${(tcoBreakdown.annualEnergy / 1000).toFixed(0)}K / year`,
                subvalue: null,
                color: '#a78bfa',
              },
              {
                label: '20-yr Running Costs (PV at 7%)',
                hint: 'Present value of all maintenance + energy over 20 years',
                value: `₹${(tcoBreakdown.pv20yrRunning / 100000).toFixed(2)} L`,
                subvalue: null,
                color: '#f59e0b',
              },
              {
                label: 'Total 20-yr TCO',
                hint: 'Construction + 20-yr running costs',
                value: `₹${(tcoBreakdown.tco20yrTotal / 100000).toFixed(2)} L`,
                subvalue: `₹${tcoBreakdown.tcoPerSqft.toLocaleString()}/sqft`,
                color: '#4ade80',
              },
            ].map(row => (
              <div key={row.label} className="px-4 py-3 flex justify-between items-start gap-4"
                style={{ borderBottom: '1px solid #21262d' }}>
                <div>
                  <p className="text-sm font-medium" style={{ color: '#e6edf3' }}>{row.label}</p>
                  <p className="text-xs mt-0.5" style={{ color: '#7d8590' }}>{row.hint}</p>
                </div>
                <div className="text-right flex-shrink-0">
                  <p className="text-sm font-bold font-mono" style={{ color: row.color }}>{row.value}</p>
                  {row.subvalue && <p className="text-xs font-mono" style={{ color: '#7d8590' }}>{row.subvalue}</p>}
                </div>
              </div>
            ))}
          </div>

          {/* Budget comparison */}
          {b.plot_config.target_budget_inr && (() => {
            const budget = b.plot_config.target_budget_inr!
            const constr = tcoBreakdown.constructionCostTotal
            const diff = constr - budget
            const pct = Math.round((diff / budget) * 100)
            const over = diff > 0
            return (
              <div className="rounded-xl p-4" style={{
                background: over ? '#ef444410' : '#4ade8010',
                border: `1px solid ${over ? '#ef444430' : '#4ade8030'}`,
              }}>
                <div className="flex justify-between items-center">
                  <div>
                    <p className="text-sm font-medium" style={{ color: over ? '#ef4444' : '#4ade80' }}>
                      {over ? `₹${(Math.abs(diff) / 100000).toFixed(1)}L over budget` : `₹${(Math.abs(diff) / 100000).toFixed(1)}L under budget`}
                    </p>
                    <p className="text-xs mt-0.5" style={{ color: '#7d8590' }}>
                      Construction estimate vs your target budget of ₹{(budget / 100000).toFixed(1)}L
                    </p>
                  </div>
                  <span className="text-2xl font-bold font-mono" style={{ color: over ? '#ef4444' : '#4ade80' }}>
                    {over ? '+' : ''}{pct}%
                  </span>
                </div>
              </div>
            )
          })()}

          {/* Per-stage material cost breakdown */}
          <div className="mt-4 rounded-xl overflow-hidden" style={{ border: '1px solid #30363d' }}>
            <div className="px-4 py-2.5" style={{ background: '#1c2128', borderBottom: '1px solid #30363d' }}>
              <p className="text-xs font-semibold" style={{ color: '#e6edf3' }}>Construction Cost by Stage</p>
            </div>
            {(['A', 'B', 'C', 'D', 'E', 'F'] as const).map(stage => {
              const stageLabels: Record<string, string> = {
                A: 'Foundation', B: 'Walls', C: 'Roofing', D: 'Interiors', E: 'MEP', F: 'Landscape',
              }
              const stageColors: Record<string, string> = {
                A: '#f59e0b', B: '#60a5fa', C: '#818cf8', D: '#f472b6', E: '#34d399', F: '#a3e635',
              }
              const { AREA_FRACTION_EXPORT } = { AREA_FRACTION_EXPORT: { D5: 0.04, D6: 0.06, D7: 0.03, D8: 0.05, D9: 0.10, C4: 0.30 } }
              const stageDecs = decs.filter(d => d.stage === stage)
              const stageTotal = stageDecs.reduce((sum, dec) => {
                const comp = compById[dec.chosen_option_id]
                if (!comp) return sum
                const fraction = AREA_FRACTION_EXPORT[dec.decision_id as keyof typeof AREA_FRACTION_EXPORT] ?? 1.0
                return sum + ((comp.base_cost_per_sqft_inr ?? 0) + (comp.installation_cost_per_sqft_inr ?? 0)) * fraction * b.plot_config.plot_area_sqft * b.plot_config.floors
              }, 0)
              if (stageDecs.length === 0) return null
              return (
                <div key={stage} className="px-4 py-2.5 flex justify-between items-center"
                  style={{ borderBottom: '1px solid #21262d' }}>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono font-bold" style={{ color: stageColors[stage] }}>{stage}</span>
                    <span className="text-xs" style={{ color: '#e6edf3' }}>{stageLabels[stage]}</span>
                    <span className="text-xs" style={{ color: '#7d8590' }}>({stageDecs.length} items)</span>
                  </div>
                  <span className="text-sm font-bold font-mono" style={{ color: stageColors[stage] }}>
                    ₹{(stageTotal / 100000).toFixed(2)} L
                  </span>
                </div>
              )
            })}
          </div>
        </section>

        {/* Section D: Maintenance Calendar */}
        <section>
          <SectionHeader letter="D" title="20-Year Maintenance Guide" />
          <div className="rounded-xl p-5" style={{ background: '#161b22', border: '1px solid #30363d' }}>
            {(() => {
              const rows = decs
                .map(dec => {
                  const comp = compById[dec.chosen_option_id]
                  const dp   = allDecisions.find(d => d.id === dec.decision_id)
                  if (!comp || !comp.major_maintenance_cycle_years) return null
                  return (
                    <div key={dec.decision_id} className="flex items-center justify-between py-2"
                      style={{ borderBottom: '1px solid #21262d' }}>
                      <div>
                        <span className="text-xs font-mono px-2 py-0.5 rounded mr-3"
                          style={{ background: '#1c2128', color: '#f59e0b' }}>
                          Every {comp.major_maintenance_cycle_years}yr
                        </span>
                        <span className="text-xs" style={{ color: '#e6edf3' }}>{dp?.label}</span>
                        <span className="text-xs ml-2" style={{ color: '#7d8590' }}>({comp.display_name})</span>
                      </div>
                      <span className="text-xs font-mono capitalize" style={{ color: '#4ade80' }}>
                        {comp.maintenance_complexity ?? 'Medium'} effort
                      </span>
                    </div>
                  )
                })
                .filter(Boolean)

              if (rows.length === 0) {
                return (
                  <p className="text-xs text-center py-4" style={{ color: '#7d8590' }}>
                    Maintenance data will appear here once the components table is populated in Supabase.
                  </p>
                )
              }
              return rows
            })()}
          </div>
        </section>

        {/* CTA */}
        <div className="rounded-xl p-6 text-center" style={{ background: '#161b22', border: '1px solid #30363d' }}>
          <p className="text-sm mb-4" style={{ color: '#7d8590' }}>
            Share this report with your contractor, or fork it to explore alternatives.
          </p>
          <div className="flex gap-3 justify-center">
            <Link href={`/build/${id}`}
              className="px-4 py-2.5 rounded-lg text-sm"
              style={{ border: '1px solid #30363d', color: '#7d8590' }}>
              ← Back to Simulator
            </Link>
            <Link href="/dashboard/new"
              className="px-4 py-2.5 rounded-lg text-sm font-medium"
              style={{ background: '#4ade8020', border: '1px solid #4ade8040', color: '#4ade80' }}>
              + New Build Variant
            </Link>
          </div>
        </div>

      </main>
    </div>
  )
}

function ScoreCard({ label, value, color, icon, desc }: {
  label: string; value: string; color: string; icon: string; desc: string
}) {
  return (
    <div className="rounded-xl p-4" style={{ background: '#161b22', border: '1px solid #30363d' }}>
      <div className="flex items-center gap-2 mb-2">
        <span>{icon}</span>
        <span className="text-xs" style={{ color: '#7d8590' }}>{label}</span>
      </div>
      <p className="text-xl font-bold font-mono" style={{ color }}>{value}</p>
      <p className="text-xs mt-1" style={{ color: '#7d8590' }}>{desc}</p>
    </div>
  )
}

function SectionHeader({ letter, title }: { letter: string; title: string }) {
  return (
    <div className="flex items-center gap-3 mb-4">
      <span className="w-7 h-7 rounded flex items-center justify-center text-xs font-bold font-mono"
        style={{ background: '#4ade8020', color: '#4ade80', border: '1px solid #4ade8040' }}>
        {letter}
      </span>
      <h2 className="text-base font-semibold" style={{ color: '#e6edf3' }}>{title}</h2>
    </div>
  )
}
