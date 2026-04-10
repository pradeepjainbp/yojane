# Yojane — Project Status & Pending Work
> Last updated: 2026-04-10
> Git: `pradeepjainbp/yojane` · Branch: `master` · Latest commit: `9b3bb0c`
> Live: `https://yojane.pradeepjainbp.in` · Stack: Next.js 16.2.2 (Turbopack) · Supabase · Tailwind

---

## ✅ What Has Been Built (fully working)

### App Shell
- Google OAuth login (`/login`) — `src/app/login/page.tsx`
- Auth callback + session handling — `src/app/auth/callback/route.ts` + `src/middleware.ts`
- Root page (`/`) redirects: authenticated → `/dashboard`, unauthenticated → `/login`
- Dashboard (`/dashboard`) — shows all builds for the logged-in user
- Onboarding flow (`/dashboard/new`) — multi-step: building type → plot location (Google Maps pin drop) → plot dimensions → climate/seismic params → persona → budget
- Build simulator (`/build/[id]`) — 6-stage construction decision engine (A–F)
- Build report (`/build/[id]/report`) — scores, decision log, maintenance calendar, PDF export
- Sign-out route

### Data Layer
- **Supabase schema** (`supabase/schema.sql`) — tables: `components`, `builds`, `decisions`, `build_scores`, `shared_links` with RLS policies
- **`components` table** — 134 rows, 27 subcategories, imported from `registry.csv`. All validated. Zero VERIFY flags. Source: Karnataka PWD SOR 2024-25, CPWD DSR 2023, IS codes.
- **`builds` / `decisions` / `build_scores`** — live in Supabase, saving correctly

### Simulator Engine
- `src/data/decision-points.ts` — 37 decision points across 6 stages (A–F). 20 have `subcategory` field linking to registry; 17 are list-pickers (parameter choices like mortar type, plinth height).
- `src/engine/scoring.ts` — computes comfort, durability, TCO, resilience, carbon from `Component` registry fields
- `src/engine/auto-decide.ts` — scores every component on durability (35%) · climate fit (30%) · value (20%) · carbon (15%); filters by budget tier via `spectrum_position`
- `src/components/simulator/DecisionCard.tsx` — spectrum slider with registry data for mapped decisions; list-picker fallback for unmapped ones
- `src/components/simulator/AutoDecidePanel.tsx` — "Let AI Decide" modal

### Key Types (`src/types/index.ts`)
- `Component` — 49-field type matching registry.csv / Supabase `components` table
- `DecisionPoint` — includes `subcategory?: string` linking to registry
- `Build`, `Decision`, `BuildScores`, `PlotConfig` — all stable

### How the Data Flow Works
```
Supabase components table (134 rows)
        ↓ fetched once on BuildSimulator mount
componentsBySubcategory: Record<string, Component[]>
        ↓ passed as prop
DecisionCard — if dp.subcategory set → SpectrumPicker using Component[]
             — if no subcategory    → ListPicker using dp.options string[]
        ↓ on selection
chosen_option_id = component_id (e.g. "WS-003") OR plain string (e.g. "MORTAR-CM16")
        ↓ saved to decisions table
scoring.ts receives chosenComponents: Component[] → computes scores from registry fields
```

### Decision Point → Registry Subcategory Mapping
| Decision | Label | Subcategory | Mode |
|---|---|---|---|
| A1 | Foundation Type | `Foundation Type` | Spectrum |
| A2 | Excavation Depth | — | List |
| A3 | Concrete Mix Grade | — | List |
| A4 | Steel Reinforcement Grade | — | List |
| A5 | DPC | — | List |
| A6 | Termite & Soil Treatment | `Soil Treatment` | Spectrum |
| A7 | Plinth Height | — | List |
| A8 | Plinth Filling Material | — | List |
| A9 | Underground Water Tank | — | List |
| B1 | Structural System | `Structural System` | Spectrum |
| B2 | Wall Material | `Wall System` | Spectrum |
| B3 | Wall Configuration | — | List |
| B4 | Mortar Type | — | List |
| B5 | Lintel & Sunshade | — | List |
| B6 | External Wall Finish | `Wall Finish` | Spectrum |
| C1 | Roof Structure | `Roof Type` | Spectrum |
| C2 | Roof Covering / Material | `Roofing Material` | Spectrum |
| C3 | Roof Insulation / Treatment | `Insulation` | Spectrum |
| C4 | Waterproofing System | `Waterproofing` | Spectrum |
| C5 | Parapet / Edge Detail | — | List |
| C6 | Rainwater Harvesting | `Rainwater Harvesting` | Spectrum |
| D1 | Flooring — Living Areas | `Flooring` | Spectrum |
| D2 | Flooring — Wet Areas | `Flooring` | Spectrum |
| D3 | Flooring — External | `Flooring` | Spectrum |
| D4 | Internal Wall Finish | `Wall Finish` | Spectrum |
| D5 | Kitchen Countertop | — | List |
| D6 | Bathroom Fixtures Grade | — | List |
| D7 | Main Entry Door | `Doors` | Spectrum |
| D8 | Internal Doors | `Doors` | Spectrum |
| D9 | Windows | `Windows` | Spectrum |
| E1 | Water Supply Piping | `Plumbing` | Spectrum |
| E2 | Drainage / Sewage Piping | `Plumbing` | Spectrum |
| E3 | Electrical Wiring | `Electrical` | Spectrum |
| E4 | Electrical Load Planning | — | List |
| E5 | Electrical Points Density | — | List |
| E6 | Solar Provision | `Solar` | Spectrum |
| E7 | Water Heating System | — | List |
| E8 | Rainwater Plumbing | — | List |
| E9 | Sewage Treatment | `Waste Management` | Spectrum |
| E10 | Inverter / UPS Wiring | — | List |
| F1–F4 | Compound Wall / Gate / Driveway / Garden | — | List |
| F5 | External Lighting | `Lighting Strategy` | Spectrum |

