'use client'

import type { Decision, Stage } from '@/types'

interface Props {
  decisions: Decision[]
  activeStage: Stage
}

const STAGE_LAYERS: { stage: Stage; label: string; color: string; emoji: string }[] = [
  { stage: 'A', label: 'Foundation', color: '#f59e0b', emoji: '⬛' },
  { stage: 'B', label: 'Walls',      color: '#60a5fa', emoji: '🧱' },
  { stage: 'C', label: 'Roof',       color: '#818cf8', emoji: '🏚' },
  { stage: 'D', label: 'Interiors',  color: '#f472b6', emoji: '🪟' },
  { stage: 'E', label: 'MEP',        color: '#34d399', emoji: '⚡' },
  { stage: 'F', label: 'Landscape',  color: '#a3e635', emoji: '🌿' },
]

const STAGE_ORDER: Stage[] = ['A', 'B', 'C', 'D', 'E', 'F']

export default function IsometricView({ decisions, activeStage }: Props) {
  const completedStages = new Set(decisions.map(d => d.stage))
  const activeStageIdx = STAGE_ORDER.indexOf(activeStage)

  return (
    <div className="p-4 border-b" style={{ borderColor: '#21262d' }}>
      <h3 className="text-xs font-semibold uppercase tracking-widest mb-3" style={{ color: '#7d8590' }}>
        Build Progress
      </h3>

      {/* Simplified isometric house SVG */}
      <div className="relative mx-auto mb-4" style={{ width: 200, height: 160 }}>
        <svg viewBox="0 0 200 160" width="200" height="160">
          {/* Ground */}
          <ellipse cx="100" cy="148" rx="80" ry="12" fill="#1c2128" />

          {/* Foundation layer */}
          {(completedStages.has('A') || activeStage === 'A') && (
            <rect x="40" y="128" width="120" height="16" rx="2"
              fill={activeStage === 'A' ? '#f59e0b30' : '#f59e0b20'}
              stroke={completedStages.has('A') ? '#f59e0b' : '#f59e0b50'}
              strokeWidth="1" />
          )}

          {/* Wall layer */}
          {(completedStages.has('B') || activeStage === 'B') && (
            <>
              {/* Front wall */}
              <rect x="40" y="72" width="120" height="56"
                fill={activeStage === 'B' ? '#60a5fa20' : '#60a5fa10'}
                stroke={completedStages.has('B') ? '#60a5fa' : '#60a5fa40'}
                strokeWidth="1" />
              {/* Side wall (isometric illusion) */}
              <polygon points="160,72 180,60 180,116 160,128"
                fill={activeStage === 'B' ? '#60a5fa15' : '#60a5fa08'}
                stroke={completedStages.has('B') ? '#60a5fa80' : '#60a5fa30'}
                strokeWidth="1" />
            </>
          )}

          {/* Door */}
          {completedStages.has('D') && (
            <rect x="85" y="96" width="28" height="32" rx="1"
              fill="#f472b620" stroke="#f472b6" strokeWidth="1" />
          )}

          {/* Windows */}
          {completedStages.has('D') && (
            <>
              <rect x="50" y="82" width="22" height="18" rx="1"
                fill="#60a5fa20" stroke="#60a5fa" strokeWidth="1" />
              <rect x="128" y="82" width="22" height="18" rx="1"
                fill="#60a5fa20" stroke="#60a5fa" strokeWidth="1" />
            </>
          )}

          {/* Roof layer */}
          {(completedStages.has('C') || activeStage === 'C') && (
            <>
              <polygon points="100,20 40,72 160,72"
                fill={activeStage === 'C' ? '#818cf830' : '#818cf815'}
                stroke={completedStages.has('C') ? '#818cf8' : '#818cf850'}
                strokeWidth="1.5" />
              <polygon points="100,20 160,72 180,60 120,8"
                fill={activeStage === 'C' ? '#818cf820' : '#818cf810'}
                stroke={completedStages.has('C') ? '#818cf880' : '#818cf840'}
                strokeWidth="1.5" />
            </>
          )}

          {/* MEP overlay */}
          {completedStages.has('E') && (
            <>
              <line x1="60" y1="128" x2="60" y2="72" stroke="#34d399" strokeWidth="1.5" strokeDasharray="4,3" opacity="0.6" />
              <line x1="140" y1="128" x2="140" y2="72" stroke="#f59e0b" strokeWidth="1.5" strokeDasharray="4,3" opacity="0.6" />
            </>
          )}

          {/* Landscape */}
          {completedStages.has('F') && (
            <>
              <ellipse cx="25" cy="142" rx="18" ry="14" fill="#a3e63520" stroke="#a3e635" strokeWidth="1" />
              <ellipse cx="175" cy="142" rx="18" ry="14" fill="#a3e63520" stroke="#a3e635" strokeWidth="1" />
              <line x1="25" y1="128" x2="25" y2="148" stroke="#a3e635" strokeWidth="1.5" />
              <line x1="175" y1="128" x2="175" y2="148" stroke="#a3e635" strokeWidth="1.5" />
            </>
          )}

          {/* Active stage pulse ring */}
          {activeStageIdx >= 0 && (
            <circle cx="100" cy="80" r="6"
              fill={(STAGE_LAYERS[activeStageIdx]?.color ?? '#fff') + '30'}
              stroke={STAGE_LAYERS[activeStageIdx]?.color ?? '#fff'}
              strokeWidth="1.5"
              opacity="0.8">
              <animate attributeName="r" from="4" to="10" dur="1.5s" repeatCount="indefinite" />
              <animate attributeName="opacity" from="0.8" to="0" dur="1.5s" repeatCount="indefinite" />
            </circle>
          )}
        </svg>
      </div>

      {/* Stage layer list */}
      <div className="space-y-1">
        {STAGE_LAYERS.map((layer) => {
          const done = completedStages.has(layer.stage)
          const active = layer.stage === activeStage
          return (
            <div key={layer.stage}
              className="flex items-center gap-2 px-2 py-1 rounded text-xs"
              style={{
                background: active ? layer.color + '15' : 'transparent',
              }}>
              <span>{layer.emoji}</span>
              <span style={{ color: active ? layer.color : done ? '#4ade80' : '#7d8590' }}>
                {layer.stage} · {layer.label}
              </span>
              {done && <span className="ml-auto" style={{ color: '#4ade80' }}>✓</span>}
              {active && !done && <span className="ml-auto pulse-dot w-1.5 h-1.5 rounded-full" style={{ background: layer.color }} />}
            </div>
          )
        })}
      </div>
    </div>
  )
}
