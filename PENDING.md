# Yojane — Project Status & Pending Work
> Last updated: 2026-04-10
> Git: `pradeepjainbp/yojane` · Branch: `master` · Latest commit: `2b10cf7`
> Live: `https://yojane.pradeepjainbp.in` · Stack: Next.js 15 App Router · Supabase · Tailwind · TypeScript

---

## ✅ What Has Been Built (fully working)

### App Shell
- Google OAuth login (`/login`) — `src/app/login/page.tsx`
- Auth callback + session handling — `src/app/auth/callback/route.ts` + `src/middleware.ts`
- Root page (`/`) redirects: authenticated → `/dashboard`, unauthenticated → `/login`
- Dashboard (`/dashboard`) — shows all builds, delete with confirmation
- Onboarding flow (`/dashboard/new`) — building type → Google Maps pin drop → plot dimensions → climate/seismic params → persona → budget
- Build simulator (`/build/[id]`) — 6-stage construction decision engine (A–F)
- Build report (`/build/[id]/report`) — scores, cost breakdown, decision log, maintenance calendar, PDF export

### Data Layer
- **Supabase schema** (`supabase/schema.sql`) — tables: `components`, `builds`, `decisions`, `build_scores`, `shared_links` with RLS
- **`components` table** — 214 rows, 49 subcategories. All validated. Source: Karnataka PWD SOR 2024-25, CPWD DSR 2023, IS codes
- **`builds` / `decisions` / `build_scores`** — live in Supabase, saving correctly

### Simulator Engine
- `src/data/decision-points.ts` — 45 decision points across 6 stages (A–F). All 45 use spectrum sliders backed by live registry data (zero list-pickers)
- `src/engine/scoring.ts` — computes comfort, durability, TCO, resilience, carbon
- `src/engine/auto-decide.ts` — scores every component on durability (35%) · climate fit (30%) · value (20%) · carbon (15%); filters by budget tier via `spectrum_position`
- `src/components/simulator/DecisionCard.tsx` — spectrum slider with registry data for all decisions
- `src/components/simulator/AutoDecidePanel.tsx` — "Let AI Decide" modal

### Scoring Engine — How Each Score Works

| Score | Key inputs | Notes |
|---|---|---|
| **Comfort** (0-100) | Wall thermal (B2), roof thermal (C2), insulation (C3), orientation, wall config (B3), plot area | Weighted: thermal 35%, light 20%, ventilation 20%, acoustic 15%, spatial 10% |
| **Durability** (0-100) | Foundation (A1) 25%, structure (B1) 20%, walls (B2) 20%, roof (C2) 15%, waterproofing (C4) 10%, flooring (D1) 5%, plumbing (E1) 5% | Uses `durability_score` from registry · coastal climate penalty 8% |
| **Resilience** (0-100) | Seismic: B1 structural system · Monsoon: A7 plinth + A5 DPC · Termite: A6 soil treatment · Wind: C2 roof moisture resistance | Weights scale with seismic zone and rainfall_mm |
| **TCO** (₹/sqft) | Sum of chosen component costs × area coverage fractions + 20yr maintenance PV + 20yr energy PV at 7% discount | Area fractions applied: D7/D8 doors (0.03/0.05), D9 windows (0.10), C4 waterproofing (0.30), D5 countertop (0.04), D6 bathrooms (0.06) |
| **Carbon** (kgCO₂/sqft) | Base embodied (95 kgCO₂/sqft) adjusted by `energy_impact_modifier` + 20yr operational at 0.7 kgCO₂/kWh | |

### Floating Cost Wallet
- Fixed-position widget in `BuildSimulator.tsx` showing running construction estimate in ₹L/Cr
- **Draggable** — mouse and touch, drag handle at top, bounded to viewport
- Updates in real time on every decision change with ±delta flash animation
- Colour-coded: green = under budget, red = over budget, blue = no budget set
- Seeded from existing decisions when component registry loads

