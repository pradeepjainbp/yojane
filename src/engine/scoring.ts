import type { BuildScores, PlotConfig, Decision, ClimateZone } from '@/types'

// ── Score weights by building type ───────────────────────────
const COMFORT_WEIGHTS: Record<string, { thermal: number; light: number; ventilation: number; acoustic: number; spatial: number }> = {
  residential: { thermal: 0.35, light: 0.20, ventilation: 0.20, acoustic: 0.15, spatial: 0.10 },
  apartment:   { thermal: 0.30, light: 0.20, ventilation: 0.20, acoustic: 0.20, spatial: 0.10 },
  commercial:  { thermal: 0.25, light: 0.25, ventilation: 0.15, acoustic: 0.25, spatial: 0.10 },
  agricultural:{ thermal: 0.20, light: 0.10, ventilation: 0.40, acoustic: 0.00, spatial: 0.30 },
  utility:     { thermal: 0.20, light: 0.15, ventilation: 0.20, acoustic: 0.10, spatial: 0.35 },
}

// ── U-value lookup (W/m²K) for common wall materials ─────────
const WALL_U_VALUES: Record<string, number> = {
  'WALL-AAC-200':  0.70,
  'WALL-REDBRK':   1.80,
  'WALL-FLYASH':   1.60,
  'WALL-LATERITE': 1.20,
  'WALL-SCB':      2.10,
  'WALL-HCB':      1.50,
}

// ── Roof U-values ─────────────────────────────────────────────
const ROOF_U_VALUES: Record<string, number> = {
  'ROOF-FLAT-RCC':      3.50,
  'ROOF-PITCHED-WOOD':  2.20,
  'ROOF-PITCHED-STEEL': 4.00,
  'ROOF-SLOPED-RCC':    3.00,
}

// ── Insulation U-value reduction multipliers ──────────────────
const INSULATION_MULTIPLIERS: Record<string, number> = {
  'INS-NONE':        1.00,
  'INS-CHINAMOSAIC': 0.75,
  'INS-MUDPHUSKA':   0.65,
  'INS-XPS':         0.35,
  'INS-COOLROOF':    0.55,
  'INS-GREENROOF':   0.45,
}

// ── Climate zone ideal U-values (lower = better in hot climates) ─
const CLIMATE_TARGET_U: Record<ClimateZone, number> = {
  hot_dry:    0.8,
  warm_humid: 0.7,
  composite:  0.9,
  temperate:  1.2,
  cold:       0.5,
}

// ── EUL (Expected Useful Life) by decision option ─────────────
const OPTION_EUL: Record<string, number> = {
  'FDN-ISOLATED': 60, 'FDN-STRIP': 60, 'FDN-RAFT': 60, 'FDN-PILE': 80,
  'WALL-AAC-200': 50, 'WALL-REDBRK': 60, 'WALL-FLYASH': 55, 'WALL-LATERITE': 70, 'WALL-SCB': 45, 'WALL-HCB': 40,
  'ROOF-FLAT-RCC': 40, 'ROOF-PITCHED-WOOD': 25, 'ROOF-PITCHED-STEEL': 35, 'ROOF-SLOPED-RCC': 40,
  'WP-BITUMEN': 10, 'WP-APPMOD': 15, 'WP-POLYMER': 20, 'WP-INTEGRAL': 15,
  'FLOOR-GRANITE': 40, 'FLOOR-VIT-DC': 25, 'FLOOR-KOTA': 50, 'FLOOR-MARBLE': 35,
}

// ── STC ratings for walls ─────────────────────────────────────
const WALL_STC: Record<string, number> = {
  'WALL-AAC-200': 45, 'WALL-REDBRK': 50, 'WALL-FLYASH': 48,
  'WALL-LATERITE': 52, 'WALL-SCB': 42, 'WALL-HCB': 38,
}

function getDecisionByStage(decisions: Decision[], stage: string, num: string): string | null {
  return decisions.find(d => d.decision_id === `${stage}${num}`)?.chosen_option_id ?? null
}

