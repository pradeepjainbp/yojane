'use client'

import { useState } from 'react'
import type { Component, DecisionPoint } from '@/types'

const DIFFICULTY_STARS = { 1: '★', 2: '★★', 3: '★★★' }
const DIFFICULTY_LABELS = { 1: 'Easy', 2: 'Moderate', 3: 'Hard' }

interface Props {
  decisionPoint: DecisionPoint
  /** Registry components for this decision's subcategory. Empty = fallback to list-picker. */
  components: Component[]
  chosenOptionId: string | null
  stageColor: string
  onSelect: (optionId: string) => void
}

export default function DecisionCard({ decisionPoint: dp, components, chosenOptionId, stageColor, onSelect }: Props) {
  const [expanded, setExpanded] = useState(dp.classification === 'critical')
  const isCritical = dp.classification === 'critical'
  const isComplete = !!chosenOptionId

  const hasRegistryData = components.length > 0
  const chosenComponent = hasRegistryData
    ? components.find(c => c.component_id === chosenOptionId) ?? null
    : null

  const cardBorder = isComplete
    ? `1px solid ${stageColor}40`
    : isCritical
    ? '1px solid #f59e0b30'
    : '1px solid #30363d'

  return (
    <div className="rounded-xl overflow-hidden transition-all"
      style={{ background: '#0d1117', border: cardBorder }}>

      {/* Header */}
      <button onClick={() => setExpanded(!expanded)}
        className="w-full flex items-start gap-3 p-4 text-left cursor-pointer">
        <div className="mt-0.5 w-4 h-4 rounded-full flex-shrink-0 flex items-center justify-center"
          style={{
            background: isComplete ? stageColor + '30' : isCritical ? '#f59e0b20' : '#1c2128',
            border: `1.5px solid ${isComplete ? stageColor : isCritical ? '#f59e0b' : '#30363d'}`,
          }}>
          {isComplete && <span className="text-xs" style={{ color: stageColor }}>✓</span>}
        </div>

        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-xs font-mono" style={{ color: stageColor }}>{dp.id}</span>
            {isCritical && (
              <span className="text-xs px-1.5 py-0.5 rounded"
                style={{ background: '#f59e0b15', color: '#f59e0b' }}>CRITICAL</span>
            )}
            <span className="text-xs" title={DIFFICULTY_LABELS[dp.difficulty]}
              style={{ color: '#7d8590' }}>{DIFFICULTY_STARS[dp.difficulty]}</span>
            {dp.vastu_relevant && (
              <span className="text-xs" style={{ color: '#a78bfa' }}>🕉 Vastu</span>
            )}
          </div>
          <h3 className="font-medium text-sm mt-0.5" style={{ color: '#e6edf3' }}>{dp.label}</h3>
          {chosenComponent && !expanded && (
            <p className="text-xs mt-0.5" style={{ color: stageColor }}>→ {chosenComponent.display_name}</p>
          )}
          {!hasRegistryData && chosenOptionId && !expanded && (
            <p className="text-xs mt-0.5" style={{ color: stageColor }}>→ {chosenOptionId}</p>
          )}
        </div>
        <span className="text-xs flex-shrink-0" style={{ color: '#7d8590' }}>{expanded ? '▲' : '▼'}</span>
      </button>

      {/* Expanded */}
      {expanded && (
        <div className="px-4 pb-4">
          <p className="text-xs mb-5 leading-relaxed" style={{ color: '#7d8590' }}>{dp.description}</p>

          {hasRegistryData ? (
            <SpectrumPicker
              components={components}
              chosenOptionId={chosenOptionId}
              stageColor={stageColor}
              onSelect={onSelect}
            />
          ) : (
            <ListPicker
              options={dp.options}
              chosenOptionId={chosenOptionId}
              stageColor={stageColor}
              onSelect={onSelect}
            />
          )}
        </div>
      )}
    </div>
  )
}

