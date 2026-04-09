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
// Component — single row from the Supabase `components` table
// (maps 1:1 to registry.csv columns)
// ============================================================
export interface Component {
  // Identity & Display
  component_id: string               // e.g. 'WS-001'
  category_name: string              // e.g. 'Envelope'
  subcategory_name: string           // e.g. 'Wall System'
  name: string                       // machine key e.g. 'aac_block'
  display_name: string               // e.g. 'AAC Block (Autoclaved Aerated Concrete)'
  description: string | null
  region: string
  climate_zone: string | null        // semicolon-separated e.g. 'Warm-Humid;Hot-Dry'
  spectrum_position: string | null   // Basic | Intermediate | Performance | Premium | Ultra-Premium
  sort_order: number

  // Cost — Capex (₹ per sqft of relevant area)
  base_cost_per_sqft_inr: number | null
  installation_cost_per_sqft_inr: number | null
  cost_confidence: string | null
  cost_last_updated: string | null         // TEXT in DB — may be '2023-04' or '2024-Q1'
  cost_source_notes: string | null

  // Lifecycle
  expected_lifespan_years: number | null
  replacement_cost_factor: number | null
  major_maintenance_cycle_years: number | null
  major_maintenance_cost_factor: number | null
  annual_minor_maint_factor: number | null
  maintenance_complexity: string | null  // Low | Medium | High
  lifecycle_source_notes: string | null

  // Performance Scores (0–10)
  thermal_resistance_score: number | null  // NUMERIC (0–10, may be decimal e.g. 7.5)
  acoustic_score: number | null            // NUMERIC (0–10, may be decimal)
  durability_score: number | null          // NUMERIC (0–10, may be decimal)
  moisture_resistance: string | null       // Low | Medium | High
  fire_rating: string | null
  energy_impact_modifier: number | null    // -1.0 to +1.0
  accessibility_score: string | null       // High | Medium | Low (TEXT in DB)
  thermal_source_notes: string | null

  // Rule Engine
  max_floors_supported: number | null
  min_floors_required: number | null
  max_span_supported_m: string | null      // TEXT in DB — may be 'N/A'
  incompatible_with: string | null
  compatible_with: string | null
  requires_component: string | null
  climate_restrictions: string | null
  hard_block_rule: string | null
  advisory_rule: string | null
  advisory_message: string | null
  advisory_severity: string | null
  constraint_source_notes: string | null

  // AI Advisory
  ai_advisory_notes: string | null
  pros: string | null                    // semicolon-separated
  cons: string | null                    // semicolon-separated
  tooltip_detail: string | null

  // Audit
  status: string
  verify_flags: string | null
  data_filled_by: string | null
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
  options: string[]       // fallback option IDs when no registry subcategory mapped
  subcategory?: string    // registry subcategory_name — if set, options come from Supabase
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
