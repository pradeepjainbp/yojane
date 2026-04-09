import type { BuildScores, Component, PlotConfig, Decision } from '@/types'

// ── Score weights by building type ───────────────────────────
const COMFORT_WEIGHTS: Record<string, { thermal: number; light: number; ventilation: number; acoustic: number; spatial: number }> = {
  residential: { thermal: 0.35, light: 0.20, ventilation: 0.20, acoustic: 0.15, spatial: 0.10 },
  apartment:   { thermal: 0.30, light: 0.20, ventilation: 0.20, acoustic: 0.20, spatial: 0.10 },
  commercial:  { thermal: 0.25, light: 0.25, ventilation: 0.15, acoustic: 0.25, spatial: 0.10 },
  agricultural:{ thermal: 0.20, light: 0.10, ventilation: 0.40, acoustic: 0.00, spatial: 0.30 },
  utility:     { thermal: 0.20, light: 0.15, ventilation: 0.20, acoustic: 0.10, spatial: 0.35 },
}

// ── Helpers ──────────────────────────────────────────────────
function getDecision(decisions: Decision[], id: string): string | null {
  return decisions.find(d => d.decision_id === id)?.chosen_option_id ?? null
}

/** Find the chosen Component for a given decision, from the passed component list. */
function getComponent(decisions: Decision[], decisionId: string, components: Component[]): Component | null {
  const optionId = getDecision(decisions, decisionId)
  if (!optionId) return null
  return components.find(c => c.component_id === optionId) ?? null
}

/** Scale a 0–10 registry score to 0–100. */
function scale(score: number | null, fallback = 50): number {
  if (score === null) return fallback
  return Math.round(Math.min(100, Math.max(0, score * 10)))
}

// ============================================================
// COMFORT SCORE (0–100)
// ============================================================
export function calculateComfortScore(
  decisions: Decision[],
  plot: PlotConfig,
  buildingType: string,
  components: Component[],
): { score: number; breakdown: BuildScores['score_breakdown']['comfort'] } {
  const weights = COMFORT_WEIGHTS[buildingType] ?? COMFORT_WEIGHTS.residential

  // ── Thermal ──────────────────────────────────────────────
  // Use thermal_resistance_score (0–10) from wall (B2), roof covering (C2), insulation (C3)
  const wallComp   = getComponent(decisions, 'B2', components)
  const roofComp   = getComponent(decisions, 'C2', components)
  const insComp    = getComponent(decisions, 'C3', components)

  const wallThermal = wallComp?.thermal_resistance_score ?? 5
  const roofThermal = roofComp?.thermal_resistance_score ?? 3
  const insThermal  = insComp?.thermal_resistance_score  ?? 3

  // Weighted average of envelope thermal scores
  const envelopeThermal = (wallThermal * 0.35 + roofThermal * 0.40 + insThermal * 0.25)

  // Climate bonus: warm-humid and hot-dry climates reward higher thermal resistance more
  const climateMultiplier = (plot.climate_zone === 'warm_humid' || plot.climate_zone === 'hot_dry') ? 1.1 : 1.0

  // Road-facing orientation bonus/penalty (N/NE best in hot climates)
  const orientationBonus: Record<string, number> = { N: 0.5, NE: 0.5, E: 0.3, NW: 0.3, SE: -0.2, S: -0.2, SW: -0.5, W: -0.5 }
  const orientMod = orientationBonus[plot.road_facing] ?? 0

  const thermal = Math.round(Math.min(100, Math.max(0,
    (envelopeThermal * climateMultiplier + orientMod) * 10
  )))

  // ── Natural Light ─────────────────────────────────────────
  const lightBonus: Record<string, number> = { NE: 0.95, E: 0.90, N: 0.85, SE: 0.80, S: 0.75, NW: 0.70, W: 0.65, SW: 0.60 }
  const natural_light = Math.round((lightBonus[plot.road_facing] ?? 0.75) * 100)

  // ── Ventilation ───────────────────────────────────────────
  // Wall config from list-picker decisions (B3 has no registry data)
  const wallConfig = getDecision(decisions, 'B3')
  const ventBase = wallConfig === 'WALLCFG-CAVITY' ? 0.85 : wallConfig === 'WALLCFG-INSULATED' ? 0.75 : 0.70
  const ventClimate = plot.climate_zone === 'warm_humid' ? 0.05 : 0
  const ventilation = Math.round(Math.min(100, (ventBase + ventClimate) * 100))

  // ── Acoustic ──────────────────────────────────────────────
  // Use acoustic_score (0–10) from wall component
  const acoustic = scale(wallComp?.acoustic_score ?? null, 50)

  // ── Spatial ───────────────────────────────────────────────
  const spatialBase = plot.plot_area_sqft > 1500 ? 0.9 : plot.plot_area_sqft > 800 ? 0.75 : 0.60
  const spatial = Math.round(spatialBase * 100)

  const score = Math.round(
    thermal      * weights.thermal +
    natural_light * weights.light +
    ventilation  * weights.ventilation +
    acoustic     * weights.acoustic +
    spatial      * weights.spatial
  )

  return {
    score: Math.min(100, Math.max(0, score)),
    breakdown: { thermal, natural_light, ventilation, acoustic, spatial },
  }
}

