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

// ── Snap Slider Picker ─────────────────────────────────────────
function SpectrumPicker({
  options, chosenOptionId, stageColor, onSelect,
}: {
  options: { id: string; material: MaterialEntry | null; cost: number | null }[]
  chosenOptionId: string | null
  stageColor: string
  onSelect: (id: string) => void
}) {
  // Sort cheapest → priciest
  const sorted = [...options].sort((a, b) => {
    if (a.cost === null) return 1
    if (b.cost === null) return -1
    return a.cost - b.cost
  })

  const n = sorted.length
  const chosenIdx = sorted.findIndex(o => o.id === chosenOptionId)
  const chosen = chosenIdx >= 0 ? sorted[chosenIdx] : null
  const chosenMaterial = chosen?.material ?? null

  // Equidistant position for each stop (0–100%)
  function stopPct(idx: number): number {
    if (n <= 1) return 50
    return (idx / (n - 1)) * 100
  }

  // Color by position: green → amber → red
  function stopColor(idx: number): string {
    const t = n <= 1 ? 0 : idx / (n - 1)
    if (t < 0.33) return '#4ade80'
    if (t < 0.66) return '#f59e0b'
    return '#ef4444'
  }

  // Click anywhere on track → snap to nearest stop
  function handleTrackClick(e: React.MouseEvent<HTMLDivElement>) {
    const rect = e.currentTarget.getBoundingClientRect()
    const pct = (e.clientX - rect.left) / rect.width
    const idx = Math.max(0, Math.min(n - 1, Math.round(pct * (n - 1))))
    onSelect(sorted[idx].id)
  }

  return (
    <div>
      {/* Legend */}
      <div className="flex justify-between text-xs mb-4">
        <span style={{ color: '#4ade80' }}>₹ Cheapest</span>
        <span style={{ color: '#ef4444' }}>Most expensive ₹₹₹</span>
      </div>

      {/* Track */}
      <div className="relative px-3 mb-1" style={{ height: 36 }}
        onClick={handleTrackClick}>

        {/* Base track */}
        <div className="absolute rounded-full" style={{
          top: '50%', left: 12, right: 12, height: 6,
          transform: 'translateY(-50%)',
          background: 'linear-gradient(to right, #4ade8025, #f59e0b25, #ef444425)',
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
        {sorted.map((opt, idx) => {
          const isChosen = opt.id === chosenOptionId
          if (isChosen) return null
          return (
            <div key={opt.id}
              onClick={e => { e.stopPropagation(); onSelect(opt.id) }}
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
              }}
            />
          )
        })}

        {/* Puck — the sliding button */}
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

      {/* Equidistant labels — flex so no overlap ever */}
      <div className="flex mb-5 px-3">
        {sorted.map((opt, idx) => {
          const isChosen = opt.id === chosenOptionId
          const color = stopColor(idx)
          const align: React.CSSProperties['textAlign'] =
            idx === 0 ? 'left' : idx === n - 1 ? 'right' : 'center'
          return (
            <div key={opt.id}
              onClick={() => onSelect(opt.id)}
              style={{ flex: 1, textAlign: align, cursor: 'pointer', padding: '0 2px' }}>
              <p style={{
                fontSize: 10, lineHeight: 1.3,
                fontWeight: isChosen ? 600 : 400,
                color: isChosen ? color : '#7d8590',
              }}>
                {opt.material?.name ?? opt.id}
              </p>
              {opt.cost !== null && (
                <p style={{ fontSize: 9, fontFamily: 'monospace', color: isChosen ? color : '#7d8590' }}>
                  ₹{opt.cost.toLocaleString()}
                </p>
              )}
            </div>
          )
        })}
      </div>

      {/* Selected detail card */}
      {chosenMaterial ? (
        <OptionDetail material={chosenMaterial} color={stopColor(chosenIdx)} stageColor={stageColor} />
      ) : (
        <div className="rounded-lg p-3 text-center text-xs"
          style={{ background: '#1c2128', border: '1px dashed #30363d', color: '#7d8590' }}>
          Slide or tap to choose
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
