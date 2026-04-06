'use client'

import type { Stage, Decision } from '@/types'
import { decisionsByStage } from '@/data/decision-points'

interface Props {
  stages: { id: Stage; label: string; color: string }[]
  activeStage: Stage
  onSelect: (stage: Stage) => void
  decisions: Decision[]
}

export default function StageNav({ stages, activeStage, onSelect, decisions }: Props) {
  return (
    <div className="flex flex-col items-center py-4 gap-1">
      {stages.map((s) => {
        const stageDecisions = decisionsByStage[s.id] ?? []
        const completed = stageDecisions.filter(dp =>
          decisions.some(d => d.decision_id === dp.id)
        ).length
        const total = stageDecisions.length
        const isActive = s.id === activeStage
        const isDone = completed === total && total > 0

        return (
          <button
            key={s.id}
            onClick={() => onSelect(s.id)}
            title={s.label}
            className="relative w-10 h-10 rounded-lg flex items-center justify-center font-mono font-bold text-sm cursor-pointer transition-all"
            style={{
              background: isActive ? s.color + '30' : 'transparent',
              color: isActive ? s.color : isDone ? '#4ade80' : '#7d8590',
              border: isActive ? `1px solid ${s.color}60` : '1px solid transparent',
            }}
          >
            {s.id}
            {isDone && !isActive && (
              <span className="absolute -top-0.5 -right-0.5 w-2 h-2 rounded-full" style={{ background: '#4ade80' }} />
            )}
          </button>
        )
      })}
    </div>
  )
}