// ============================================================
// DURABILITY INDEX (0–100)
// ============================================================
export function calculateDurabilityScore(
  decisions: Decision[],
  plot: PlotConfig,
  components: Component[],
): number {
  // Weighted by structural importance
  const slots: { decisionId: string; weight: number }[] = [
    { decisionId: 'A1', weight: 0.25 },  // Foundation
    { decisionId: 'B1', weight: 0.20 },  // Structural system
    { decisionId: 'B2', weight: 0.20 },  // Wall material
    { decisionId: 'C2', weight: 0.15 },  // Roof covering
    { decisionId: 'C4', weight: 0.10 },  // Waterproofing
    { decisionId: 'D1', weight: 0.05 },  // Flooring
    { decisionId: 'E1', weight: 0.05 },  // Plumbing
  ]

  // Coastal/humid climate penalty on durability
  const climatePenalty = plot.climate_zone === 'warm_humid' ? 0.92 : 1.0

  let weightedSum = 0
  let weightUsed = 0

  for (const slot of slots) {
    const comp = getComponent(decisions, slot.decisionId, components)
    if (!comp) continue
    const compScore = (comp.durability_score ?? 5) * climatePenalty
    weightedSum += compScore * slot.weight
    weightUsed  += slot.weight
  }

  if (weightUsed === 0) return 50
  return Math.round(Math.min(100, Math.max(0, (weightedSum / weightUsed) * 10)))
}

// ============================================================
// RESILIENCE RATING (0–100)
// ============================================================
export function calculateResilienceScore(
  decisions: Decision[],
  plot: PlotConfig,
  components: Component[],
): { score: number; breakdown: BuildScores['score_breakdown']['resilience'] } {
  const seismicWeights: Record<string, number> = { II: 0.1, III: 0.2, IV: 0.3, V: 0.4 }
  const seismicW = seismicWeights[plot.seismic_zone] ?? 0.2

  // Seismic — foundation durability score as proxy
  const foundComp = getComponent(decisions, 'A1', components)
  const seismic = scale(foundComp?.durability_score ?? null, 60)

  // Monsoon — plinth + DPC from list-picker decisions (no registry data yet)
  const plinthChoice = getDecision(decisions, 'A7')
  const plinthScores: Record<string, number> = { 'PLINTH-450': 50, 'PLINTH-600': 65, 'PLINTH-750': 80, 'PLINTH-900': 95 }
  const plinthScore = plinthChoice ? (plinthScores[plinthChoice] ?? 65) : 65

  const dpcChoice = getDecision(decisions, 'A5')
  const dpcScores: Record<string, number> = { 'DPC-CEMENT': 60, 'DPC-BITUMEN': 75, 'DPC-POLYMER': 92 }
  const dpcScore = dpcChoice ? (dpcScores[dpcChoice] ?? 60) : 60

  const monsoon = Math.round(plinthScore * 0.5 + dpcScore * 0.5)

  // Termite — use durability_score of soil treatment component (A6)
  const soilComp = getComponent(decisions, 'A6', components)
  const termite = scale(soilComp?.durability_score ?? null, 50)

  // Wind — use moisture_resistance of roof covering as proxy
  const roofComp = getComponent(decisions, 'C2', components)
  const moistureMap: Record<string, number> = { High: 85, Medium: 65, Low: 40 }
  const wind = roofComp?.moisture_resistance ? (moistureMap[roofComp.moisture_resistance] ?? 65) : 65

  const rainfallW = plot.rainfall_mm > 1500 ? 0.40 : plot.rainfall_mm > 800 ? 0.30 : 0.20
  const termiteW  = 0.25
  const windW     = 0.15

  const score = Math.round(Math.min(100, Math.max(0,
    seismic  * seismicW +
    monsoon  * rainfallW +
    termite  * termiteW +
    wind     * windW
  )))

  return { score, breakdown: { seismic, monsoon, wind, termite } }
}