**Registry subcategories not yet assigned to any decision point** (add as new decisions later):
HVAC, Glazing, Ceiling, Column Grid, Floor System, Green Rating Target, Senior-Friendly, High-Seismic, Flood-Prone

---

## 🔴 Next Up — Highest Priority

### 0. Expand Registry to Cover All Decision Points
**Full spec:** See `TASK-registry-expansion.md` in project root.

**What:** 22 decisions still use hardcoded list-picker options (e.g. Excavation Depth, Mortar Type, Countertop). They should be migrated to the registry so they render as spectrum sliders like all other decisions.

**Three steps:**
1. Add ~90 new rows to `src/data/registry.csv` (22 new subcategories, 3–5 options each)
2. Update `src/data/decision-points.ts` — change those 22 from `options: [...]` to `subcategory: '...'` + `options: []`
3. Re-import CSV to Supabase `components` table

**Also:** 9 registry subcategories exist with no decision point (HVAC, Glazing, Ceiling, Column Grid, Floor System, Green Rating, Senior-Friendly, High-Seismic, Flood-Prone). Add decision points for these.

**Future:** Add `audience: 'homeowner' | 'engineer' | 'both'` field to `DecisionPoint` type and a toggle in the simulator UI. See spec for full classification list.

---

### 1. Images for Material Choices
**What:** Decision cards show text + specs only. Users need to see what each material looks like.

**How:**
1. Add `image_url TEXT` column to `components` table in Supabase:
   ```sql
   ALTER TABLE components ADD COLUMN image_url TEXT;
   ```
2. Upload ~1 photo per component to Supabase Storage bucket `component-images`
3. In `DecisionCard.tsx` → `ComponentDetail` component — add `<img src={c.image_url}>` thumbnail
4. In `SpectrumPicker` — show small thumbnail above each slider label

**Files to edit:** `src/components/simulator/DecisionCard.tsx`

---

### 2. Build Report — Cost Breakdown Section
**What:** Section C of the report is missing a proper cost table. The registry data is now available to compute it.

**How:** In `src/app/build/[id]/report/page.tsx`:
- For each decision with a Component, calculate: `(base_cost_per_sqft_inr + installation_cost_per_sqft_inr) × relevant_area_sqft`
- Relevant area: use `build.plot_config.plot_area_sqft × floors` for most; adjust for walls/roof
- Show stage-wise table: Stage A total | B total | C total … | Grand total
- Show material cost vs labour cost split
- Compare to `target_budget_inr`

**Files to edit:** `src/app/build/[id]/report/page.tsx`

---

### 3. Cost Override (Contractor Quote Entry)
**What:** User can enter their actual contractor quote per material and see delta vs PWD benchmark.

**How:**
- `cost_override` field already exists in the `decisions` table
- Add "Enter actual quote ₹__/sqft" input in `DecisionCard.tsx` below the selected component detail
- On save: `supabase.from('decisions').update({ cost_override: value })`
- Show delta: "Your quote: ₹72/sqft · Benchmark: ₹65/sqft · +11% above"
- Use `cost_override` in `scoring.ts → calculateTCO()` when present (already has the parameter, just not wired to UI)

**Files to edit:** `src/components/simulator/DecisionCard.tsx`, `src/engine/scoring.ts`

---

### 4. Build Sharing (Read-only Link)
**What:** Generate a shareable link for any build. `shared_links` table already exists in DB.

**How:**
- Add "Share Build" button in `BuildSimulator.tsx` header
- On click: `supabase.from('shared_links').insert({ build_id, permissions: 'view' })` → returns token
- Create `/share/[token]/page.tsx` — server component, reads build via token, renders read-only report view
- "Fork this build" button on shared view: copies to viewer's account