// ============================================================
// COMFORT SCORE (0–100)
// ============================================================
export function calculateComfortScore(
  decisions: Decision[],
  plot: PlotConfig,
  buildingType: string
): { score: number; breakdown: BuildScores['score_breakdown']['comfort'] } {
  const weights = COMFORT_WEIGHTS[buildingType] ?? COMFORT_WEIGHTS.residential

  // ── Thermal ──────────────────────────────────────────────
  const wallChoice = getDecisionByStage(decisions, 'B', '2')
  const roofChoice = getDecisionByStage(decisions, 'C', '1')
  const insChoice  = getDecisionByStage(decisions, 'C', '3')

  const wallU = wallChoice ? (WALL_U_VALUES[wallChoice] ?? 2.0) : 2.0
  const roofU = roofChoice ? (ROOF_U_VALUES[roofChoice] ?? 3.5) : 3.5
  const insMulti = insChoice ? (INSULATION_MULTIPLIERS[insChoice] ?? 1.0) : 1.0
  const effectiveRoofU = roofU * insMulti

  const targetU = CLIMATE_TARGET_U[plot.climate_zone] ?? 1.0
  const thermalWall = Math.max(0, 1 - (wallU - targetU) / 3)
  const thermalRoof = Math.max(0, 1 - (effectiveRoofU - targetU) / 4)

  // Road-facing orientation penalty/bonus (N/NE is best in hot climates)
  const orientationBonus: Record<string, number> = { N: 0.1, NE: 0.1, E: 0.05, NW: 0.05, SE: -0.05, S: -0.05, SW: -0.1, W: -0.1 }
  const orientMod = orientationBonus[plot.road_facing] ?? 0
  const thermalRaw = (thermalWall * 0.5 + thermalRoof * 0.5) + orientMod
  const thermal = Math.round(Math.min(100, Math.max(0, thermalRaw * 100)))

  // ── Natural Light ─────────────────────────────────────────
  // Simplified: east/north-east facing gets bonus
  const lightBonus: Record<string, number> = { NE: 0.95, E: 0.90, N: 0.85, SE: 0.80, S: 0.75, NW: 0.70, W: 0.65, SW: 0.60 }
  const natural_light = Math.round((lightBonus[plot.road_facing] ?? 0.75) * 100)

  // ── Ventilation ───────────────────────────────────────────
  // Wall config cavity = better cross-ventilation
  const wallConfig = getDecisionByStage(decisions, 'B', '3')
  const ventBase = wallConfig === 'WALLCFG-CAVITY' ? 0.85 : wallConfig === 'WALLCFG-INSULATED' ? 0.75 : 0.70
  const ventClimate = plot.climate_zone === 'warm_humid' ? 0.05 : 0
  const ventilation = Math.round(Math.min(100, (ventBase + ventClimate) * 100))

  // ── Acoustic ──────────────────────────────────────────────
  const stc = wallChoice ? (WALL_STC[wallChoice] ?? 40) : 40
  const acoustic = Math.round(Math.min(100, ((stc - 30) / 30) * 100))

  // ── Spatial ───────────────────────────────────────────────
  // Based on plot area vs floors
  const spatialBase = plot.plot_area_sqft > 1500 ? 0.9 : plot.plot_area_sqft > 800 ? 0.75 : 0.60
  const spatial = Math.round(spatialBase * 100)

  const score = Math.round(
    thermal * weights.thermal +
    natural_light * weights.light +
    ventilation * weights.ventilation +
    acoustic * weights.acoustic +
    spatial * weights.spatial
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
): number {
  const components = [
    { id: 'A1', weight: 0.25, maxEUL: 80 },  // Foundation
    { id: 'B1', weight: 0.20, maxEUL: 60 },  // Structure
    { id: 'B2', weight: 0.20, maxEUL: 70 },  // Walls
    { id: 'C1', weight: 0.15, maxEUL: 50 },  // Roof
    { id: 'C4', weight: 0.10, maxEUL: 20 },  // Waterproofing
    { id: 'D1', weight: 0.05, maxEUL: 50 },  // Flooring
    { id: 'E1', weight: 0.05, maxEUL: 40 },  // Plumbing
  ]

  // Coastal penalty
  const climatePenalty = plot.climate_zone === 'warm_humid' ? 0.90 : 1.0

  let score = 0
  let totalWeight = 0

  for (const comp of components) {
    const dec = decisions.find(d => d.decision_id === comp.id)
    if (!dec) continue
    const eul = OPTION_EUL[dec.chosen_option_id] ?? 30
    const compScore = (eul / comp.maxEUL) * climatePenalty
    score += compScore * comp.weight
    totalWeight += comp.weight
  }

  if (totalWeight === 0) return 50  // Default if no decisions made
  return Math.round(Math.min(100, (score / totalWeight) * 100))
}

// ============================================================
// RESILIENCE RATING (0–100)
// ============================================================
export function calculateResilienceScore(
  decisions: Decision[],
  plot: PlotConfig,
): number {
  const seismicWeights: Record<string, number> = { II: 0.1, III: 0.2, IV: 0.3, V: 0.4 }
  const seismicW = seismicWeights[plot.seismic_zone] ?? 0.2

  // Seismic — foundation and structure choice
  const foundChoice = getDecisionByStage(decisions, 'A', '1')
  const seismicScores: Record<string, number> = { 'FDN-RAFT': 90, 'FDN-PILE': 95, 'FDN-ISOLATED': 75, 'FDN-STRIP': 65 }
  const seismicScore = foundChoice ? (seismicScores[foundChoice] ?? 70) : 50

  // Monsoon — plinth height + DPC + RWH
  const plinthChoice = getDecisionByStage(decisions, 'A', '7')
  const plinthScores: Record<string, number> = { 'PLINTH-450': 50, 'PLINTH-600': 65, 'PLINTH-750': 80, 'PLINTH-900': 95 }
  const plinthScore = plinthChoice ? (plinthScores[plinthChoice] ?? 65) : 65

  const dpcChoice = getDecisionByStage(decisions, 'A', '5')
  const dpcScores: Record<string, number> = { 'DPC-CEMENT': 60, 'DPC-BITUMEN': 75, 'DPC-POLYMER': 92 }
  const dpcScore = dpcChoice ? (dpcScores[dpcChoice] ?? 60) : 60

  const monsoonScore = Math.round((plinthScore * 0.5 + dpcScore * 0.5))

  // Termite resilience
  const termChoice = getDecisionByStage(decisions, 'A', '6')
  const termScores: Record<string, number> = { 'TERM-NONE': 10, 'TERM-CHEMICAL': 65, 'TERM-MESH': 95, 'TERM-DUAL': 98 }
  const termiteScore = termChoice ? (termScores[termChoice] ?? 50) : 50

  // Rainfall factor for monsoon weight
  const rainfallW = plot.rainfall_mm > 1500 ? 0.4 : plot.rainfall_mm > 800 ? 0.3 : 0.2
  const termiteW = 0.25
  const windW = 0.15

  const windScore = 75  // Default; would vary with wind zone choice

  const totalScore = Math.round(
    seismicScore * seismicW +
    monsoonScore * rainfallW +
    termiteScore * termiteW +
    windScore * windW
  )

  return Math.min(100, Math.max(0, totalScore))
}

// ============================================================
// TCO (Total Cost of Ownership over 20 years in ₹/sqft)
// ============================================================
export function calculateTCO(
  decisions: Decision[],
  plot: PlotConfig,
): number {
  // Base construction cost per sqft by building type
  const baseCost = 1800  // ₹/sqft — Karnataka residential benchmark 2025

  // Material cost adjustments
  const wallChoice = getDecisionByStage(decisions, 'B', '2')
  const wallCostAdj: Record<string, number> = {
    'WALL-AAC-200': 80, 'WALL-REDBRK': 0, 'WALL-FLYASH': -20,
    'WALL-LATERITE': 50, 'WALL-SCB': -40, 'WALL-HCB': -60,
  }
  const wallAdj = wallChoice ? (wallCostAdj[wallChoice] ?? 0) : 0

  const roofChoice = getDecisionByStage(decisions, 'C', '1')
  const roofCostAdj: Record<string, number> = {
    'ROOF-FLAT-RCC': 0, 'ROOF-PITCHED-WOOD': 80, 'ROOF-PITCHED-STEEL': 50, 'ROOF-SLOPED-RCC': 30,
  }
  const roofAdj = roofChoice ? (roofCostAdj[roofChoice] ?? 0) : 0

  const constructionCost = (baseCost + wallAdj + roofAdj) * plot.plot_area_sqft * plot.floors

  // Annual energy cost (simplified)
  const wallU = wallChoice ? (WALL_U_VALUES[wallChoice] ?? 2.0) : 2.0
  const insChoice = getDecisionByStage(decisions, 'C', '3')
  const insM = insChoice ? (INSULATION_MULTIPLIERS[insChoice] ?? 1.0) : 1.0
  const effectiveU = (wallU + (roofChoice ? (ROOF_U_VALUES[roofChoice] ?? 3.5) : 3.5)) / 2 * insM

  // kWh estimate: U-value × HDD/CDD × area × energy price
  const annualKWh = effectiveU * 1200 * (plot.plot_area_sqft * 0.09)  // rough cooling estimate
  const electricityRate = 7.5  // ₹/kWh BESCOM average
  const annualEnergyCost = annualKWh * electricityRate

  // 20-year maintenance (simplified average)
  const annualMaintenance = constructionCost * 0.005  // 0.5% of construction cost per year

  // PV of 20-year running costs at 7% discount rate
  const discountRate = 0.07
  const pvFactor = (1 - Math.pow(1 + discountRate, -20)) / discountRate  // ≈ 10.59

  const totalTCO = constructionCost + (annualEnergyCost + annualMaintenance) * pvFactor

  return Math.round(totalTCO / (plot.plot_area_sqft * plot.floors))  // ₹/sqft
}

// ============================================================
// CARBON FOOTPRINT (kgCO₂/sqft)
// ============================================================
export function calculateCarbon(
  decisions: Decision[],
  plot: PlotConfig,
): number {
  // Embodied carbon estimates per sqft by key material choices
  const wallChoice = getDecisionByStage(decisions, 'B', '2')
  const wallCarbon: Record<string, number> = {
    'WALL-AAC-200': 28, 'WALL-REDBRK': 45, 'WALL-FLYASH': 22,
    'WALL-LATERITE': 18, 'WALL-SCB': 52, 'WALL-HCB': 48,
  }
  const wallC = wallChoice ? (wallCarbon[wallChoice] ?? 40) : 40

  const roofChoice = getDecisionByStage(decisions, 'C', '1')
  const roofCarbon: Record<string, number> = {
    'ROOF-FLAT-RCC': 35, 'ROOF-PITCHED-WOOD': 12, 'ROOF-PITCHED-STEEL': 28, 'ROOF-SLOPED-RCC': 30,
  }
  const roofC = roofChoice ? (roofCarbon[roofChoice] ?? 35) : 35

  const embodied = wallC + roofC + 60  // 60 = foundation + structure base

  // Operational carbon — 20 years
  const wallU = wallChoice ? (WALL_U_VALUES[wallChoice] ?? 2.0) : 2.0
  const insChoice = getDecisionByStage(decisions, 'C', '3')
  const insM = insChoice ? (INSULATION_MULTIPLIERS[insChoice] ?? 1.0) : 1.0
  const annualKWh = wallU * insM * 1200 * (plot.plot_area_sqft * 0.09)
  const gridEmissionFactor = 0.7  // kgCO2/kWh Indian grid (CEA 2024)
  const operationalCarbon = (annualKWh * gridEmissionFactor * 20) / plot.plot_area_sqft

  return Math.round(embodied + operationalCarbon)
}

// ============================================================
// MASTER: Calculate all scores
// ============================================================
export function calculateAllScores(
  decisions: Decision[],
  plot: PlotConfig,
  buildingType: string
): BuildScores {
  const { score: comfort, breakdown: comfortBreakdown } = calculateComfortScore(decisions, plot, buildingType)
  const durability = calculateDurabilityScore(decisions, plot)
  const resilience = calculateResilienceScore(decisions, plot)
  const tco = calculateTCO(decisions, plot)
  const carbon = calculateCarbon(decisions, plot)

  return {
    comfort,
    durability,
    tco,
    resilience,
    carbon,
    score_breakdown: {
      comfort: comfortBreakdown,
      durability: {
        foundation: 0, structure: 0, envelope: 0, finishes: 0, mep: 0,
      },
      resilience: {
        monsoon: 0, seismic: 0, wind: 0, termite: 0,
      },
    },
  }
}
