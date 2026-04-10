'use client'

import { useState, useEffect, useCallback, useRef } from 'react'
import { useRouter } from 'next/navigation'
import { createClient } from '@/lib/supabase/client'
import { decisionsByStage, allDecisions } from '@/data/decision-points'
import { calculateAllScores } from '@/engine/scoring'
import type { Build, Component, Decision, BuildScores, Stage } from '@/types'
import ScorePanel from '@/components/simulator/ScorePanel'
import StageNav from '@/components/simulator/StageNav'
import DecisionCard from '@/components/simulator/DecisionCard'
import IsometricView from '@/components/simulator/IsometricView'
import AutoDecidePanel from '@/components/simulator/AutoDecidePanel'

function computeDirectCost(
  decs: Decision[],
  componentsBySubcategory: Record<string, Component[]>,
  plotArea: number,
  floors: number
): number {
  let total = 0
  for (const dec of decs) {
    for (const comps of Object.values(componentsBySubcategory)) {
      const found = comps.find(c => c.component_id === dec.chosen_option_id)
      if (found) {
        total += ((found.base_cost_per_sqft_inr ?? 0) + (found.installation_cost_per_sqft_inr ?? 0)) * plotArea * floors
        break
      }
    }
  }
  return total
}

const STAGES: { id: Stage; label: string; color: string }[] = [
  { id: 'A', label: 'Foundation', color: '#f59e0b' },
  { id: 'B', label: 'Walls',      color: '#60a5fa' },
  { id: 'C', label: 'Roofing',    color: '#818cf8' },
  { id: 'D', label: 'Interiors',  color: '#f472b6' },
  { id: 'E', label: 'MEP',        color: '#34d399' },
  { id: 'F', label: 'Landscape',  color: '#a3e635' },
]

const TOTAL_DECISIONS = allDecisions.length

interface Props {
  build: Build
  initialDecisions: Decision[]
  initialScores: BuildScores | null
}

