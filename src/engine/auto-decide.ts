import { allDecisions } from '@/data/decision-points'
import { calculateAllScores } from './scoring'
import type { Component, PlotConfig, Decision, Stage } from '@/types'

// ── Score a single Component for a given plot (0–100) ────────
// Weights: durability 35% · climate fit 30% · value 20% · low carbon 15%
function scoreComponent(comp: Component, plot: PlotConfig): number {
  // Durability: registry durability_score is 0–10
  const durability = ((comp.durability_score ?? 5) / 10) * 100

  // Climate fit: check if user's climate zone appears in the component's climate_zone list
  // climate_zone field is semicolon-separated e.g. 'Warm-Humid;Hot-Dry'
  // PlotConfig uses snake_case e.g. 'warm_humid' — normalise for comparison
  const registryZones = (comp.climate_zone ?? '').toLowerCase().replace(/-/g, '_').replace(/;/g, ' ')
  const userZone = plot.climate_zone.toLowerCase()
  const climateFit = registryZones.includes(userZone) ? 100 : 50

  // Value: lower total cost = higher value score (inverted, normalised to 0–100)
  // We use spectrum_position as a proxy when no cost data (Basic=100, Ultra-Premium=10)
  const spectrumMap: Record<string, number> = {
    'Basic': 90, 'Intermediate': 70, 'Performance': 50, 'Premium': 30, 'Ultra-Premium': 10,
  }
  const value = spectrumMap[comp.spectrum_position ?? 'Intermediate'] ?? 50

  // Low carbon: positive energy_impact_modifier = greener (saves energy/carbon)
  const energyMod = comp.energy_impact_modifier ?? 0
  const carbon = Math.round(50 + energyMod * 50)  // -1→0, 0→50, +1→100

  return Math.round(
    durability * 0.35 +
    climateFit * 0.30 +
    value      * 0.20 +
    carbon     * 0.15
  )
}

export interface AutoDecideResult {
  feasible: boolean
  decisions: Decision[]
  estimatedCostPerSqft: number
  estimatedTotalCost: number
  budgetPerSqft: number
  shortfall: number
  reasoning: Record<string, { chosen: string; chosenName: string; score: number; why: string }>
}

export function autoDecide(
  plot: PlotConfig,
  buildingType: string,
  componentsBySubcategory: Record<string, Component[]>,
): AutoDecideResult {
  const budget = plot.target_budget_inr ?? 0
  const builtUpArea = plot.plot_area_sqft * plot.floors
  const budgetPerSqft = budget > 0 ? budget / builtUpArea : Infinity

  // Budget tier guidance: map spectrum_position to max allowed position by budget
  // ₹1500/sqft → Basic only; ₹2000 → up to Intermediate; ₹3000 → up to Performance; ₹4000+ → any
  const spectrumOrder = ['Basic', 'Intermediate', 'Performance', 'Premium', 'Ultra-Premium']
  let maxSpectrumIdx = 4  // no limit by default
  if (budget > 0) {
    if (budgetPerSqft < 1800) maxSpectrumIdx = 1
    else if (budgetPerSqft < 2500) maxSpectrumIdx = 2
    else if (budgetPerSqft < 3500) maxSpectrumIdx = 3
  }

  const decisions: Decision[] = []
  const reasoning: AutoDecideResult['reasoning'] = {}
  const chosenComponents: Component[] = []

  for (const dp of allDecisions) {
    let chosenId: string
    let chosenName: string
    let chosenScore: number
    let why: string

    if (dp.subcategory && componentsBySubcategory[dp.subcategory]?.length > 0) {
      // Registry-backed decision — pick best-scoring component within budget tier
      const candidates = componentsBySubcategory[dp.subcategory].map(comp => ({
        comp,
        score: scoreComponent(comp, plot),
        specIdx: spectrumOrder.indexOf(comp.spectrum_position ?? 'Intermediate'),
      }))

      // Filter by budget tier
      const withinBudget = candidates.filter(c => c.specIdx <= maxSpectrumIdx)
      const pool = withinBudget.length > 0 ? withinBudget : candidates  // fallback to any if all out of budget

      // Pick highest scoring
      pool.sort((a, b) => b.score - a.score)
      const best = pool[0]

      chosenId    = best.comp.component_id
      chosenName  = best.comp.display_name
      chosenScore = best.score
      chosenComponents.push(best.comp)

      const climateMatch = (best.comp.climate_zone ?? '').toLowerCase().replace(/-/g, '_').includes(plot.climate_zone)
      why = `Score ${best.score}/100 · ${climateMatch ? 'Good climate fit' : 'Available for your region'} · ${best.comp.spectrum_position ?? 'Standard'} tier`

      if (best.comp.ai_advisory_notes) {
        why += ` · ${best.comp.ai_advisory_notes.slice(0, 80)}…`
      }
    } else {
      // No registry data — use default or first option
      chosenId    = dp.default_option ?? dp.options[0] ?? 'UNKNOWN'
      chosenName  = chosenId
      chosenScore = 50
      why = 'System default — no registry data for this decision yet'
    }

    reasoning[dp.id] = { chosen: chosenId, chosenName, score: chosenScore, why }

    decisions.push({
      id: crypto.randomUUID(),
      build_id: '',
      decision_id: dp.id,
      stage: dp.stage as Stage,
      chosen_option_id: chosenId,
      cost_override: null,
      notes: null,
      updated_at: new Date().toISOString(),
    })
  }

  const scores = calculateAllScores(decisions, plot, buildingType, chosenComponents)
  const estimatedCostPerSqft = scores.tco
  const estimatedTotalCost   = estimatedCostPerSqft * builtUpArea

  const feasible = budget === 0 || estimatedTotalCost <= budget * 1.15
  const shortfall = feasible ? 0 : estimatedTotalCost - budget

  return {
    feasible,
    decisions,
    estimatedCostPerSqft: Math.round(estimatedCostPerSqft),
    estimatedTotalCost:   Math.round(estimatedTotalCost),
    budgetPerSqft:        Math.round(budgetPerSqft),
    shortfall:            Math.round(shortfall),
    reasoning,
  }
}
