// ============================================================
// Yojane — Core Types
// ============================================================

export type BuildingType = 'residential' | 'apartment' | 'commercial' | 'agricultural' | 'utility'
export type Persona =
  | 'young_it_couple'
  | 'joint_family'
  | 'retired_couple'
  | 'budget_first_timer'
  | 'investor'
  | 'small_developer'
  | 'premium_builder'
  | 'small_farmer'

export type ClimateZone = 'hot_dry' | 'warm_humid' | 'composite' | 'temperate' | 'cold'
export type SeismicZone = 'II' | 'III' | 'IV' | 'V'
export type Stage = 'A' | 'B' | 'C' | 'D' | 'E' | 'F'

export interface PlotConfig {
  lat: number
  lng: number
  climate_zone: ClimateZone
  seismic_zone: SeismicZone
  wind_speed_zone: string
  rainfall_mm: number
  soil_type: string
  elevation_m: number
  city_tier: 'tier1' | 'tier2' | 'tier3'
  plot_length_ft: number
  plot_width_ft: number
  plot_area_sqft: number
  floors: number
  road_facing: 'N' | 'NE' | 'E' | 'SE' | 'S' | 'SW' | 'W' | 'NW'
  target_budget_inr: number | null
  vastu_enabled: boolean
  setback_front_ft: number
  setback_side_ft: number
  setback_rear_ft: number
}

export interface Build {
  id: string
  user_id: string
  name: string
  building_type: BuildingType
  sub_type: string | null
  persona: Persona | null
  status: 'draft' | 'complete'
  is_copy_of: string | null
  plot_config: PlotConfig
  created_at: string
  updated_at: string
}

export interface Decision {
  id: string
  build_id: string
  decision_id: string         // e.g. "A1"
  stage: Stage
  chosen_option_id: string
  cost_override: number | null
  notes: string | null
  updated_at: string
}

export interface BuildScores {
  comfort: number             // 0-100
  durability: number          // 0-100
  tco: number                 // INR total 20yr
  resilience: number          // 0-100
  carbon: number              // kgCO2/sqft
  score_breakdown: ScoreBreakdown
}

export interface ScoreBreakdown {
  comfort: {
    thermal: number
    natural_light: number
    ventilation: number
    acoustic: number
    spatial: number
  }
  durability: {
    foundation: number
    structure: number
    envelope: number
    finishes: number
    mep: number
  }
  resilience: {
    monsoon: number
    seismic: number
    wind: number
    termite: number
  }
}

// ============================================================
// Data Registry Types
// ============================================================

export interface MaterialEntry {
  id: string
  name: string
  name_local: string
  category: 'foundation' | 'wall' | 'roof' | 'floor' | 'mep_plumbing' | 'mep_electrical' | 'exterior'
  sub_category: string
  applicable_building_types: BuildingType[]
  unit: string
  unit_metric: string
  cost_per_unit_material: number
  cost_per_unit_labor: number
  cost_source: string
  u_value: number | null
  stc_rating: number | null
  compressive_strength: string | null
  water_absorption: string | null
  fire_rating: string | null
  expected_useful_life_years: number
  maintenance_schedule: MaintenanceItem[]
  carbon_footprint_kgco2: number
  climate_suitability: Partial<Record<ClimateZone, number>>
  contractor_popularity: number
  common_misconception: string | null
  myth_buster_fact: string | null
  vastu_notes: string | null
  technical_spec_ref: string
  visual_ref: string
  pros: string[]
  cons: string[]
}

export interface MaintenanceItem {
  year: number
  task: string
  estimated_cost_inr: number
  complexity: 'low' | 'medium' | 'high'
}

// ============================================================
// Decision Point Types
// ============================================================

export type Difficulty = 1 | 2 | 3  // ★ ★★ ★★★

export interface DecisionPoint {
  id: string              // e.g. "A1"
  stage: Stage
  label: string
  description: string
  classification: 'critical' | 'standard'
  difficulty: Difficulty
  options: string[]       // material IDs
  default_option: string | null
  constraints: DecisionConstraint[]
  vastu_relevant: boolean
}

export interface DecisionConstraint {
  depends_on: string      // decision_id
  condition: string       // option_id of the dependency
  effect: 'enable' | 'disable' | 'recommend'
  affected_options: string[]
}