export default function BuildSimulator({ build, initialDecisions, initialScores }: Props) {
  const supabase = createClient()
  const router = useRouter()
  const [decisions, setDecisions] = useState<Decision[]>(initialDecisions)
  const [activeStage, setActiveStage] = useState<Stage>('A')
  const [scores, setScores] = useState<BuildScores | null>(initialScores)
  const [saving, setSaving] = useState(false)
  const [showAutoDecide, setShowAutoDecide] = useState(false)
  const [directCost, setDirectCost] = useState(0)
  const [costDelta, setCostDelta] = useState<number | null>(null)
  const deltaTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null)

  // All 134 components keyed by subcategory_name — fetched once on mount
  const [componentsBySubcategory, setComponentsBySubcategory] = useState<Record<string, Component[]>>({})
  const [componentsLoading, setComponentsLoading] = useState(true)
  const [componentsError, setComponentsError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchComponents() {
      const { data, error } = await supabase
        .from('components')
        .select('*')
        .order('sort_order', { ascending: true })

      if (error) {
        console.error('components fetch error:', error)
        setComponentsError(error.message)
        setComponentsLoading(false)
        return
      }
      if (!data || data.length === 0) {
        setComponentsError('components table is empty — run the registry import first')
        setComponentsLoading(false)
        return
      }

      const grouped: Record<string, Component[]> = {}
      for (const row of data as Component[]) {
        if (!grouped[row.subcategory_name]) grouped[row.subcategory_name] = []
        grouped[row.subcategory_name].push(row)
      }
      setComponentsBySubcategory(grouped)
      setComponentsLoading(false)
      // Seed wallet with current decisions
      const plotArea = build.plot_config?.plot_area_sqft ?? 1000
      const floors = build.plot_config?.floors ?? 1
      setDirectCost(computeDirectCost(
        initialDecisions,
        grouped,
        plotArea,
        floors,
      ))
    }
    fetchComponents()
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  const recalcScores = useCallback((decs: Decision[]) => {
    // Pass the chosen component objects so scoring can use registry fields
    const chosenComponents = decs
      .map(d => {
        // Find the component by component_id = chosen_option_id
        for (const comps of Object.values(componentsBySubcategory)) {
          const found = comps.find(c => c.component_id === d.chosen_option_id)
          if (found) return found
        }
        return null
      })
      .filter((c): c is Component => c !== null)

    const newScores = calculateAllScores(decs, build.plot_config, build.building_type, chosenComponents)
    setScores(newScores)
    return newScores
  }, [build, componentsBySubcategory])

  useEffect(() => {
    if (decisions.length > 0) recalcScores(decisions)
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  async function handleDecisionChange(decisionId: string, optionId: string) {
    const stage = decisionId[0] as Stage
    const existing = decisions.find(d => d.decision_id === decisionId)
    const plotArea = build.plot_config?.plot_area_sqft ?? 1000
    const floors = build.plot_config?.floors ?? 1

    const updated: Decision = existing
      ? { ...existing, chosen_option_id: optionId, updated_at: new Date().toISOString() }
      : {
          id: crypto.randomUUID(),
          build_id: build.id,
          decision_id: decisionId,
          stage,
          chosen_option_id: optionId,
          cost_override: null,
          notes: null,
          updated_at: new Date().toISOString(),
        }

    const newDecisions = existing
      ? decisions.map(d => d.decision_id === decisionId ? updated : d)
      : [...decisions, updated]

    // Compute cost delta for wallet animation
    const oldCost = computeDirectCost(decisions, componentsBySubcategory, plotArea, floors)
    const newCost = computeDirectCost(newDecisions, componentsBySubcategory, plotArea, floors)
    const delta = newCost - oldCost
    setDirectCost(newCost)
    if (delta !== 0) {
      setCostDelta(delta)
      if (deltaTimerRef.current) clearTimeout(deltaTimerRef.current)
      deltaTimerRef.current = setTimeout(() => setCostDelta(null), 3000)
    }

    setDecisions(newDecisions)
    const newScores = recalcScores(newDecisions)

    setSaving(true)
    try {
      await supabase.from('decisions').upsert({
        build_id: build.id,
        decision_id: decisionId,
        stage,
        chosen_option_id: optionId,
        updated_at: new Date().toISOString(),
      }, { onConflict: 'build_id,decision_id' })

      await supabase.from('build_scores').upsert({
        build_id: build.id,
        comfort: newScores.comfort,
        durability: newScores.durability,
        tco: newScores.tco,
        resilience: newScores.resilience,
        carbon: newScores.carbon,
        score_breakdown: newScores.score_breakdown,
        calculated_at: new Date().toISOString(),
      }, { onConflict: 'build_id' })
    } finally {
      setSaving(false)
    }
  }

  async function handleAutoDecideApply(newDecisions: Decision[]) {
    const plotArea = build.plot_config?.plot_area_sqft ?? 1000
    const floors = build.plot_config?.floors ?? 1
    const merged = [...decisions]
    for (const nd of newDecisions) {
      const idx = merged.findIndex(d => d.decision_id === nd.decision_id)
      if (idx >= 0) merged[idx] = nd
      else merged.push(nd)
    }
    setDecisions(merged)
    setDirectCost(computeDirectCost(merged, componentsBySubcategory, plotArea, floors))
    recalcScores(merged)
    setSaving(true)
    try {
      const upsertRows = newDecisions.map(d => ({
        build_id: build.id,
        decision_id: d.decision_id,
        stage: d.stage,
        chosen_option_id: d.chosen_option_id,
        updated_at: new Date().toISOString(),
      }))
      await supabase.from('decisions').upsert(upsertRows, { onConflict: 'build_id,decision_id' })
    } finally {
      setSaving(false)
      setShowAutoDecide(false)
    }
  }

  async function markComplete() {
    await supabase.from('builds').update({ status: 'complete' }).eq('id', build.id)
    router.push(`/build/${build.id}/report`)
  }

  const stageDecisions = decisionsByStage[activeStage] ?? []
  const stageInfo = STAGES.find(s => s.id === activeStage)!
  const stageIdx = STAGES.findIndex(s => s.id === activeStage)

  // Progress
  const decisionsCompleted = decisions.length
  const progressPct = Math.round((decisionsCompleted / TOTAL_DECISIONS) * 100)
  const criticalRemaining = allDecisions
    .filter(d => d.classification === 'critical')
    .filter(d => !decisions.some(dec => dec.decision_id === d.id)).length
  const allCriticalDone = criticalRemaining === 0

  // Budget gauge
  const budget = build.plot_config?.target_budget_inr
  const estimate = scores ? Math.round(scores.tco * (build.plot_config?.plot_area_sqft ?? 1000) * (build.plot_config?.floors ?? 1) * 0.45) : null
  const budgetPct = budget && estimate ? Math.round(((estimate - budget) / budget) * 100) : null

  return (
    <div className="min-h-screen flex flex-col" style={{ background: '#0d1117' }}>
      {/* Header */}
      <header className="sticky top-0 z-50" style={{ borderBottom: '1px solid #21262d', background: '#161b22' }}>
        <div className="max-w-full px-4 h-14 flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <a href="/dashboard" className="text-sm" style={{ color: '#7d8590' }}>← Builds</a>
            <span style={{ color: '#30363d' }}>|</span>
            <h1 className="text-sm font-semibold" style={{ color: '#e6edf3' }}>{build.name}</h1>
            {saving && <span className="text-xs" style={{ color: '#7d8590' }}>Saving…</span>}
          </div>

          <div className="flex items-center gap-3">
            {/* Progress pill */}
            <div className="hidden sm:flex items-center gap-2 text-xs font-mono">
              <div className="w-24 h-1.5 rounded-full" style={{ background: '#30363d' }}>
                <div className="h-full rounded-full transition-all duration-500"
                  style={{ width: `${progressPct}%`, background: '#4ade80' }} />
              </div>
              <span style={{ color: '#7d8590' }}>{decisionsCompleted}/{TOTAL_DECISIONS}</span>
            </div>

            {/* Budget gauge */}
            {budget && estimate && (
              <span className="text-xs font-mono px-2 py-0.5 rounded"
                style={{
                  background: budgetPct === null ? '#30363d20'
                    : budgetPct <= 0 ? '#10b98120'
                    : budgetPct <= 20 ? '#f59e0b20'
                    : '#ef444420',
                  color: budgetPct === null ? '#7d8590'
                    : budgetPct <= 0 ? '#10b981'
                    : budgetPct <= 20 ? '#f59e0b'
                    : '#ef4444',
                }}>
                {budgetPct !== null
                  ? budgetPct > 0 ? `+${budgetPct}% over` : `${Math.abs(budgetPct)}% under`
                  : `₹${(budget / 100000).toFixed(1)}L`}
              </span>
            )}

            {/* Auto-decide button */}
            <button
              onClick={() => setShowAutoDecide(true)}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium cursor-pointer"
              style={{ background: '#818cf820', border: '1px solid #818cf840', color: '#818cf8' }}>
              ✦ Let AI Decide
            </button>

            {/* View Report button — shown when all critical decisions done */}
            {allCriticalDone && (
              <button onClick={markComplete}
                className="flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium cursor-pointer"
                style={{ background: '#4ade80', color: '#0d1117' }}>
                View Report →
              </button>
            )}
          </div>
        </div>
      </header>

      <div className="flex flex-1 overflow-hidden">
        {/* Left — Stage nav */}
        <aside className="hidden lg:flex flex-col w-14" style={{ borderRight: '1px solid #21262d', background: '#161b22' }}>
          <StageNav stages={STAGES} activeStage={activeStage} onSelect={setActiveStage} decisions={decisions} />
        </aside>

        {/* Main — Decision cards */}
        <main className="flex-1 overflow-y-auto">
          <div className="max-w-2xl mx-auto px-4 py-6">

            {/* Stage header */}
            <div className="flex items-center gap-3 mb-6">
              <span className="text-2xl font-bold font-mono" style={{ color: stageInfo.color }}>
                {activeStage}
              </span>
              <div>
                <h2 className="text-lg font-bold" style={{ color: '#e6edf3' }}>{stageInfo.label}</h2>
                <p className="text-xs" style={{ color: '#7d8590' }}>
                  {stageDecisions.filter(d => d.classification === 'critical').length} critical ·{' '}
                  {stageDecisions.filter(d => d.classification === 'standard').length} standard
                </p>
              </div>
              {componentsLoading && (
                <span className="text-xs ml-auto" style={{ color: '#7d8590' }}>Loading material data…</span>
              )}
              {componentsError && (
                <span className="text-xs ml-auto px-2 py-0.5 rounded"
                  style={{ background: '#ef444420', color: '#ef4444', border: '1px solid #ef444440' }}>
                  ⚠ Registry error: {componentsError}
                </span>
              )}
              {!componentsLoading && !componentsError && Object.keys(componentsBySubcategory).length > 0 && (
                <span className="text-xs ml-auto" style={{ color: '#4ade80' }}>
                  ✓ {Object.values(componentsBySubcategory).flat().length} materials loaded
                </span>
              )}
            </div>

            {/* Mobile stage tabs */}
            <div className="flex gap-2 mb-6 overflow-x-auto pb-1 lg:hidden">
              {STAGES.map(s => (
                <button key={s.id} onClick={() => setActiveStage(s.id)}
                  className="flex-shrink-0 px-3 py-1.5 rounded-lg text-xs font-medium cursor-pointer"
                  style={{
                    background: activeStage === s.id ? s.color + '20' : '#161b22',
                    border: `1px solid ${activeStage === s.id ? s.color : '#30363d'}`,
                    color: activeStage === s.id ? s.color : '#7d8590',
                  }}>
                  {s.id} · {s.label}
                </button>
              ))}
            </div>

            {/* Decision cards */}
            <div className="space-y-4">
              {stageDecisions.map(dp => (
                <DecisionCard
                  key={dp.id}
                  decisionPoint={dp}
                  components={dp.subcategory ? (componentsBySubcategory[dp.subcategory] ?? []) : []}
                  chosenOptionId={decisions.find(d => d.decision_id === dp.id)?.chosen_option_id ?? null}
                  stageColor={stageInfo.color}
                  onSelect={(optionId) => handleDecisionChange(dp.id, optionId)}
                />
              ))}
            </div>

            {/* Stage navigation */}
            <div className="flex gap-3 mt-8">
              {stageIdx > 0 && (
                <button onClick={() => setActiveStage(STAGES[stageIdx - 1].id)}
                  className="flex-1 py-3 rounded-lg text-sm cursor-pointer"
                  style={{ border: '1px solid #30363d', color: '#7d8590' }}>
                  ← {STAGES[stageIdx - 1].label}
                </button>
              )}
              {stageIdx < STAGES.length - 1 ? (
                <button onClick={() => setActiveStage(STAGES[stageIdx + 1].id)}
                  className="flex-1 py-3 rounded-lg font-medium text-sm cursor-pointer"
                  style={{
                    background: stageInfo.color + '20',
                    border: `1px solid ${stageInfo.color}40`,
                    color: stageInfo.color,
                  }}>
                  {STAGES[stageIdx + 1].label} →
                </button>
              ) : (
                <button onClick={markComplete}
                  disabled={!allCriticalDone}
                  className="flex-1 py-3 rounded-lg font-medium text-sm cursor-pointer disabled:opacity-40"
                  style={{ background: allCriticalDone ? '#4ade80' : '#30363d', color: allCriticalDone ? '#0d1117' : '#7d8590' }}>
                  {allCriticalDone
                    ? '🏗 View Build Report →'
                    : `Complete ${criticalRemaining} critical decision${criticalRemaining > 1 ? 's' : ''} first`}
                </button>
              )}
            </div>

            {/* All-critical-done banner */}
            {allCriticalDone && activeStage !== 'F' && (
              <div className="mt-6 p-4 rounded-xl text-sm flex items-center justify-between"
                style={{ background: '#4ade8015', border: '1px solid #4ade8040' }}>
                <div>
                  <p className="font-medium" style={{ color: '#4ade80' }}>All critical decisions done ✓</p>
                  <p className="text-xs mt-0.5" style={{ color: '#7d8590' }}>
                    You can view your Build Report now, or keep refining standard decisions.
                  </p>
                </div>
                <button onClick={markComplete}
                  className="ml-4 px-3 py-2 rounded-lg text-xs font-medium cursor-pointer flex-shrink-0"
                  style={{ background: '#4ade80', color: '#0d1117' }}>
                  View Report
                </button>
              </div>
            )}
          </div>
        </main>

        {/* Right — Scores + Isometric */}
        <aside className="hidden xl:flex flex-col w-80 overflow-y-auto"
          style={{ borderLeft: '1px solid #21262d', background: '#161b22' }}>
          <IsometricView decisions={decisions} activeStage={activeStage} />
          <ScorePanel scores={scores} plotConfig={build.plot_config} />
        </aside>
      </div>

      {/* AutoDecide modal */}
      {showAutoDecide && (
        <AutoDecidePanel
          plot={build.plot_config}
          buildingType={build.building_type}
          buildId={build.id}
          componentsBySubcategory={componentsBySubcategory}
          onApply={handleAutoDecideApply}
          onClose={() => setShowAutoDecide(false)}
        />
      )}

      {/* Floating Wallet */}
      <FloatingWallet
        directCost={directCost}
        budget={budget ?? null}
        decisionsCount={decisions.length}
        totalDecisions={TOTAL_DECISIONS}
        costDelta={costDelta}
      />
    </div>
  )
}

// ── Floating Wallet (draggable) ──────────────────────────────────
function FloatingWallet({
  directCost,
  budget,
  decisionsCount,
  totalDecisions,
  costDelta,
}: {
  directCost: number
  budget: number | null
  decisionsCount: number
  totalDecisions: number
  costDelta: number | null
}) {
  const [pos, setPos] = useState<{ x: number; y: number } | null>(null)
  const dragging = useRef(false)
  const dragOrigin = useRef({ mouseX: 0, mouseY: 0, elemX: 0, elemY: 0 })

  // Initialise to bottom-right on first render
  useEffect(() => {
    setPos({ x: window.innerWidth - 220, y: window.innerHeight - 145 })
  }, [])

  useEffect(() => {
    function onMove(e: MouseEvent) {
      if (!dragging.current) return
      setPos(prev => {
        if (!prev) return prev
        return {
          x: Math.max(0, Math.min(window.innerWidth - 210, dragOrigin.current.elemX + e.clientX - dragOrigin.current.mouseX)),
          y: Math.max(0, Math.min(window.innerHeight - 130, dragOrigin.current.elemY + e.clientY - dragOrigin.current.mouseY)),
        }
      })
    }
    function onUp() { dragging.current = false }
    function onTouchMove(e: TouchEvent) {
      if (!dragging.current) return
      e.preventDefault()
      const t = e.touches[0]
      setPos(prev => {
        if (!prev) return prev
        return {
          x: Math.max(0, Math.min(window.innerWidth - 210, dragOrigin.current.elemX + t.clientX - dragOrigin.current.mouseX)),
          y: Math.max(0, Math.min(window.innerHeight - 130, dragOrigin.current.elemY + t.clientY - dragOrigin.current.mouseY)),
        }
      })
    }
    window.addEventListener('mousemove', onMove)
    window.addEventListener('mouseup', onUp)
    window.addEventListener('touchmove', onTouchMove, { passive: false })
    window.addEventListener('touchend', onUp)
    return () => {
      window.removeEventListener('mousemove', onMove)
      window.removeEventListener('mouseup', onUp)
      window.removeEventListener('touchmove', onTouchMove)
      window.removeEventListener('touchend', onUp)
    }
  }, [])

  function onMouseDown(e: React.MouseEvent) {
    if (!pos) return
    dragging.current = true
    dragOrigin.current = { mouseX: e.clientX, mouseY: e.clientY, elemX: pos.x, elemY: pos.y }
    e.preventDefault()
  }

  function onTouchStart(e: React.TouchEvent) {
    if (!pos) return
    const t = e.touches[0]
    dragging.current = true
    dragOrigin.current = { mouseX: t.clientX, mouseY: t.clientY, elemX: pos.x, elemY: pos.y }
  }

  if (!pos || (directCost === 0 && decisionsCount === 0)) return null

  const inLakhs = (v: number) => v >= 10000000 ? `₹${(v / 10000000).toFixed(2)} Cr` : `₹${(v / 100000).toFixed(2)} L`

  const pct = budget && directCost ? Math.round(((directCost - budget) / budget) * 100) : null
  const overBudget = pct !== null && pct > 0
  const underBudget = pct !== null && pct <= 0
  const walletColor = overBudget ? '#ef4444' : underBudget ? '#4ade80' : '#60a5fa'
  const deltaColor = costDelta !== null ? (costDelta > 0 ? '#ef4444' : '#4ade80') : 'transparent'

  return (
    <div
      onMouseDown={onMouseDown}
      onTouchStart={onTouchStart}
      style={{
        position: 'fixed',
        left: pos.x,
        top: pos.y,
        zIndex: 100,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'flex-end',
        gap: 6,
        cursor: 'grab',
        userSelect: 'none',
        touchAction: 'none',
      }}
    >
      {/* Delta flash */}
      {costDelta !== null && (
        <div style={{
          background: deltaColor + '20',
          border: `1px solid ${deltaColor}60`,
          color: deltaColor,
          borderRadius: 8,
          padding: '4px 10px',
          fontSize: 13,
          fontFamily: 'monospace',
          fontWeight: 600,
        }}>
          {costDelta > 0 ? '+' : ''}{inLakhs(Math.abs(costDelta))}
        </div>
      )}

      {/* Wallet pill */}
      <div style={{
        background: '#161b22',
        border: `1px solid ${walletColor}50`,
        borderRadius: 12,
        padding: '10px 16px',
        boxShadow: `0 4px 24px rgba(0,0,0,0.5), 0 0 0 1px ${walletColor}20`,
        minWidth: 188,
      }}>
        {/* drag handle hint */}
        <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 4 }}>
          <div style={{ width: 28, height: 3, borderRadius: 2, background: '#30363d' }} />
        </div>
        <div style={{ display: 'flex', alignItems: 'baseline', gap: 6, justifyContent: 'space-between' }}>
          <span style={{ fontSize: 11, color: '#7d8590', fontFamily: 'monospace' }}>
            ESTIMATE ({decisionsCount}/{totalDecisions})
          </span>
          {pct !== null && (
            <span style={{ fontSize: 10, color: walletColor, fontFamily: 'monospace' }}>
              {pct > 0 ? `+${pct}%` : `${pct}%`}
            </span>
          )}
        </div>
        <div style={{ fontSize: 22, fontWeight: 700, fontFamily: 'monospace', color: walletColor, marginTop: 2, letterSpacing: '-0.5px' }}>
          {inLakhs(directCost)}
        </div>
        {budget && (
          <div style={{ fontSize: 10, color: '#7d8590', fontFamily: 'monospace', marginTop: 2 }}>
            budget {inLakhs(budget)}
          </div>
        )}
      </div>
    </div>
  )
}