// ── Spectrum Picker — used when registry components are available ──
function SpectrumPicker({
  components, chosenOptionId, stageColor, onSelect,
}: {
  components: Component[]
  chosenOptionId: string | null
  stageColor: string
  onSelect: (id: string) => void
}) {
  // Already sorted by sort_order from Supabase query
  const n = components.length
  const chosenIdx = components.findIndex(c => c.component_id === chosenOptionId)
  const chosen = chosenIdx >= 0 ? components[chosenIdx] : null

  function stopPct(idx: number): number {
    if (n <= 1) return 50
    return (idx / (n - 1)) * 100
  }

  // Blue (economical) → violet (mid) → gold (premium)
  function stopColor(idx: number): string {
    const t = n <= 1 ? 0 : idx / (n - 1)
    if (t < 0.33) return '#60a5fa'
    if (t < 0.66) return '#a78bfa'
    return '#f59e0b'
  }

  function handleTrackClick(e: React.MouseEvent<HTMLDivElement>) {
    const rect = e.currentTarget.getBoundingClientRect()
    const pct = (e.clientX - rect.left) / rect.width
    const idx = Math.max(0, Math.min(n - 1, Math.round(pct * (n - 1))))
    onSelect(components[idx].component_id)
  }

  return (
    <div>
      {/* Legend */}
      <div className="flex justify-between text-xs mb-4">
        <span style={{ color: '#60a5fa' }}>₹ Economical</span>
        <span style={{ color: '#f59e0b' }}>Premium ✦</span>
      </div>

      {/* Track */}
      <div className="relative px-3 mb-1" style={{ height: 36 }} onClick={handleTrackClick}>

        {/* Base track */}
        <div className="absolute rounded-full" style={{
          top: '50%', left: 12, right: 12, height: 6,
          transform: 'translateY(-50%)',
          background: 'linear-gradient(to right, #60a5fa25, #a78bfa25, #f59e0b25)',
          border: '1px solid #30363d',
          cursor: 'pointer',
        }} />

        {/* Filled portion up to selected */}
        {chosenIdx >= 0 && (
          <div className="absolute rounded-full" style={{
            top: '50%',
            left: 12,
            width: `calc(${stopPct(chosenIdx)}% * (100% - 24px) / 100%)`,
            height: 6,
            transform: 'translateY(-50%)',
            background: `linear-gradient(to right, #4ade80, ${stopColor(chosenIdx)})`,
            transition: 'width 0.25s ease',
            pointerEvents: 'none',
          }} />
        )}

        {/* Stop notches */}
        {components.map((comp, idx) => {
          if (comp.component_id === chosenOptionId) return null
          return (
            <div key={comp.component_id}
              onClick={e => { e.stopPropagation(); onSelect(comp.component_id) }}
              style={{
                position: 'absolute',
                left: `calc(12px + ${stopPct(idx)}% * (100% - 24px) / 100%)`,
                top: '50%',
                transform: 'translate(-50%, -50%)',
                width: 12, height: 12,
                borderRadius: '50%',
                background: '#0d1117',
                border: `2px solid ${stopColor(idx)}`,
                cursor: 'pointer',
                zIndex: 5,
              }} />
          )
        })}

        {/* Puck */}
        {chosenIdx >= 0 && (
          <div style={{
            position: 'absolute',
            left: `calc(12px + ${stopPct(chosenIdx)}% * (100% - 24px) / 100%)`,
            top: '50%',
            transform: 'translate(-50%, -50%)',
            width: 28, height: 28,
            borderRadius: '50%',
            background: stopColor(chosenIdx),
            border: '3px solid #0d1117',
            boxShadow: `0 0 0 4px ${stopColor(chosenIdx)}40, 0 2px 8px rgba(0,0,0,0.6)`,
            transition: 'left 0.25s cubic-bezier(0.34, 1.56, 0.64, 1)',
            zIndex: 10,
            cursor: 'pointer',
            pointerEvents: 'none',
          }} />
        )}
      </div>

      {/* Labels below track */}
      <div className="flex mb-5 px-3">
        {components.map((comp, idx) => {
          const isChosen = comp.component_id === chosenOptionId
          const color = stopColor(idx)
          const align: React.CSSProperties['textAlign'] =
            idx === 0 ? 'left' : idx === n - 1 ? 'right' : 'center'
          return (
            <div key={comp.component_id}
              onClick={() => onSelect(comp.component_id)}
              style={{ flex: 1, textAlign: align, cursor: 'pointer', padding: '0 2px' }}>
              <p style={{
                fontSize: 10, lineHeight: 1.3,
                fontWeight: isChosen ? 600 : 400,
                color: isChosen ? color : '#7d8590',
              }}>
                {comp.display_name}
              </p>
              {comp.base_cost_per_sqft_inr !== null && (
                <p style={{ fontSize: 9, fontFamily: 'monospace', color: isChosen ? color : '#7d8590' }}>
                  ₹{comp.base_cost_per_sqft_inr}/sqft
                </p>
              )}
            </div>
          )
        })}
      </div>

      {/* Selected detail card */}
      {chosen ? (
        <ComponentDetail component={chosen} color={stopColor(chosenIdx)} stageColor={stageColor} />
      ) : (
        <div className="rounded-lg p-3 text-center text-xs"
          style={{ background: '#1c2128', border: '1px dashed #30363d', color: '#7d8590' }}>
          Slide or tap to choose
        </div>
      )}

      {/* Compare all options */}
      <details className="mt-3">
        <summary className="text-xs cursor-pointer" style={{ color: '#7d8590' }}>
          Compare all {n} options in detail ▾
        </summary>
        <div className="mt-2 space-y-2">
          {components.map((comp, idx) => {
            const isChosen = comp.component_id === chosenOptionId
            const color = stopColor(idx)
            const totalCost = (comp.base_cost_per_sqft_inr ?? 0) + (comp.installation_cost_per_sqft_inr ?? 0)
            return (
              <button key={comp.component_id} onClick={() => onSelect(comp.component_id)}
                className="w-full text-left p-3 rounded-lg cursor-pointer"
                style={{ background: isChosen ? color + '10' : '#161b22', border: `1px solid ${isChosen ? color : '#30363d'}` }}>
                <div className="flex justify-between items-start">
                  <p className="text-sm font-medium" style={{ color: '#e6edf3' }}>{comp.display_name}</p>
                  {totalCost > 0 && (
                    <span className="text-xs font-mono" style={{ color }}>₹{totalCost}/sqft</span>
                  )}
                </div>
                {comp.description && (
                  <p className="text-xs mt-1 line-clamp-2" style={{ color: '#7d8590' }}>{comp.description}</p>
                )}
                <div className="flex gap-3 mt-1 text-xs font-mono flex-wrap">
                  {comp.durability_score !== null && (
                    <span style={{ color: '#7d8590' }}>Durability: {comp.durability_score}/10</span>
                  )}
                  {comp.expected_lifespan_years !== null && (
                    <span style={{ color: '#7d8590' }}>Life: {comp.expected_lifespan_years}yr</span>
                  )}
                </div>
              </button>
            )
          })}
        </div>
      </details>
    </div>
  )
}