### Build Report Sections
| Section | Status | Notes |
|---|---|---|
| Hero summary | ✅ Done | Plot, floors, orientation, climate, decisions count |
| Build Scores | ✅ Done | 5 score cards (Comfort, Durability, Resilience, TCO, Carbon) + budget target |
| A: Project Summary | ✅ Done | Building type, persona, plot details, zones |
| B: Decision Log | ✅ Done | Stage-grouped, shows component name + cost/sqft + durability/lifespan |
| C: Cost Breakdown | ✅ Done | Year-0 estimate, annual maintenance, annual energy, 20yr TCO; budget vs estimate; stage-by-stage table; formula explanation |
| D: Maintenance Guide | ✅ Done | Per-component maintenance cycle and effort |
| Radar chart | ❌ Missing | Score cards exist, no visual radar |
| "Consider Reviewing" | ❌ Missing | Suggestions for choices scoring below threshold |

### Key Files
- `src/types/index.ts` — Component type (49 fields), DecisionPoint, Build, Decision, BuildScores
- `src/data/decision-points.ts` — all 45 decisions with subcategory mappings
- `src/data/registry.csv` — 214-row source of truth (49 subcategories)
- `src/data/image_prompts.md` — Gemini image generation prompts for all 214 components
- `src/engine/scoring.ts` — all score calculations + `calculateTCOBreakdown()` export
- `src/engine/auto-decide.ts` — AI auto-select logic
- `src/middleware.ts` — MUST EXIST for Supabase session; calls updateSession
- `supabase/schema.sql` — full DB schema
- `supabase/fix_sort_order.sql` — ✅ APPLIED 2026-04-10 — fixed sort_order for 14 subcategories

### Known Data Notes
- Registry costs are **₹ per sqft of the element's own area** (not always per sqft of built-up area)
- Items like windows, doors, waterproofing apply to partial areas — scoring engine applies coverage fractions
- The floating wallet uses `computeDirectCost` which applies the same coverage fractions
- `spectrum_position` labels (Basic/Intermediate/Performance/Premium) are quality-based, not purely cost-based
- `sort_order` in Supabase now reflects cheapest → most expensive after `fix_sort_order.sql` was applied

---

## 🔴 Next Up — Highest Priority

### 1. Images for Material Choices
**What:** Decision cards show text + specs only. Users need to see what each material looks like.

**How:**
1. Add `image_url TEXT` column to `components` table in Supabase:
   ```sql
   ALTER TABLE components ADD COLUMN image_url TEXT;
   ```
2. Collect images using Gemini — prompts are in `src/data/image_prompts.md` (one prompt per component, 214 total)
3. Upload to Supabase Storage bucket `component-images`
4. In `DecisionCard.tsx` → `ComponentDetail` component — add `<img src={c.image_url}>` thumbnail
5. In `SpectrumPicker` — show small thumbnail above each slider label

**Files to edit:** `src/components/simulator/DecisionCard.tsx`

---

### 2. Cost Override (Contractor Quote Entry)
**What:** User can enter their actual contractor quote per material and see delta vs PWD benchmark.

**How:**
- `cost_override` field already exists in the `decisions` table
- Add "Enter actual quote ₹__/sqft" input in `DecisionCard.tsx` below the selected component detail
- On save: `supabase.from('decisions').update({ cost_override: value })`
- Show delta: "Your quote: ₹72/sqft · Benchmark: ₹65/sqft · +11% above"
- Use `cost_override` in `scoring.ts → calculateTCOBreakdown()` when present

**Files to edit:** `src/components/simulator/DecisionCard.tsx`, `src/engine/scoring.ts`

---

### 3. Build Sharing (Read-only Link)
**What:** Generate a shareable link. `shared_links` table already exists in DB.

**How:**
- Add "Share Build" button in `BuildSimulator.tsx` header
- On click: `supabase.from('shared_links').insert({ build_id, permissions: 'view' })` → returns token
- Create `/share/[token]/page.tsx` — server component, reads build via token, renders read-only report
- "Fork this build" button on shared view

