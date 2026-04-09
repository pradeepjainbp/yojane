'use client'

import type { BuildScores, PlotConfig } from '@/types'

interface Props {
  scores: BuildScores | null
  plotConfig: PlotConfig
}

const SCORE_ITEMS = [
  { key: 'comfort',   label: 'Comfort',    unit: '/100', color: '#4ade80',  desc: 'Thermal, light, ventilation, acoustic, spatial' },
  { key: 'durability',label: 'Durability', unit: '/100', color: '#60a5fa',  desc: 'Expected useful life across all components' },
  { key: 'resilience',label: 'Resilience', unit: '/100', color: '#a78bfa',  desc: 'Monsoon, seismic, wind, termite resilience' },
]

export default function ScorePanel({ scores, plotConfig }: Props) {
  if (!scores) {
    return (
      <div className="p-4 border-t" style={{ borderColor: '#21262d' }}>
        <p className="text-xs text-center" style={{ color: '#7d8590' }}>
          Make your first decision to see scores
        </p>
      </div>
    )
  }

  const budget = plotConfig?.target_budget_inr
  const tcoDisplay = scores.tco ? `₹${Math.round(scores.tco).toString()}/sqft` : '—'
  const carbonDisplay = scores.carbon ? `${scores.carbon} kg/sqft` : '—'

  return (
    <div className="p-4 space-y-4 border-t" style={{ borderColor: '#21262d' }}>
      <h3 className="text-xs font-semibold uppercase tracking-widest" style={{ color: '#7d8590' }}>
        Live Scores
      </h3>

      {/* 3 bar scores */}
      {SCORE_ITEMS.map(item => {
        const value = scores[item.key as keyof BuildScores] as number
        return (
          <div key={item.key}>
            <div className="flex justify-between items-baseline mb-1">
              <span className="text-xs font-medium" style={{ color: '#e6edf3' }}>{item.label}</span>
              <span className="text-sm font-bold font-mono" style={{ color: item.color }}>
                {value ?? 0}{item.unit}
              </span>
            </div>
            <div className="h-1.5 rounded-full overflow-hidden" style={{ background: '#1c2128' }}>
              <div className="h-full rounded-full transition-all duration-700"
                style={{ width: `${value ?? 0}%`, background: item.color }} />
            </div>
            <p className="text-xs mt-0.5" style={{ color: '#7d8590' }}>{item.desc}</p>
          </div>
        )
      })}

      {/* TCO */}
      <div className="rounded-lg p-3" style={{ background: '#1c2128' }}>
        <div className="flex justify-between items-baseline">
          <span className="text-xs" style={{ color: '#7d8590' }}>20-yr TCO</span>
          <span className="text-sm font-bold font-mono" style={{ color: '#f59e0b' }}>{tcoDisplay}</span>
        </div>
        <p className="text-xs mt-0.5" style={{ color: '#7d8590' }}>
          Construction + maintenance + energy (7% discount)
        </p>
      </div>

      {/* Carbon */}
      <div className="rounded-lg p-3" style={{ background: '#1c2128' }}>
        <div className="flex justify-between items-baseline">
          <span className="text-xs" style={{ color: '#7d8590' }}>Carbon</span>
          <span className="text-sm font-bold font-mono" style={{ color: '#a3e635' }}>{carbonDisplay}</span>
        </div>
        <p className="text-xs mt-0.5" style={{ color: '#7d8590' }}>Embodied + 20-yr operational CO₂</p>
      </div>

      {/* Budget gauge */}
      {budget && (
        <div className="rounded-lg p-3 border"
          style={{ background: '#1c2128', borderColor: '#30363d' }}>
          <p className="text-xs mb-1" style={{ color: '#7d8590' }}>Budget</p>
          <p className="text-sm font-mono font-bold" style={{ color: '#e6edf3' }}>
            ₹{(budget / 100000).toFixed(1)}L target
          </p>
        </div>
      )}

      {/* Score breakdown — comfort */}
      {scores.score_breakdown?.comfort && (
        <div>
          <p className="text-xs font-medium mb-2" style={{ color: '#7d8590' }}>Comfort breakdown</p>
          <div className="space-y-1">
            {Object.entries(scores.score_breakdown.comfort).map(([key, val]) => (
              <div key={key} className="flex justify-between text-xs">
                <span className="capitalize" style={{ color: '#7d8590' }}>{key.replace('_', ' ')}</span>
                <span className="font-mono" style={{ color: '#e6edf3' }}>{val}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
