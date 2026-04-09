# Yojane — Pending Work Tracker
> Last updated: 2026-04-09 — ACTIVE MIGRATION IN PROGRESS

---

## 🔴 ACTIVE WORK: Registry → Simulator Migration (Option B)

### The Core Problem (solved in architecture, now implementing)
The app has two data systems that are not connected:
- `registry.csv` — 134 material rows, 27 subcategories, all validated ✅
- Hardcoded TypeScript (`materials-foundation.ts`, `decision-points.ts`) — what the simulator actually reads ❌

### The Fix: Option B — Join by `subcategory_name`
Each `DecisionPoint` gets a `subcategory?: string` field. If set, the simulator fetches
components from the Supabase `components` table WHERE `subcategory_name = that value`.
Those components become the spectrum slider options. Decision points without a subcategory
fall back to simple list-picker mode (no change needed there).

### Decision Point → Subcategory Mappings

| Decision | Label | Registry Subcategory | Status |
|---|---|---|---|
| A1 | Foundation Type | `Foundation Type` | Mapped |
| A2 | Excavation Depth | — | List only |
| A3 | Concrete Mix Grade | — | List only |
| A4 | Steel Reinforcement Grade | — | List only |
| A5 | DPC | — | List only |
| A6 | Termite Protection | `Soil Treatment` | Mapped |
| A7 | Plinth Height | — | List only |
| A8 | Plinth Filling Material | — | List only |
| A9 | Underground Water Tank | — | List only |
| B1 | Structural System | `Structural System` | Mapped |
| B2 | Wall Material | `Wall System` | Mapped |
| B3 | Wall Configuration | — | List only |
| B4 | Mortar Type | — | List only |
| B5 | Lintel & Sunshade | — | List only |
| B6 | External Plastering | `Wall Finish` | Mapped |
| C1 | Roof Structure | `Roof Type` | Mapped |
| C2 | Roof Covering | `Roofing Material` | Mapped |
| C3 | Roof Insulation/Treatment | `Insulation` | Mapped |
| C4 | Waterproofing System | `Waterproofing` | Mapped |
| C5 | Parapet / Edge Detail | — | List only |
| C6 | Rainwater Harvesting | `Rainwater Harvesting` | Mapped |
| D1 | Flooring — Living Areas | `Flooring` | Mapped |
| D2 | Flooring — Wet Areas | `Flooring` | Mapped (same subcategory) |
| D3 | Flooring — External | `Flooring` | Mapped (same subcategory) |
| D4 | Internal Wall Finish | `Wall Finish` | Mapped |
| D5 | Kitchen Countertop | — | List only |
| D6 | Bathroom Fixtures Grade | — | List only |
| D7 | Main Entry Door | `Doors` | Mapped |
| D8 | Internal Doors | `Doors` | Mapped (same subcategory) |
| D9 | Windows | `Windows` | Mapped |
| E1 | Water Supply Piping | `Plumbing` | Mapped |
| E2 | Drainage / Sewage Piping | `Plumbing` | Mapped (same subcategory) |
| E3 | Electrical Wiring | `Electrical` | Mapped |
| E4 | Electrical Load Planning | — | List only |
| E5 | Electrical Points Density | — | List only |
| E6 | Solar Provision | `Solar` | Mapped |
| E7 | Water Heating System | — | List only |
| E8 | Rainwater Plumbing | — | List only |
| E9 | Sewage Treatment | `Waste Management` | Mapped |
| E10 | Inverter / UPS Wiring | — | List only |
| F1 | Compound Wall | — | List only |
| F2 | Gate & Entry | — | List only |
| F3 | Driveway & Paving | — | List only |
| F4 | Garden / Landscape | — | List only |
| F5 | External Lighting | `Lighting Strategy` | Mapped |

**Registry subcategories not yet assigned to a decision point:**
HVAC, Glazing, Ceiling, Column Grid, Floor System, Green Rating Target,
Senior-Friendly, High-Seismic, Flood-Prone — add as new decision points later.