**Files to create:** `src/app/share/[token]/page.tsx`
**Files to edit:** `src/app/build/[id]/BuildSimulator.tsx`

---

### 4. Copy / Duplicate Build
**What:** "Create a variant" — e.g. "Showing Contractor Raju's quote", "If We Stretch Budget 10%".

**How:**
- Add "Duplicate" button to `src/components/dashboard/BuildCard.tsx`
- On click: copy `builds` row with `is_copy_of = original_id`, copy all `decisions` rows
- Report for copied builds shows "X changes from original build"

**Files to edit:** `src/components/dashboard/BuildCard.tsx`, `src/app/dashboard/page.tsx`

---

## 🟡 Should-Have for v1

### 5. Score Radar Chart in Report
- Add a radar/spider chart to Section D of the report showing all 5 scores visually
- Recommend `recharts` (already likely in project) or pure SVG

### 6. "Consider Reviewing" Section in Report
- When any choice scores below threshold (e.g. durability < 6), show diplomatic suggestion
- Data available via registry `advisory_message` + `advisory_rule` fields
- Add as final section in `src/app/build/[id]/report/page.tsx`

### 7. PDF Quality
- Current PDF uses `html2canvas` — screenshot quality
- Switch to `@react-pdf/renderer` for clean A4 typeset PDF
- File: `src/components/simulator/DownloadPdfButton.tsx`

### 8. Google Maps Pin Drop (Onboarding)
- Already partially built (`src/components/onboarding/PlotMapPicker.tsx`)
- `NEXT_PUBLIC_GOOGLE_MAPS_KEY` set in `.env.local`
- Auto-derive from lat/lng: climate zone, seismic zone, rainfall, soil type
- Check `src/app/dashboard/new/page.tsx` for the step needing the real map

### 9. Architect Insights Panel
- Sun path analysis for chosen road-facing direction
- Ventilation quality rating based on wall config + orientation
- Vastu conflict alerts when `vastu_enabled = true` and a choice conflicts with thermal/acoustic optimum

---

## 🟢 v2 / Nice-to-Have

10. **Isometric Building Visualiser** — PixiJS, material textures, stage-by-stage animation
11. **20-Year Fast-Forward Animation** — maintenance events, material degradation, cost accumulation
12. **Achievement Badges** — Monsoon-Proof, Carbon Champion, The Accountant, Vastu Compliant
13. **"What Yojane Users Chose" Benchmarks** — distribution of choices per climate zone
14. **Myth Buster Feature** — `common_misconception` + `myth_buster_fact` fields in registry schema, needs UI in DecisionCard
15. **BOQ Generation** — contractor-ready document with quantities, specs, costs
16. **Demo Mode** — unauthenticated `/demo` route with pre-configured sample plot
17. **Additional Building Types** — apartment, commercial, agricultural decision trees
18. **Integration with pradeepjainbp.in** — card on main website linking to Yojane

---

## 🏗️ Architecture Decision Record — Multi-Building-Type Engine

> Recorded 2026-04-10. Do not implement without rethinking the full approach.

### Current state (residential-only, partially type-aware)

The engine captures `building_type` in onboarding and passes it through to `calculateAllScores()`.
It is used in **one place only**: `COMFORT_WEIGHTS` in `src/engine/scoring.ts` — weighting thermal/light/ventilation/acoustic/spatial differently for `residential` / `apartment` / `commercial`.

Everything else (Durability, Resilience, TCO, Carbon, all 45 decision points, all AREA_FRACTIONs) is identical regardless of building type. The 45-decision tree and the 214-row registry were designed for a **South India residential house**.

### What actually differs by building type