// ── Component Detail Card (shown after selection) ─────────────
function ComponentDetail({ component: c, color, stageColor }: {
  component: Component; color: string; stageColor: string
}) {
  const pros = c.pros ? c.pros.split(';').map(s => s.trim()).filter(Boolean) : []
  const cons = c.cons ? c.cons.split(';').map(s => s.trim()).filter(Boolean) : []
  const totalCost = (c.base_cost_per_sqft_inr ?? 0) + (c.installation_cost_per_sqft_inr ?? 0)

  return (
    <div className="rounded-lg p-4" style={{ background: '#1c2128', border: `1px solid ${color}40` }}>
      <div className="flex justify-between items-start mb-3">
        <div>
          <p className="font-semibold text-sm" style={{ color: '#e6edf3' }}>{c.display_name}</p>
          {c.spectrum_position && (
            <p className="text-xs italic" style={{ color: '#7d8590' }}>{c.spectrum_position}</p>
          )}
        </div>
        {totalCost > 0 && (
          <div className="text-right">
            <p className="text-sm font-bold font-mono" style={{ color }}>₹{totalCost}/sqft</p>
            <p className="text-xs" style={{ color: '#7d8590' }}>
              {c.base_cost_per_sqft_inr !== null ? `₹${c.base_cost_per_sqft_inr} mat` : ''}
              {c.installation_cost_per_sqft_inr !== null ? ` + ₹${c.installation_cost_per_sqft_inr} labour` : ''}
            </p>
          </div>
        )}
      </div>

      {/* Key specs grid */}
      <div className="grid grid-cols-2 gap-2 mb-3">
        {c.durability_score !== null && (
          <Spec label="Durability" value={`${c.durability_score}/10`} />
        )}
        {c.thermal_resistance_score !== null && (
          <Spec label="Thermal resistance" value={`${c.thermal_resistance_score}/10`} note="higher = better insulation" />
        )}
        {c.acoustic_score !== null && (
          <Spec label="Sound isolation" value={`${c.acoustic_score}/10`} note="higher = quieter" />
        )}
        {c.expected_lifespan_years !== null && (
          <Spec label="Expected life" value={`${c.expected_lifespan_years} years`} />
        )}
        {c.energy_impact_modifier !== null && (
          <Spec
            label="Energy impact"
            value={c.energy_impact_modifier > 0 ? `+${c.energy_impact_modifier} (saves energy)` : `${c.energy_impact_modifier} (uses more)`}
          />
        )}
        {c.maintenance_complexity && (
          <Spec label="Maintenance" value={c.maintenance_complexity} />
        )}
      </div>

      {/* Cost source */}
      {c.cost_source_notes && (
        <p className="text-xs mb-3 font-mono" style={{ color: '#7d8590' }}>
          📋 {c.cost_source_notes}
        </p>
      )}

      {/* Pros / Cons */}
      {(pros.length > 0 || cons.length > 0) && (
        <div className="grid grid-cols-2 gap-3 mb-3">
          <div>{pros.map((p, i) => <p key={i} className="text-xs" style={{ color: '#4ade80' }}>+ {p}</p>)}</div>
          <div>{cons.map((con, i) => <p key={i} className="text-xs" style={{ color: '#ef4444' }}>− {con}</p>)}</div>
        </div>
      )}

      {/* AI advisory notes (domain expert voice) */}
      {c.ai_advisory_notes && (
        <div className="p-3 rounded text-xs mb-3"
          style={{ background: '#818cf810', borderLeft: '2px solid #818cf8' }}>
          <p className="font-medium mb-1" style={{ color: '#818cf8' }}>💡 Expert insight</p>
          <p style={{ color: '#e6edf3' }}>{c.ai_advisory_notes}</p>
        </div>
      )}

      {/* Advisory warning */}
      {c.advisory_message && c.advisory_severity !== 'None' && (
        <div className="p-3 rounded text-xs mb-3"
          style={{
            background: c.advisory_severity === 'Critical' ? '#ef444410' : '#f59e0b10',
            borderLeft: `2px solid ${c.advisory_severity === 'Critical' ? '#ef4444' : '#f59e0b'}`,
          }}>
          <p style={{ color: c.advisory_severity === 'Critical' ? '#ef4444' : '#f59e0b' }}>
            ⚠ {c.advisory_message}
          </p>
        </div>
      )}

      <p className="text-xs mt-2 text-right font-medium" style={{ color: stageColor }}>✓ Selected</p>
    </div>
  )
}

