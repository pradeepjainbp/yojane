'use client'

import { useState } from 'react'
import { autoDecide } from '@/engine/auto-decide'
import { allDecisions } from '@/data/decision-points'
import type { Component, PlotConfig, Decision } from '@/types'

interface Props {
  plot: PlotConfig
  buildingType: string
  buildId: string
  componentsBySubcategory: Record<string, Component[]>
  onApply: (decisions: Decision[]) => void
  onClose: () => void
}

export default function AutoDecidePanel({ plot, buildingType, buildId, componentsBySubcategory, onApply, onClose }: Props) {
  const [budget, setBudget] = useState<number>(plot.target_budget_inr ?? 0)
  const [result, setResult] = useState<ReturnType<typeof autoDecide> | null>(null)
  const [running, setRunning] = useState(false)
  const [applying, setApplying] = useState(false)

  function runEngine() {
    setRunning(true)
    const plotWithBudget = { ...plot, target_budget_inr: budget || null }
    setTimeout(() => {
      const r = autoDecide(plotWithBudget, buildingType, componentsBySubcategory)
      setResult(r)
      setRunning(false)
    }, 800)
  }

  function handleApply() {
    if (!result) return
    setApplying(true)
    const decisionsWithBuildId = result.decisions.map(d => ({ ...d, build_id: buildId }))
    onApply(decisionsWithBuildId)
  }

  const criticalCount  = allDecisions.filter(d => d.classification === 'critical').length
  const standardCount  = allDecisions.filter(d => d.classification === 'standard').length

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4"
      style={{ background: 'rgba(0,0,0,0.8)' }}>
      <div className="w-full max-w-lg rounded-2xl overflow-hidden"
        style={{ background: '#161b22', border: '1px solid #30363d', maxHeight: '90vh', overflowY: 'auto' }}>

        {/* Header */}
        <div className="px-6 py-4 flex items-center justify-between"
          style={{ borderBottom: '1px solid #30363d', background: '#1c2128' }}>
          <div>
            <h2 className="font-semibold" style={{ color: '#e6edf3' }}>Let AI Decide</h2>
            <p className="text-xs mt-0.5" style={{ color: '#7d8590' }}>
              AI picks the best materials for your budget &amp; climate
            </p>
          </div>
          <button onClick={onClose} className="text-lg cursor-pointer" style={{ color: '#7d8590' }}>×</button>
        </div>

        <div className="p-6 space-y-6">

          {/* Budget input */}
          <div>
            <label className="block text-sm font-medium mb-2" style={{ color: '#e6edf3' }}>
              Total Construction Budget (₹)
            </label>
            <input
              type="number"
              value={budget || ''}
              onChange={e => setBudget(+e.target.value)}
              placeholder="e.g. 4500000  (leave blank = best quality)"
              className="w-full px-3 py-2.5 rounded-lg text-sm"
              style={{ background: '#0d1117', border: '1px solid #30363d', color: '#e6edf3' }}
            />
            {budget > 0 && (
              <p className="text-xs mt-1 font-mono" style={{ color: '#4ade80' }}>
                ₹{(budget / 100000).toFixed(1)}L total ·{' '}
                ≈ ₹{Math.round(budget / (plot.plot_area_sqft * plot.floors)).toLocaleString()}/sqft
              </p>
            )}
            {!budget && (
              <p className="text-xs mt-1" style={{ color: '#7d8590' }}>
                No budget = AI picks highest-quality options regardless of cost.
              </p>
            )}
          </div>

          {/* What AI will decide */}
          <div className="rounded-lg p-4" style={{ background: '#0d1117', border: '1px solid #30363d' }}>
            <p className="text-xs font-medium mb-3" style={{ color: '#7d8590' }}>AI will make:</p>
            <div className="flex gap-4">
              <div className="text-center">
                <p className="text-2xl font-bold" style={{ color: '#f59e0b' }}>{criticalCount}</p>
                <p className="text-xs" style={{ color: '#7d8590' }}>Critical decisions</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold" style={{ color: '#4ade80' }}>{standardCount}</p>
                <p className="text-xs" style={{ color: '#7d8590' }}>Standard decisions</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold" style={{ color: '#60a5fa' }}>{allDecisions.length}</p>
                <p className="text-xs" style={{ color: '#7d8590' }}>Total</p>
              </div>
            </div>
            <p className="text-xs mt-3" style={{ color: '#7d8590' }}>
              For each decision, AI scores every option on durability (35%), climate fit (30%), value for money (20%), and low carbon (15%) — picks the highest scorer within your budget tier. You can override any choice after.
            </p>
          </div>

          {/* Run button */}
          {!result && (
            <button
              onClick={runEngine}
              disabled={running}
              className="w-full py-3 rounded-lg font-medium cursor-pointer disabled:opacity-60"
              style={{ background: '#4ade80', color: '#0d1117' }}>
              {running ? (
                <span className="flex items-center justify-center gap-2">
                  <svg className="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                  </svg>
                  AI is thinking…
                </span>
              ) : 'Run AI Decision Engine →'}
            </button>
          )}

          {/* Results */}
          {result && (
            <div className="space-y-4">

              {/* Feasibility verdict */}
              {result.feasible ? (
                <div className="rounded-xl p-4" style={{ background: '#4ade8015', border: '1px solid #4ade8040' }}>
                  <p className="font-semibold text-sm" style={{ color: '#4ade80' }}>✓ Feasible within budget</p>
                  <div className="mt-2 grid grid-cols-2 gap-3 text-xs font-mono">
                    <div>
                      <p style={{ color: '#7d8590' }}>Est. cost/sqft</p>
                      <p className="font-bold" style={{ color: '#e6edf3' }}>₹{result.estimatedCostPerSqft.toLocaleString()}</p>
                    </div>
                    <div>
                      <p style={{ color: '#7d8590' }}>Est. total</p>
                      <p className="font-bold" style={{ color: '#e6edf3' }}>₹{(result.estimatedTotalCost / 100000).toFixed(1)}L</p>
                    </div>
                    {budget > 0 && (
                      <>
                        <div>
                          <p style={{ color: '#7d8590' }}>Your budget</p>
                          <p className="font-bold" style={{ color: '#4ade80' }}>₹{(budget / 100000).toFixed(1)}L</p>
                        </div>
                        <div>
                          <p style={{ color: '#7d8590' }}>Headroom</p>
                          <p className="font-bold" style={{ color: '#4ade80' }}>
                            ₹{((budget - result.estimatedTotalCost) / 100000).toFixed(1)}L
                          </p>
                        </div>
                      </>
                    )}
                  </div>
                </div>
              ) : (
                <div className="rounded-xl p-4" style={{ background: '#ef444415', border: '1px solid #ef444440' }}>
                  <p className="font-semibold text-sm" style={{ color: '#ef4444' }}>⚠ Budget too tight for quality construction</p>
                  <p className="text-xs mt-1" style={{ color: '#7d8590' }}>
                    Even with the most affordable choices, the estimate exceeds your budget.
                  </p>
                  <div className="mt-3 grid grid-cols-2 gap-3 text-xs font-mono">
                    <div>
                      <p style={{ color: '#7d8590' }}>Minimum est.</p>
                      <p className="font-bold" style={{ color: '#ef4444' }}>₹{(result.estimatedTotalCost / 100000).toFixed(1)}L</p>
                    </div>
                    <div>
                      <p style={{ color: '#7d8590' }}>Your budget</p>
                      <p className="font-bold" style={{ color: '#e6edf3' }}>₹{(budget / 100000).toFixed(1)}L</p>
                    </div>
                    <div>
                      <p style={{ color: '#7d8590' }}>Shortfall</p>
                      <p className="font-bold" style={{ color: '#ef4444' }}>₹{(result.shortfall / 100000).toFixed(1)}L</p>
                    </div>
                    <div>
                      <p style={{ color: '#7d8590' }}>Suggested budget</p>
                      <p className="font-bold" style={{ color: '#f59e0b' }}>₹{(result.estimatedTotalCost / 100000).toFixed(1)}L+</p>
                    </div>
                  </div>
                  <p className="text-xs mt-3" style={{ color: '#7d8590' }}>
                    You can still apply these decisions as a starting point and adjust — but we recommend revising your budget first.
                  </p>
                </div>
              )}

              {/* Decision preview */}
              <div>
                <p className="text-xs font-medium mb-2" style={{ color: '#7d8590' }}>Decision preview</p>
                <div className="space-y-1 max-h-60 overflow-y-auto pr-1">
                  {result.decisions.slice(0, 20).map(dec => {
                    const dp  = allDecisions.find(d => d.id === dec.decision_id)
                    const r   = result.reasoning[dec.decision_id]
                    const isCritical = dp?.classification === 'critical'
                    return (
                      <div key={dec.decision_id} className="flex items-start gap-2 py-1.5 text-xs"
                        style={{ borderBottom: '1px solid #21262d' }}>
                        <span className="font-mono flex-shrink-0 w-6" style={{ color: isCritical ? '#f59e0b' : '#7d8590' }}>
                          {dec.decision_id}
                        </span>
                        <span className="flex-1 min-w-0 truncate" style={{ color: '#e6edf3' }}>
                          {r?.chosenName ?? dec.chosen_option_id}
                        </span>
                        {r?.score !== undefined && (
                          <span className="ml-auto font-mono flex-shrink-0" style={{ color: '#7d8590' }}>
                            {r.score}/100
                          </span>
                        )}
                      </div>
                    )
                  })}
                  {result.decisions.length > 20 && (
                    <p className="text-xs text-center py-2" style={{ color: '#7d8590' }}>
                      + {result.decisions.length - 20} more decisions
                    </p>
                  )}
                </div>
              </div>

              {/* Action buttons */}
              <div className="flex gap-3">
                <button onClick={() => setResult(null)}
                  className="flex-1 py-2.5 rounded-lg text-sm cursor-pointer"
                  style={{ border: '1px solid #30363d', color: '#7d8590' }}>
                  Adjust Budget
                </button>
                <button
                  onClick={handleApply}
                  disabled={applying}
                  className="flex-1 py-2.5 rounded-lg text-sm font-medium cursor-pointer disabled:opacity-60"
                  style={{ background: result.feasible ? '#4ade80' : '#f59e0b', color: '#0d1117' }}>
                  {applying ? 'Applying…' : result.feasible ? 'Apply All Decisions' : 'Apply Anyway (review after)'}
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