**Files to create:** `src/app/share/[token]/page.tsx`
**Files to edit:** `src/app/build/[id]/BuildSimulator.tsx`

---

### 5. Copy / Duplicate Build
**What:** "Create a variant" — e.g. "Showing Contractor Raju", "If We Stretch Budget 10%".

**How:**
- Add "Duplicate" button to `src/components/dashboard/BuildCard.tsx`
- On click: copy `builds` row with `is_copy_of = original_id`, copy all `decisions` rows with new `build_id`
- Report for copied builds shows "X changes from original build"

**Files to edit:** `src/components/dashboard/BuildCard.tsx`, `src/app/dashboard/page.tsx`

---

### 6. Vercel Deployment → `yojane.pradeepjainbp.in`
**Steps:**
1. Repo already on GitHub: `pradeepjainbp/yojane`
2. Connect to Vercel → import that repo → auto-deploy on push
3. Set env vars in Vercel dashboard:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - `NEXT_PUBLIC_GOOGLE_MAPS_KEY`
   - `NEXT_PUBLIC_APP_URL=https://yojane.pradeepjainbp.in`
4. Add CNAME in Cloudflare: `yojane` → Vercel deployment URL
5. In Google Cloud Console → OAuth → Authorized redirect URIs → add `https://yojane.pradeepjainbp.in/auth/callback`
6. In Supabase Dashboard → Auth → URL Configuration → add `https://yojane.pradeepjainbp.in` to allowed URLs

---

## 🟡 Important / Should-have for v1

### 7. Architect Layer
- "Architect Insights" panel in simulator right sidebar (next to ScorePanel)
- Sun path analysis for chosen road-facing direction
- Ventilation quality rating based on wall config + orientation
- Vastu conflict alerts when `vastu_enabled = true` and a choice conflicts with thermal/acoustic optimum

### 8. Build Report — Missing Sections
| Section | Status | Notes |
|---------|--------|-------|
| A: Project Summary | ✅ Done | |
| B: Decision Log | ✅ Done | Shows display_name, cost/sqft, lifespan |
| C: Cost Breakdown | ❌ Missing | See item 2 above |
| D: Score Summary | ✅ Partial | Cards exist, no radar chart |
| E: Maintenance Calendar | ✅ Partial | Shows major_maintenance_cycle_years per component |
| F: "Consider Reviewing" | ❌ Missing | Diplomatic suggestions when a choice scores below threshold |

### 9. PDF Quality
- Current PDF uses `html2canvas` — it's a screenshot, not typeset
- Switch to `@react-pdf/renderer` for clean A4 white-background PDF
- File: `src/components/simulator/DownloadPdfButton.tsx`

### 10. Google Maps Pin Drop (Onboarding)
- Already partially built (`src/components/onboarding/PlotMapPicker.tsx` exists)
- `NEXT_PUBLIC_GOOGLE_MAPS_KEY` is set in `.env.local`
- Auto-derive from lat/lng: climate zone, seismic zone, rainfall, soil type, elevation
- Check `src/app/dashboard/new/page.tsx` for the onboarding step that needs the real map

---

## 🟢 v2 / Nice-to-have

11. **Isometric Building Visualiser** — PixiJS, material textures, stage-by-stage animation
12. **20-Year Fast-Forward Animation** — maintenance events, material degradation, cost accumulation
13. **Achievement Badges** — Monsoon-Proof, Carbon Champion, The Accountant, Vastu Compliant etc.
14. **"What Yojane Users Chose" Benchmarks** — distribution of choices per climate zone (needs user base)
15. **Myth Buster Feature** — `common_misconception` + `myth_buster_fact` fields already in registry schema, just needs UI treatment in DecisionCard
16. **BOQ Generation** — contractor-ready document with quantities, specs, costs
17. **Demo Mode** — unauthenticated `/demo` route with pre-configured sample plot
18. **Additional Building Types** — apartment, commercial, agricultural decision trees (currently only residential has full depth)
19. **Integration with pradeepjainbp.in** — card on main website linking to Yojane

---

## 📊 Summary

| Category | Count | Status |
|---|---|---|
| Fully working | Core app + registry + scoring | ✅ |
| Next up (highest ROI) | Images, cost breakdown, sharing, deployment | 🔴 6 items |
| Should-have v1 | Architect layer, PDF, report sections | 🟡 4 items |
| v2 backlog | Visualiser, badges, demo mode, BOQ | 🟢 9 items |

### Suggested build order for next session
1. Images for material choices (visual impact, relatively simple)
2. Cost breakdown section in report (data is there, just needs UI)
3. Vercel deployment (gets it live)
4. Cost override UI (contractor workflow)
5. Build sharing
6. Copy/duplicate build