function Spec({ label, value, note }: { label: string; value: string; note?: string }) {
  return (
    <div className="rounded p-2" style={{ background: '#161b22' }}>
      <p className="text-xs" style={{ color: '#7d8590' }}>{label}</p>
      <p className="text-xs font-mono font-medium" style={{ color: '#e6edf3' }}>{value}</p>
      {note && <p style={{ color: '#7d8590', fontSize: 9 }}>{note}</p>}
    </div>
  )
}

// ── List Picker — fallback when no registry data ───────────────
function ListPicker({
  options, chosenOptionId, stageColor, onSelect,
}: {
  options: { id: string; label: string; hint?: string }[]
  chosenOptionId: string | null
  stageColor: string
  onSelect: (id: string) => void
}) {
  return (
    <div className="space-y-2">
      {options.map(opt => {
        const isChosen = opt.id === chosenOptionId
        return (
          <button key={opt.id} onClick={() => onSelect(opt.id)}
            className="w-full flex items-center gap-3 p-3 rounded-lg text-left cursor-pointer"
            style={{ background: isChosen ? stageColor + '15' : '#161b22', border: `1px solid ${isChosen ? stageColor : '#30363d'}` }}>
            <div className="flex-1">
              <p className="text-sm font-medium" style={{ color: '#e6edf3' }}>{opt.label}</p>
              {opt.hint && <p className="text-xs mt-0.5" style={{ color: '#7d8590' }}>{opt.hint}</p>}
            </div>
            {isChosen && <span style={{ color: stageColor }}>✓</span>}
          </button>
        )
      })}
    </div>
  )
}