// ============================================================
// TCO — Total Cost of Ownership over 20 years (₹/sqft)
// ============================================================
export function calculateTCO(
  decisions: Decision[],
  plot: PlotConfig,
  components: Component[],
): number {
  const builtUpSqft = plot.plot_area_sqft * plot.floors

  // Year-0 construction cost: sum (base + installation) per chosen component
  // For components without registry data we use Karnataka benchmark base
  const baseBenchmark = 1800  // ₹/sqft structural base (foundation + columns + beam)

  let materialCostPerSqft = 0
  for (const comp of components) {
    materialCostPerSqft += (comp.base_cost_per_sqft_inr ?? 0) + (comp.installation_cost_per_sqft_inr ?? 0)
  }
  // If no components chosen yet, fall back to benchmark
  const constructionCostPerSqft = materialCostPerSqft > 0
    ? baseBenchmark * 0.4 + materialCostPerSqft   // 40% structural base + finish costs
    : baseBenchmark

  const year0 = constructionCostPerSqft * builtUpSqft

  // Annual maintenance: weighted average of annual_minor_maint_factor across chosen components
  let maintFactorSum = 0
  let maintCount = 0
  for (const comp of components) {
    if (comp.annual_minor_maint_factor !== null) {
      maintFactorSum += comp.annual_minor_maint_factor
      maintCount++
    }
  }
  const avgMaintFactor = maintCount > 0 ? maintFactorSum / maintCount : 0.005
  const annualMaint = year0 * avgMaintFactor

  // Annual energy cost via energy_impact_modifier
  // Base: 1800 kWh/yr per 1000 sqft for Karnataka residential
  const baseAnnualKWh = (builtUpSqft / 1000) * 1800
  let energyModSum = 0
  let energyModCount = 0
  for (const comp of components) {
    if (comp.energy_impact_modifier !== null) {
      energyModSum += comp.energy_impact_modifier
      energyModCount++
    }
  }
  const avgEnergyMod = energyModCount > 0 ? energyModSum / energyModCount : 0
  const adjustedKWh = baseAnnualKWh * (1 - avgEnergyMod * 0.3)  // 30% max swing
  const electricityRate = 7.5  // ₹/kWh BESCOM 2024
  const annualEnergy = adjustedKWh * electricityRate

  // PV of 20-year running costs at 7% discount
  const pvFactor = (1 - Math.pow(1.07, -20)) / 0.07  // ≈ 10.59
  const tco20yr = year0 + (annualMaint + annualEnergy) * pvFactor

  return Math.round(tco20yr / builtUpSqft)  // ₹/sqft
}

// ============================================================
// CARBON FOOTPRINT (kgCO₂/sqft)
// ============================================================
export function calculateCarbon(
  decisions: Decision[],
  plot: PlotConfig,
  components: Component[],
): number {
  const builtUpSqft = plot.plot_area_sqft * plot.floors

  // Embodied carbon: base structural + chosen component impacts
  // energy_impact_modifier < 0 means more carbon, > 0 means less
  const baseEmbodied = 95  // kgCO2/sqft — Karnataka concrete structure baseline

  let energyModSum = 0
  let energyModCount = 0
  for (const comp of components) {
    if (comp.energy_impact_modifier !== null) {
      energyModSum += comp.energy_impact_modifier
      energyModCount++
    }
  }
  const avgEnergyMod = energyModCount > 0 ? energyModSum / energyModCount : 0

  // Positive modifier = lower carbon embodied (green materials)
  const embodied = Math.max(50, baseEmbodied * (1 - avgEnergyMod * 0.25))

  // Operational carbon over 20 years
  const baseAnnualKWh = (builtUpSqft / 1000) * 1800
  const adjustedKWh = baseAnnualKWh * (1 - avgEnergyMod * 0.30)
  const gridEmissionFactor = 0.7  // kgCO2/kWh Indian grid (CEA 2024)
  const operationalCarbon = (adjustedKWh * gridEmissionFactor * 20) / builtUpSqft

  return Math.round(embodied + operationalCarbon)
}

// ============================================================
// MASTER: Calculate all scores
// ============================================================
export function calculateAllScores(
  decisions: Decision[],
  plot: PlotConfig,
  buildingType: string,
  chosenComponents: Component[] = [],
): BuildScores {
  const { score: comfort, breakdown: comfortBreakdown } = calculateComfortScore(decisions, plot, buildingType, chosenComponents)
  const durability  = calculateDurabilityScore(decisions, plot, chosenComponents)
  const { score: resilience, breakdown: resBreakdown } = calculateResilienceScore(decisions, plot, chosenComponents)
  const tco    = calculateTCO(decisions, plot, chosenComponents)
  const carbon = calculateCarbon(decisions, plot, chosenComponents)

  return {
    comfort,
    durability,
    tco,
    resilience,
    carbon,
    score_breakdown: {
      comfort: comfortBreakdown,
      durability: { foundation: 0, structure: 0, envelope: 0, finishes: 0, mep: 0 },
      resilience: resBreakdown,
    },
  }
}