### Migration Task Checklist
- [x] Analyse full decision-point ↔ registry mapping
- [x] **Add `Component` type to `types/index.ts`** (registry row shape, 49 columns)
- [x] **Add `subcategory?: string` to `DecisionPoint` type**
- [x] **Add subcategory field to all 37 decision points in `decision-points.ts`**
- [x] **Update `BuildSimulator.tsx`**: fetches all components on mount, groups by subcategory_name, passes down to DecisionCard
- [x] **Rewrite `DecisionCard.tsx`**: accepts `components: Component[]`; full spectrum slider with registry data; falls back to list-picker if empty
- [x] **Rewrite `scoring.ts`**: uses `durability_score`, `energy_impact_modifier`, `thermal_resistance_score`, `acoustic_score` directly. All hardcoded lookup tables removed.
- [x] **Rewrite `auto-decide.ts`**: uses `Component` fields; budget tier filtering via `spectrum_position`
- [x] **Rewrite `AutoDecidePanel.tsx`**: receives `componentsBySubcategory` from BuildSimulator
- [x] **Rewrite `report/page.tsx`**: fetches components from Supabase server-side; shows `display_name`, cost/sqft, lifespan in Decision Log; maintenance calendar uses registry lifecycle fields
- [x] **Delete `materials-foundation.ts`**
- [x] **Remove `MaterialEntry` type from `types/index.ts`** (replaced by `Component`)

### ✅ COMPLETED — Supabase import
The code is wired. The `components` table just needs to be created and populated.
Until this is done the app runs in fallback mode (list-pickers, no spectrum sliders).

**Step 1 — Create the table**
Open [Supabase Dashboard](https://app.supabase.com) → your project → SQL Editor
Paste and run the `CREATE TABLE components` block from `supabase/schema.sql`
(lines 26–116, the `components` table only — builds/decisions tables may already exist)

**Step 2 — Import the CSV**
Supabase Dashboard → Table Editor → `components` table → Import data → CSV
Select: `src/data/registry.csv`
Make sure "First row is header" is ticked.
134 rows will be imported.

**Step 3 — Verify**
```sql
SELECT subcategory_name, COUNT(*) FROM components GROUP BY subcategory_name ORDER BY subcategory_name;
```
Should return 27 rows, each with 4–8 components.

**After import:** all 20 decision points with a `subcategory` mapping will show the spectrum slider with real material data, costs, scores, and expert advisory notes.

---

## 🔴 Critical / Blocking (unblocked after migration above)

### 2. Google Maps Pin Drop (Onboarding Step 2)
- Add `NEXT_PUBLIC_GOOGLE_MAPS_KEY` to `.env.local`
- Enable Maps JavaScript API + Elevation API in Google Cloud Console
- Replace placeholder in `src/app/dashboard/new/page.tsx`
- Auto-derive: climate zone, seismic zone, rainfall, soil type, elevation from lat/lng

### 3. Images / Visual References for Material Choices
- Add `image_url` column to `components` table in Supabase
- Curate photos, upload to Supabase Storage
- Show thumbnail in spectrum slider beside option name

---

## 🟡 Important / Should-have for v1 launch

### 4. Architect Layer
- "Architect Insights" panel in simulator sidebar
- Sun path, ventilation quality, Vastu conflict alerts

### 5. Build Report — Full Sections
| Section | Status |
|---------|--------|
| A: Project Summary | ✅ Done |
| B: Decision Log | ✅ Partial |
| C: Cost Breakdown | ❌ Missing — needs Component data from registry |
| D: Score Summary | ✅ Partial |
| E: Maintenance Calendar | ✅ Partial |
| F: "Consider Reviewing" | ❌ Missing |

### 6. Cost Override (Contractor Quote Entry)
- "Enter actual quote" button per decision card
- `cost_override` field exists in DB, not in UI

### 7. Build Sharing (Read-only Link)
- `shared_links` table exists in DB
- `/share/[token]` route not built

### 8. Copy / Duplicate Build
- `is_copy_of` field in DB, not in UI
- "Duplicate" button on dashboard build cards

### 9. PDF Quality
- Switch to `@react-pdf/renderer` for proper A4 PDF

### 10. Vercel Deployment
1. Push `yojane/` to GitHub
2. Connect to Vercel
3. Set env vars (Supabase URL + key, Maps key)
4. Configure `yojane.pradeepjainbp.in` CNAME in Cloudflare
5. Add auth callback URL to Google OAuth

---

## 🟢 Nice-to-have / v2

11. Isometric Building Visualiser (PixiJS, proper textures)
12. 20-Year Fast-Forward Animation
13. Achievement Badges
14. "What Yojane Users Chose" Benchmarks
15. Myth Buster Feature (fields already in registry)
16. BOQ (Bill of Quantities) Generation
17. Demo Mode (unauthenticated)
18. Additional Building Types (full depth)
19. Integration with pradeepjainbp.in

---

## 📊 Summary

| Category | Count | Status |
|----------|-------|--------|
| Active migration tasks | 10 | 🔴 In progress |
| Critical blockers | 2 | 🔴 Not done |
| Important v1 features | 7 | 🟡 Not done |
| v2 / Nice-to-have | 9 | 🟢 Backlog |
