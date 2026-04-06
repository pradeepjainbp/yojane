'use client'

import { useState } from 'react'
import type { DecisionPoint } from '@/types'
import { foundationMaterials } from '@/data/materials-foundation'
import type { MaterialEntry } from '@/types'

const allMaterials: MaterialEntry[] = [...foundationMaterials]

function getMaterial(id: string): MaterialEntry | null {
  return allMaterials.find(m => m.id === id) ?? null
}

const DIFFICULTY_STARS = { 1: '★', 2: '★★', 3: '★★★' }
const DIFFICULTY_LABELS = { 1: 'Easy', 2: 'Moderate', 3: 'Hard' }

interface Props {
  decisionPoint: DecisionPoint
  chosenOptionId: string | null
  stageColor: string
  onSelect: (optionId: string) => void
}

export default function DecisionCard({ decisionPoint: dp, chosenOptionId, stageColor, onSelect }: Props) {
  const [expanded, setExpanded] = useState(dp.classification === 'critical')
  const isCritical = dp.classification === 'critical'
  const isComplete = !!chosenOptionId

  // Gather options with cost data
  const optionsWithData = dp.options.map(id => ({
    id,
    material: getMaterial(id),
    cost: (() => { const m = getMaterial(id); return m ? m.cost_per_unit_material + m.cost_per_unit_labor : null })(),
  }))

  const hasSpectrumData = optionsWithData.filter(o => o.cost !== null).length >= 2
  const chosenMaterial = chosenOptionId ? getMaterial(chosenOptionId) : null

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
          {chosenMaterial && !expanded && (
            <p className="text-xs mt-0.5" style={{ color: stageColor }}>→ {chosenMaterial.name}</p>
          )}
        </div>
        <span className="text-xs flex-shrink-0" style={{ color: '#7d8590' }}>{expanded ? '▲' : '▼'}</span>
      </button>

      {/* Expanded */}
      {expanded && (
        <div className="px-4 pb-4">
          <p className="text-xs mb-5 leading-relaxed" style={{ color: '#7d8590' }}>{dp.description}</p>

          {hasSpectrumData ? (
            <SpectrumPicker
              options={optionsWithData}
              chosenOptionId={chosenOptionId}
              stageColor={stageColor}
              onSelect={onSelect}
            />
          ) : (
            <ListPicker
              options={optionsWithData}
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

// ── Spectrum Picker ────────────────────────────────────────────
function SpectrumPicker({
  options, chosenOptionId, stageColor, onSelect,
}: {
  options: { id: string; material: MaterialEntry | null; cost: number | null }[]
  chosenOptionId: string | null
  stageColor: string
  onSelect: (id: string) => void
}) {
  // Sort by cost ascending; unknowns go to end
  const sorted = [...options].sort((a, b) => {
    if (a.cost === null) return 1
    if (b.cost === null) return -1
    return a.cost - b.cost
  })

  const costs = sorted.map(o => o.cost).filter(Boolean) as number[]
  const minCost = Math.min(...costs)
  const maxCost = Math.max(...costs)
  const costRange = maxCost - minCost || 1

  const chosen = chosenOptionId ? sorted.find(o => o.id === chosenOptionId) : null
  const chosenMaterial = chosen?.material ?? null

  // Colour along the spectrum: green → amber → red
  function spectrumColor(cost: number | null): string {
    if (cost === null) return '#7d8590'
    const t = (cost - minCost) / costRange  // 0 = cheapest, 1 = priciest
    if (t < 0.33) return '#4ade80'
    if (t < 0.66) return '#f59e0b'
    return '#ef4444'
  }

  function pct(cost: number | null): number {
    if (cost === null) return 100
    return ((cost - minCost) / costRange) * 100
  }

  return (
    <div>
      {/* Legend */}
      <div className="flex justify-between text-xs mb-2">
        <span style={{ color: '#4ade80' }}>₹ Cheapest</span>
        <span className="font-mono" style={{ color: '#7d8590' }}>cost per unit</span>
        <span style={{ color: '#ef4444' }}>Most expensive ₹₹₹</span>
      </div>

      {/* Spectrum bar with markers */}
      <div className="relative mb-5" style={{ height: 8 }}>
        <div className="absolute inset-0 rounded-full"
          style={{ background: 'linear-gradient(to right, #4ade8040, #f59e0b40, #ef444440)' }} />
        {sorted.map(opt => {
          const isChosen = opt.id === chosenOptionId
          const color = spectrumColor(opt.cost)
          return (
            <button
              key={opt.id}
              onClick={() => onSelect(opt.id)}
              title={opt.material?.name ?? opt.id}
              className="absolute cursor-pointer transition-all"
              style={{
                left: `${pct(opt.cost)}%`,
                top: '50%',
                width: isChosen ? 20 : 14,
                height: isChosen ? 20 : 14,
                borderRadius: '50%',
                background: isChosen ? color : '#0d1117',
                border: `2px solid ${color}`,
                transform: 'translate(-50%, -50%)',
                zIndex: isChosen ? 10 : 5,
                boxShadow: isChosen ? `0 0 0 4px ${color}30` : 'none',
              }}
            />
          )
        })}
      </div>

      {/* Option buttons — responsive grid, no overlapping */}
      <div className="grid gap-2 mb-4"
        style={{ gridTemplateColumns: `repeat(${Math.min(sorted.length, 3)}, 1fr)` }}>
        {sorted.map(opt => {
          const isChosen = opt.id === chosenOptionId
          const color = spectrumColor(opt.cost)
          return (
            <button key={opt.id} onClick={() => onSelect(opt.id)}
              className="p-2 rounded-lg text-left cursor-pointer transition-all"
              style={{
                background: isChosen ? `${color}20` : '#161b22',
                border: `1px solid ${isChosen ? color : '#30363d'}`,
              }}>
              <p className="text-xs font-medium leading-snug"
                style={{ color: isChosen ? color : '#e6edf3' }}>
                {opt.material?.name ?? opt.id}
              </p>
              {opt.cost !== null && (
                <p className="text-xs font-mono mt-0.5"
                  style={{ color: isChosen ? color : '#7d8590' }}>
                  ₹{opt.cost.toLocaleString()}
                </p>
              )}
            </button>
          )
        })}
      </div>

      {/* Selected option detail card */}
      {chosenMaterial ? (
        <OptionDetail material={chosenMaterial} color={spectrumColor(chosen?.cost ?? null)} stageColor={stageColor} />
      ) : (
        <div className="rounded-lg p-3 text-center text-xs"
          style={{ background: '#1c2128', border: '1px dashed #30363d', color: '#7d8590' }}>
          Click a marker or option above to select
        </div>
      )}

      {/* All options list (collapsed) */}
      <details className="mt-3">
        <summary className="text-xs cursor-pointer" style={{ color: '#7d8590' }}>
          Compare all {sorted.length} options in detail ▾
        </summary>
        <div className="mt-2 space-y-2">
          {sorted.map(opt => {
            if (!opt.material) return null
            const isChosen = opt.id === chosenOptionId
            const color = spectrumColor(opt.cost)
            return (
              <button key={opt.id} onClick={() => onSelect(opt.id)}
                className="w-full text-left p-3 rounded-lg cursor-pointer"
                style={{ background: isChosen ? color + '10' : '#161b22', border: `1px solid ${isChosen ? color : '#30363d'}` }}>
                <div className="flex justify-between items-start">
                  <p className="text-sm font-medium" style={{ color: '#e6edf3' }}>{opt.material.name}</p>
                  <span className="text-xs font-mono" style={{ color }}>₹{opt.cost?.toLocaleString()}/{opt.material.unit.split(' ')[0]}</span>
                </div>
                <p className="text-xs mt-1" style={{ color: '#7d8590' }}>{opt.material.name_local !== opt.material.name ? opt.material.name_local : ''}</p>
                <div className="flex gap-3 mt-1 text-xs font-mono flex-wrap">
                  {opt.material.u_value !== null && <span style={{ color: '#7d8590' }}>U: {opt.material.u_value}</span>}
                  <span style={{ color: '#7d8590' }}>Life: {opt.material.expected_useful_life_years}yr</span>
                </div>
              </button>
            )
          })}
        </div>
      </details>
    </div>
  )
}

// ── Option Detail Card (shown after selection in spectrum) ─────
function OptionDetail({ material: m, color, stageColor }: {
  material: MaterialEntry; color: string; stageColor: string
}) {
  return (
    <div className="rounded-lg p-4" style={{ background: '#1c2128', border: `1px solid ${color}40` }}>
      <div className="flex justify-between items-start mb-3">
        <div>
          <p className="font-semibold text-sm" style={{ color: '#e6edf3' }}>{m.name}</p>
          {m.name_local !== m.name && (
            <p className="text-xs italic" style={{ color: '#7d8590' }}>{m.name_local}</p>
          )}
        </div>
        <div className="text-right">
          <p className="text-sm font-bold font-mono" style={{ color }}>
            ₹{(m.cost_per_unit_material + m.cost_per_unit_labor).toLocaleString()}
          </p>
          <p className="text-xs" style={{ color: '#7d8590' }}>{m.unit}</p>
        </div>
      </div>

      {/* Key specs grid */}
      <div className="grid grid-cols-2 gap-2 mb-3">
        {m.u_value !== null && (
          <Spec label="Thermal (U-value)" value={`${m.u_value} W/m²K`} note="lower = better insulation" />
        )}
        {m.stc_rating !== null && (
          <Spec label="Sound (STC)" value={`${m.stc_rating} dB`} note="higher = quieter" />
        )}
        <Spec label="Expected life" value={`${m.expected_useful_life_years} years`} />
        <Spec label="Carbon footprint" value={`${m.carbon_footprint_kgco2} kg CO₂`} />
        {m.compressive_strength && (
          <Spec label="Compressive strength" value={m.compressive_strength} />
        )}
        {m.water_absorption && (
          <Spec label="Water absorption" value={m.water_absorption} />
        )}
      </div>

      {/* Source */}
      <p className="text-xs mb-3 font-mono" style={{ color: '#7d8590' }}>
        📋 {m.cost_source}
      </p>

      {/* Pros / Cons */}
      <div className="grid grid-cols-2 gap-3 mb-3">
        <div>
          {m.pros.map((p, i) => (
            <p key={i} className="text-xs" style={{ color: '#4ade80' }}>+ {p}</p>
          ))}
        </div>
        <div>
          {m.cons.map((c, i) => (
            <p key={i} className="text-xs" style={{ color: '#ef4444' }}>− {c}</p>
          ))}
        </div>
      </div>

      {/* Myth buster */}
      {m.common_misconception && (
        <div className="p-3 rounded text-xs"
          style={{ background: '#f59e0b10', borderLeft: '2px solid #f59e0b' }}>
          <p className="font-medium mb-1" style={{ color: '#f59e0b' }}>
            💡 Common myth: &ldquo;{m.common_misconception}&rdquo;
          </p>
          <p style={{ color: '#e6edf3' }}>{m.myth_buster_fact}</p>
        </div>
      )}

      {/* Vastu note */}
      {m.vastu_notes && (
        <p className="text-xs mt-2" style={{ color: '#a78bfa' }}>🕉 {m.vastu_notes}</p>
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
      {note && <p className="text-xs" style={{ color: '#7d8590', fontSize: 9 }}>{note}</p>}
    </div>
  )
}

// ── List Picker (fallback when no cost data) ───────────────────
function ListPicker({
  options, chosenOptionId, stageColor, onSelect,
}: {
  options: { id: string; material: MaterialEntry | null; cost: number | null }[]
  chosenOptionId: string | null
  stageColor: string
  onSelect: (id: string) => void
}) {
  return (
    <div className="space-y-2">
      {options.map(opt => {
        const isChosen = opt.id === chosenOptionId
        if (!opt.material) {
          return (
            <button key={opt.id} onClick={() => onSelect(opt.id)}
              className="w-full flex items-center gap-3 p-3 rounded-lg text-left cursor-pointer"
              style={{ background: isChosen ? stageColor + '15' : '#161b22', border: `1px solid ${isChosen ? stageColor : '#30363d'}` }}>
              <div className="flex-1">
                <p className="text-sm font-medium" style={{ color: '#e6edf3' }}>{opt.id}</p>
                <p className="text-xs" style={{ color: '#7d8590' }}>Data coming soon</p>
              </div>
              {isChosen && <span style={{ color: stageColor }}>✓</span>}
            </button>
          )
        }
        return (
          <button key={opt.id} onClick={() => onSelect(opt.id)}
            className="w-full p-3 rounded-lg text-left cursor-pointer"
            style={{ background: isChosen ? stageColor + '10' : '#161b22', border: `1px solid ${isChosen ? stageColor : '#30363d'}` }}>
            <div className="flex justify-between items-start">
              <p className="text-sm font-medium" style={{ color: '#e6edf3' }}>{opt.material.name}</p>
              {isChosen && <span className="text-xs" style={{ color: stageColor }}>✓ Selected</span>}
            </div>
            <p className="text-xs mt-0.5" style={{ color: '#7d8590' }}>{opt.material.name_local}</p>
          </button>
        )
      })}
    </div>
  )
}
