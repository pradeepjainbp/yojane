-- ============================================================
-- Yojane — Database Schema v2
-- Run this in Supabase SQL Editor (supabase.com → SQL Editor)
-- ============================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================
-- COMPONENTS — Materials registry (single source of truth)
-- Populated from registry.csv import
-- Each row = one buildable option in one subcategory
-- ============================================================
-- HOW EACH COLUMN FEEDS THE APP:
--   thermal_resistance_score + acoustic_score → build_scores.comfort
--   durability_score                          → build_scores.durability
--   base_cost + installation_cost + lifecycle → build_scores.tco
--   moisture_resistance + fire_rating         → build_scores.resilience
--   energy_impact_modifier                    → build_scores.carbon_efficiency
--   climate_zone + climate_restrictions       → build_scores.climate_fit
--   hard_block_rule                           → rule engine (blocks incompatible combos)
--   ai_advisory_notes + pros + cons           → "Let AI Decide" explanation panel
--   spectrum_position + sort_order            → snap slider stop position & order
--   tooltip_detail                            → hover tooltip text on slider
-- ============================================================
CREATE TABLE IF NOT EXISTS components (

  -- ── Identity & Display ──────────────────────────────────
  component_id              TEXT PRIMARY KEY,              -- e.g. ENV-ROOF-001
  category_name             TEXT NOT NULL,                 -- Envelope | Structure | Foundation | Finishes | Systems | Sustainability | Special Modes
  subcategory_name          TEXT NOT NULL,                 -- e.g. Roofing Material
  name                      TEXT NOT NULL,                 -- machine key e.g. gi_sheet
  display_name              TEXT NOT NULL,                 -- e.g. Galvanized Iron (GI) Sheet
  description               TEXT,
  region                    TEXT NOT NULL DEFAULT 'South India',
  climate_zone              TEXT,                          -- semicolon-separated e.g. 'Warm-Humid;Hot-Dry;Temperate'
  spectrum_position         TEXT,                          -- Basic | Intermediate | Performance | Premium | Ultra-Premium
  sort_order                INTEGER NOT NULL DEFAULT 1,

  -- ── Cost — Capex (₹ per sqft of relevant area) ──────────
  -- Note: "sqft" means different things per subcategory:
  --   Flooring/Roofing/Wall  → sqft of floor/roof/wall area
  --   HVAC                   → sqft of conditioned area
  --   Doors/Windows          → sqft of door/window leaf area
  base_cost_per_sqft_inr          NUMERIC,                -- material cost only
  installation_cost_per_sqft_inr  NUMERIC,                -- labour cost only
  cost_confidence                 TEXT,                   -- High | Medium | Low
  cost_last_updated               DATE,
  cost_source_notes               TEXT,                   -- e.g. "CPWD DSR 2023 Item 12.50"

  -- ── Lifecycle — 20-year cost model ──────────────────────
  -- TCO formula per component:
  --   year0 = (base_cost + installation_cost) × sqft_area
  --   annual_maint = base_cost × sqft × annual_minor_maint_factor  [each year]
  --   major_maint  = base_cost × sqft × major_maintenance_cost_factor
  --                  [every major_maintenance_cycle_years]
  --   replacement  = base_cost × sqft × replacement_cost_factor
  --                  [if expected_lifespan_years < 20]
  --   tco_20yr = year0 + Σ(annual_maint) + Σ(major_maint) + replacement
  expected_lifespan_years         INTEGER,
  replacement_cost_factor         NUMERIC,                -- e.g. 1.2 = 120% of base to replace
  major_maintenance_cycle_years   INTEGER,
  major_maintenance_cost_factor   NUMERIC,                -- fraction of base cost when due
  annual_minor_maint_factor       NUMERIC,                -- fraction of base cost per year
  maintenance_complexity          TEXT,                   -- Low | Medium | High
  lifecycle_source_notes          TEXT,

  -- ── Performance Scores (0–10 scale) ─────────────────────
  -- build_scores.comfort = avg(thermal×0.5 + acoustic×0.5) × 10  across chosen components
  -- build_scores.durability = weighted avg(durability_score) × 10 across structural/envelope components
  thermal_resistance_score        INTEGER,                -- 0–10 (10 = best insulator)
  acoustic_score                  INTEGER,                -- 0–10 (10 = quietest)
  durability_score                INTEGER,                -- 0–10 (10 = most durable)
  moisture_resistance             TEXT,                   -- Low | Medium | High
  fire_rating                     TEXT,                   -- Class A (best) | Class B | Class C
  -- energy_impact_modifier: relative energy penalty/benefit of this component
  --   -1.0 = major energy penalty (e.g. bare GI roof in summer)
  --    0.0 = neutral
  --   +1.0 = major energy saving (e.g. cool roof with good SRI)
  -- build_scores.carbon_efficiency = avg(50 + energy_impact_modifier × 50) across components → 0–100
  energy_impact_modifier          NUMERIC,                -- -1.0 to +1.0
  accessibility_score             INTEGER,                -- 0–10 (10 = most accessible)
  thermal_source_notes            TEXT,

  -- ── Rule Engine — Constraint Fields ─────────────────────
  max_floors_supported            INTEGER,                -- NULL = no limit
  min_floors_required             INTEGER,                -- NULL = no minimum
  max_span_supported_m            NUMERIC,
  incompatible_with               TEXT,                   -- semicolon-separated component names/IDs
  compatible_with                 TEXT,                   -- semicolon-separated preferred pairings
  requires_component              TEXT,                   -- must-have companion component
  climate_restrictions            TEXT,                   -- human-readable constraint text
  hard_block_rule                 TEXT,                   -- machine-readable e.g. "None" | rule text
  advisory_rule                   TEXT,                   -- condition for showing advisory_message
  advisory_message                TEXT,                   -- text shown to user when rule fires
  advisory_severity               TEXT,                   -- None | Warning | Critical
  constraint_source_notes         TEXT,

  -- ── AI Advisory ─────────────────────────────────────────
  -- Used by "Let AI Decide" explanation panel
  -- AI scores each option in a subcategory on 4 weights:
  --   Durability 35%  → durability_score
  --   Climate Fit 30% → climate_zone match + energy_impact_modifier
  --   Value 20%       → inverse of tco (lower tco = higher value score)
  --   Carbon 15%      → energy_impact_modifier (positive = lower carbon)
  -- ai_advisory_notes = the domain-expert explanation the AI shows when it picks this option
  ai_advisory_notes               TEXT,
  pros                            TEXT,                   -- semicolon-separated benefit points
  cons                            TEXT,                   -- semicolon-separated drawback points
  tooltip_detail                  TEXT,                   -- 1-2 sentence hover tooltip on slider

  -- ── Audit & Metadata ────────────────────────────────────
  status                          TEXT NOT NULL DEFAULT 'Active',  -- Active | Draft | Deprecated
  verify_flags                    TEXT,                   -- comma-separated field names needing cost verification
  data_filled_by                  TEXT                    -- Domain Expert | AI | Manual
);

-- Indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_components_subcategory ON components(subcategory_name);
CREATE INDEX IF NOT EXISTS idx_components_category   ON components(category_name);
CREATE INDEX IF NOT EXISTS idx_components_status     ON components(status);


-- ============================================================
-- BUILDS — Core entity: one build per construction project
-- ============================================================
CREATE TABLE IF NOT EXISTS builds (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id         UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name            TEXT NOT NULL DEFAULT 'My Build',
  building_type   TEXT NOT NULL DEFAULT 'residential',   -- residential | apartment | commercial | agricultural | utility
  sub_type        TEXT,                                   -- e.g. warehouse, office, car_shed
  persona         TEXT,                                   -- young_it_couple | joint_family | retired_couple | budget_first_timer | investor
  status          TEXT NOT NULL DEFAULT 'draft',         -- draft | complete
  is_copy_of      UUID REFERENCES builds(id),
  -- plot_config stores all onboarding params including sqft_area (needed for TCO calc):
  -- { lat, lng, climate_zone, seismic_zone, sqft_area, floors, plot_area_sqyd, ... }
  plot_config     JSONB NOT NULL DEFAULT '{}',
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- ============================================================
-- DECISIONS — One row per decision per build
-- NOTE: chosen_option_id has NO foreign key to components.
--   Registry-backed decisions store a component_id (e.g. WS-001).
--   List-picker decisions store a plain string (e.g. EXC-900, MORTAR-CM16).
--   Both are valid; a FK would reject the list-picker values.
-- ============================================================
CREATE TABLE IF NOT EXISTS decisions (
  id                UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  build_id          UUID NOT NULL REFERENCES builds(id) ON DELETE CASCADE,
  decision_id       TEXT NOT NULL,                        -- e.g. "A1", "B2", "C3"
  stage             TEXT NOT NULL,                        -- A | B | C | D | E | F
  chosen_option_id  TEXT NOT NULL,                        -- component_id OR plain option string
  cost_override     NUMERIC,                              -- user-specified actual contractor quote (₹/sqft)
  notes             TEXT,
  updated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(build_id, decision_id)
);


-- ============================================================
-- BUILD_SCORES — Cached scores, recalculated on any decision change
-- ============================================================
-- HOW EACH SCORE IS COMPUTED (run server-side when decisions change):
--
-- comfort (0–100):
--   avg over chosen components of (thermal_resistance_score × 5 + acoustic_score × 5)
--   Components with null scores are excluded from the average.
--
-- durability (0–100):
--   weighted average of durability_score × 10 across chosen components.
--   Envelope + Structure components carry double weight (they define building lifespan).
--
-- climate_fit (0–100):
--   For each chosen component, check if build's climate_zone is in component.climate_zone list.
--   Match = 10, Partial = 6, No match = 0. Also subtract 20 if advisory_severity = 'Critical'.
--   Normalize to 0–100 across all chosen components.
--
-- tco (INR — total over 20 years):
--   Sum across all chosen components:
--     year0     = (base_cost + installation_cost) × relevant_area_sqft
--     annual    = base_cost × relevant_area × annual_minor_maint_factor × 20
--     major     = base_cost × relevant_area × major_maintenance_cost_factor
--                 × floor(20 / major_maintenance_cycle_years)
--     replace   = if expected_lifespan_years < 20:
--                   base_cost × relevant_area × replacement_cost_factor
--   relevant_area_sqft comes from plot_config (sqft_area for most; door/window count × size for Doors/Windows)
--   If user provided cost_override, use that instead of base_cost + installation_cost for year0.
--
-- resilience (0–100):
--   Per chosen component: moisture_score + fire_score mapped as:
--     moisture_resistance: High→10, Medium→6, Low→2
--     fire_rating: Class A→10, Class B→7, Class C→3
--   avg((moisture_score + fire_score) / 2 × 10) across components
--
-- carbon_efficiency (0–100) — higher = lower carbon impact:
--   Per component: 50 + (energy_impact_modifier × 50) → 0–100
--   avg across all chosen components.
--   Note: This is a relative index, not absolute kgCO₂/sqft.
--   To get absolute carbon later, add embodied_carbon_kgco2_per_sqft column to components.
-- ============================================================
CREATE TABLE IF NOT EXISTS build_scores (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  build_id        UUID NOT NULL REFERENCES builds(id) ON DELETE CASCADE UNIQUE,
  comfort         NUMERIC DEFAULT 0,    -- 0–100 (thermal + acoustic)
  durability      NUMERIC DEFAULT 0,    -- 0–100 (structural longevity)
  tco             NUMERIC DEFAULT 0,    -- ₹/sqft over 20 years
  resilience      NUMERIC DEFAULT 0,    -- 0–100 (moisture + fire + seismic)
  carbon          NUMERIC DEFAULT 0,    -- kgCO₂/sqft (embodied + 20yr operational)
  score_breakdown JSONB DEFAULT '{}',   -- full per-component breakdown for debug/report
  calculated_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- ============================================================
-- SHARED_LINKS — For read-only / forkable build sharing
-- ============================================================
CREATE TABLE IF NOT EXISTS shared_links (
  id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  build_id    UUID NOT NULL REFERENCES builds(id) ON DELETE CASCADE,
  token       TEXT NOT NULL UNIQUE DEFAULT encode(gen_random_bytes(16), 'hex'),
  permissions TEXT NOT NULL DEFAULT 'view',               -- view | fork
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  expires_at  TIMESTAMPTZ
);


-- ============================================================
-- Row Level Security (RLS)
-- ============================================================
ALTER TABLE components    ENABLE ROW LEVEL SECURITY;
ALTER TABLE builds        ENABLE ROW LEVEL SECURITY;
ALTER TABLE decisions     ENABLE ROW LEVEL SECURITY;
ALTER TABLE build_scores  ENABLE ROW LEVEL SECURITY;
ALTER TABLE shared_links  ENABLE ROW LEVEL SECURITY;

-- Components: public read (reference data), no user writes
CREATE POLICY "Anyone can read active components"
  ON components FOR SELECT
  USING (status = 'Active');

-- Builds: users own their own builds
CREATE POLICY "Users can manage own builds"
  ON builds FOR ALL
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- Decisions: users can manage decisions on their own builds
CREATE POLICY "Users can manage own decisions"
  ON decisions FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM builds WHERE builds.id = decisions.build_id AND builds.user_id = auth.uid()
    )
  );

-- Build scores: same pattern
CREATE POLICY "Users can manage own scores"
  ON build_scores FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM builds WHERE builds.id = build_scores.build_id AND builds.user_id = auth.uid()
    )
  );

-- Shared links: owner can manage; anyone with token can read
CREATE POLICY "Owners can manage shared links"
  ON shared_links FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM builds WHERE builds.id = shared_links.build_id AND builds.user_id = auth.uid()
    )
  );

CREATE POLICY "Anyone can view shared links by token"
  ON shared_links FOR SELECT
  USING (true);


-- ============================================================
-- Triggers — auto-update updated_at
-- ============================================================
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER builds_updated_at
  BEFORE UPDATE ON builds
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER decisions_updated_at
  BEFORE UPDATE ON decisions
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();