| Factor | House | Office | Factory / Shed |
|---|---|---|---|
| Internal walls (D2, D3) | Many partitions | Open plan or moderate | Minimal |
| Doors (D7 main, D8 internal) | Flush/panel doors, domestic count | Commercial grade, glazed | Rolling shutters, industrial |
| Windows (D9) | ~10% of wall area | Larger glazing ~15-20% | Skylights, ventilators (not standard windows) |
| Electrical (E2) | Domestic single-phase load | Moderate | Heavy-duty 3-phase, larger conduits, industrial panels |
| Flooring (D1) | Tile / marble | Epoxy or heavy tile | Industrial epoxy or CC — high-load rating |
| Landscape (F stage) | Gardens, gate, compound wall | Parking, signage, ramp | Minimal — may not apply |
| Comfort scoring axes | Thermal, acoustic, spatial all relevant | Acoustic + light more important | Thermal comfort not primary; ventilation/exhaust is |
| Area fraction for D9 windows | 0.10 of built-up area | 0.15-0.20 | 0.05 or skylight fraction |
| Electrical load multiplier | 1.0× | 1.3× | 2.0-2.5× |

### Why the current approach falls short for non-residential

1. **Wrong decision options** — rolling shutters, industrial epoxy floors, ventilator louvers do not exist in the registry. Users would be forced to pick domestic options that don't apply.
2. **Wrong AREA_FRACTIONs** — window cost fraction of 0.10 makes sense for a house; for a factory it overestimates glazing, underestimates industrial doors.
3. **Wrong comfort axes** — showing an acoustic-comfort score to a factory owner is irrelevant; showing exhaust/ventilation capacity isn't modelled at all.
4. **Wrong decision count** — a shed may need only 20-25 decisions, not 45. Showing all 45 creates confusion.

### Two viable implementation approaches

**Option A — AREA_FRACTION + weight overrides per building type (lighter lift)**
- Keep the same 45 decision points and registry
- Add `AREA_FRACTION_BY_TYPE` and `COMFORT_WEIGHTS` already differentiated
- Add type-specific electrical multipliers in TCO
- Suitable if the building types are similar enough (residential ↔ apartment ↔ small commercial)
- Files: `src/engine/scoring.ts`, `computeDirectCost()` in `BuildSimulator.tsx`

**Option B — Decision tree branching by building type (correct long-term approach)**
- Tag each DecisionPoint in `src/data/decision-points.ts` with `applicableTypes: string[]`
- Add factory/commercial-specific components to the registry (rolling shutters, industrial flooring, etc.)
- Swap in type-specific options in `DecisionCard.tsx` based on `buildingType`
- Show only the N decisions relevant to that building type
- Requires registry expansion (~30-50 new rows) + decision-point tagging + onboarding changes
- This is the right approach before opening to commercial/industrial use

### Recommendation before implementing

Before writing any code, decide:
1. Which building types will be supported in v1 (residential only? +apartment? +small office?)
2. Whether the 214-row registry needs new components for each type, or if mapping existing ones to new uses is good enough
3. Whether decision count should vary by type (45 for house, 30 for apartment, 25 for shed) — this affects the wallet's `X/45` counter and the report completeness signal

**Do not add building-type branching as a small incremental change.** It touches the registry, decision-points data, scoring engine, wallet display, and report — do it as a deliberate milestone.

---

## 📊 Summary

| Category | Items | Status |
|---|---|---|
| Core app fully working | Auth, dashboard, onboarding, simulator, report | ✅ |
| Registry | 214 rows, 49 subcategories, all 45 decisions spectrum | ✅ |
| Scoring engine | Comfort, Durability, Resilience, TCO, Carbon | ✅ (bugs fixed 2026-04-10) |
| Floating wallet | Draggable, real-time estimate, delta flash | ✅ |
| Cost breakdown in report | Year-0, maintenance, energy, TCO, stage breakdown | ✅ |
| Next up (highest ROI) | Images, cost override, sharing, duplicate | 🔴 4 items |
| Should-have v1 | Radar chart, PDF, maps, architect panel | 🟡 4 items |
| v2 backlog | Visualiser, badges, demo, BOQ | 🟢 9 items |

### Suggested build order for next session
1. Images for material choices (visual impact — prompts already ready in `image_prompts.md`)
2. Cost override UI (contractor workflow — DB field already exists)
3. Build sharing (read-only link — DB table already exists)
4. Copy/duplicate build
