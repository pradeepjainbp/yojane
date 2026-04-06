-- ============================================================
-- Yojane — Database Schema
-- Run this in Supabase SQL Editor (supabase.com → SQL Editor)
-- ============================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================
-- BUILDS — Core entity: one build per construction project
-- ============================================================
CREATE TABLE IF NOT EXISTS builds (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id         UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name            TEXT NOT NULL DEFAULT 'My Build',
  building_type   TEXT NOT NULL DEFAULT 'residential',      -- residential | apartment | commercial | agricultural | utility
  sub_type        TEXT,                                      -- e.g. warehouse, office, car_shed
  persona         TEXT,                                      -- young_it_couple | joint_family | retired_couple | budget_first_timer | investor
  status          TEXT NOT NULL DEFAULT 'draft',            -- draft | complete
  is_copy_of      UUID REFERENCES builds(id),
  plot_config     JSONB NOT NULL DEFAULT '{}',              -- all onboarding params (lat, lng, climate_zone, seismic_zone, etc.)
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================
-- DECISIONS — One row per decision per build
-- ============================================================
CREATE TABLE IF NOT EXISTS decisions (
  id                UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  build_id          UUID NOT NULL REFERENCES builds(id) ON DELETE CASCADE,
  decision_id       TEXT NOT NULL,          -- e.g. "A1", "B2", "C3"
  stage             TEXT NOT NULL,          -- A | B | C | D | E | F
  chosen_option_id  TEXT NOT NULL,          -- references materials registry id
  cost_override     NUMERIC,               -- user-specified actual contractor quote
  notes             TEXT,
  updated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(build_id, decision_id)
);

-- ============================================================
-- BUILD_SCORES — Cached scores, recalculated on decision change
-- ============================================================
CREATE TABLE IF NOT EXISTS build_scores (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  build_id        UUID NOT NULL REFERENCES builds(id) ON DELETE CASCADE UNIQUE,
  comfort         NUMERIC DEFAULT 0,       -- 0-100
  durability      NUMERIC DEFAULT 0,       -- 0-100
  tco             NUMERIC DEFAULT 0,       -- INR total over 20 years
  resilience      NUMERIC DEFAULT 0,       -- 0-100
  carbon          NUMERIC DEFAULT 0,       -- kgCO2/sqft
  score_breakdown JSONB DEFAULT '{}',      -- full sub-component breakdown
  calculated_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================
-- SHARED_LINKS — For read-only / forkable build sharing
-- ============================================================
CREATE TABLE IF NOT EXISTS shared_links (
  id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  build_id    UUID NOT NULL REFERENCES builds(id) ON DELETE CASCADE,
  token       TEXT NOT NULL UNIQUE DEFAULT encode(gen_random_bytes(16), 'hex'),
  permissions TEXT NOT NULL DEFAULT 'view',  -- view | fork
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  expires_at  TIMESTAMPTZ
);

-- ============================================================
-- Row Level Security (RLS)
-- ============================================================
ALTER TABLE builds ENABLE ROW LEVEL SECURITY;
ALTER TABLE decisions ENABLE ROW LEVEL SECURITY;
ALTER TABLE build_scores ENABLE ROW LEVEL SECURITY;
ALTER TABLE shared_links ENABLE ROW LEVEL SECURITY;

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
-- Updated_at trigger
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
