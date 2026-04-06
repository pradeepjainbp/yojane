import { allDecisions } from '@/data/decision-points'
import { foundationMaterials } from '@/data/materials-foundation'
import { calculateAllScores } from './scoring'
import type { PlotConfig, Decision, MaterialEntry, Stage } from '@/types'

const allMaterials: MaterialEntry[] = [...foundationMaterials]

function getMaterial(id: string): MaterialEntry | null {
  return allMaterials.find(m => m.id === id) ?? null
}

// ── Score a single material option on a 0–100 scale ───────────
// Weights: durability 35%, climate suitability 30%, value 20%, low carbon 15%
function scoreOption(mat: MaterialEntry, plot: PlotConfig): number {
  const durabilityScore = (mat.expected_useful_life_years / 80) * 100

  const climateSuit = mat.climate_suitability[plot.climate_zone] ?? 0.7
  const climateScore = climateSuit * 100

  // Value = inverse of cost (normalised within category — lower is better value per unit)
  // We'll treat this relative to range, so alone it contributes a neutral midpoint
  const valueScore = 50  // resolved relatively across options below

  const carbonScore = Math.max(0, 100 - mat.carbon_footprint_kgco2 * 0.5)

  return (
    durabilityScore * 0.35 +
    climateScore * 0.30 +
    valueScore * 0.20 +
    carbonScore * 0.15
  )
}

export interface AutoDecideResult {
  feasible: boolean
  decisions: Decision[]
  estimatedCostPerSqft: number
  estimatedTotalCost: number
  budgetPerSqft: number
  shortfall: number  // how much over budget (0 if feasible)
  reasoning: Record<string, { chosen: string; why: string; costPerUnit: number }>
}

export function autoDecide(plot: PlotConfig, buildingType: string): AutoDecideResult {
  const budget = plot.target_budget_inr ?? 0
  const builtUpArea = plot.plot_area_sqft * plot.floors
  const budgetPerSqft = budget > 0 ? budget / builtUpArea : Infinity

  // Karnataka benchmark construction cost breakdown (₹/sqft)
  // Foundation ~15%, Structure ~25%, Envelope ~20%, Interiors ~25%, MEP ~15%
  const STAGE_BUDGET_SHARE: Record<string, number> = {
    A: 0.15, B: 0.25, C: 0.20, D: 0.25, E: 0.15, F: 0.05,
  }

  const decisions: Decision[] = []
  const reasoning: AutoDecideResult['reasoning'] = {}

  for (const dp of allDecisions) {
    const stageBudgetPct = STAGE_BUDGET_SHARE[dp.stage] ?? 0.15
    const stageBudgetPerSqft = budgetPerSqft * stageBudgetPct

    // Gather options that have material data
    const candidates = dp.options
      .map(id => {
        const mat = getMaterial(id)
        if (!mat) return null
        const costPerUnit = mat.cost_per_unit_material + mat.cost_per_unit_labor
        const score = scoreOption(mat, plot)
        return { id, mat, costPerUnit, score }
      })
      .filter(Boolean) as { id: string; mat: MaterialEntry; costPerUnit: number; score: number }[]

    let chosen: string
    let why: string
    let chosenCost = 0

    if (candidates.length === 0) {
      // No material data — use default or first
      chosen = dp.default_option ?? dp.options[0]
      why = 'No cost data yet — using system default'
      chosenCost = 0
    } else {
      // Sort by score descending
      candidates.sort((a, b) => b.score - a.score)

      if (budget === 0) {
        // No budget set — pick highest scoring option
        const best = candidates[0]
        chosen = best.id
        why = `Best overall score (${Math.round(best.score)}/100) — no budget constraint set`
        chosenCost = best.costPerUnit
      } else {
        // Find the best-scoring option that fits within stage budget allocation
        // Normalise costs relative to budget per sqft for this stage
        const affordable = candidates.filter(c => {
          // Rough check: cost per unit should be within the stage's share
          // This is a heuristic since units differ (per sqft vs per bag etc.)
          return c.costPerUnit <= stageBudgetPerSqft * 15  // 15 = typical unit multiplier
        })

        if (affordable.length > 0) {
          const best = affordable[0]
          chosen = best.id
          why = `Best score (${Math.round(best.score)}/100) within your budget tier`
          chosenCost = best.costPerUnit
        } else {
          // Nothing fits — pick cheapest option
          candidates.sort((a, b) => a.costPerUnit - b.costPerUnit)
          const cheapest = candidates[0]
          chosen = cheapest.id
          why = `Budget is tight — selected most affordable option (₹${cheapest.costPerUnit}/unit)`
          chosenCost = cheapest.costPerUnit
        }
      }
    }

    reasoning[dp.id] = {
      chosen,
      why,
      costPerUnit: chosenCost,
    }

    decisions.push({
      id: crypto.randomUUID(),
      build_id: '',  // filled in by caller
      decision_id: dp.id,
      stage: dp.stage as Stage,
      chosen_option_id: chosen,
      cost_override: null,
      notes: null,
      updated_at: new Date().toISOString(),
    })
  }

  // Calculate resulting scores to estimate cost
  const scores = calculateAllScores(decisions, plot, buildingType)
  const estimatedCostPerSqft = scores.tco * 0.45  // roughly construction portion of TCO
  const estimatedTotalCost = estimatedCostPerSqft * builtUpArea

  const feasible = budget === 0 || estimatedTotalCost <= budget * 1.15  // 15% tolerance
  const shortfall = feasible ? 0 : estimatedTotalCost - budget

  return {
    feasible,
    decisions,
    estimatedCostPerSqft: Math.round(estimatedCostPerSqft),
    estimatedTotalCost: Math.round(estimatedTotalCost),
    budgetPerSqft: Math.round(budgetPerSqft),
    shortfall: Math.round(shortfall),
    reasoning,
  }
}
