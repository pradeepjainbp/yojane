# Yojane Component Registry — Status & Next Steps
*Last updated: 2026-04-09*

---

## What Is This Registry?

A 49-column CSV file (`registry.csv`) that is the **single source of truth** for all building material choices in the Yojane construction simulator. Every field feeds something in the app:

| Field group | Powers |
|---|---|
| `durability_score`, `thermal_resistance_score`, `energy_impact_modifier` | AI scoring weights (durability 35%, climate 30%, value 20%, carbon 15%) |
| `base_cost_per_sqft_inr` + lifecycle fields | Cost estimate engine |
| `climate_zone`, `climate_restrictions`, `hard_block_rule` | Climate fit scoring + hard blocks |
| `ai_advisory_notes`, `pros`, `cons` | "Let AI Decide" explanation panel |
| `spectrum_position` | Snap slider stop position |
| `tooltip_detail` | Hover tooltip on slider |

---

## Source Files

| File | Location | Purpose |
|---|---|---|
| `registry.csv` | `src/data/registry.csv` | **The clean master registry — use this** |
| `generate_registry.py` | `src/data/generate_registry.py` | Original script; generated first 9 subcategories |
| `fix_verify_flags.py` | `src/data/fix_verify_flags.py` | Resolved all 49 VERIFY flags; rewrites whole CSV |
| `append_*.py` | `src/data/append_*.py` | One script per subcategory (18 scripts total) |
| `UBIE_Component_Registry_Schema.xlsx` | `C:\Users\PradeepJain\Downloads\` | Schema template, AGENT_PROMPTS, EXAMPLE_ROWS, VALIDATION |
| `Building material Options.xlsx` | `C:\Users\PradeepJain\Downloads\` | Original first-attempt data (messy, used as source only) |

---

## Registry Current State

**Total: 134 rows | 49 columns | 27 subcategories | 0 VERIFY flags**
**ALL SUBCATEGORIES COMPLETE · ALL VERIFY FLAGS RESOLVED**

| # | Subcategory | Category | IDs | Options | Status |
|---|---|---|---|---|---|
| 1 | Structural System | Structure | UB-STR-001…007 | 7 | ✅ Validated |
| 2 | Foundation Type | Foundation | FND-001…005 | 5 | ✅ Validated |
| 3 | Roofing Material | Envelope | ENV-ROOF-001…005 | 5 | ✅ Validated |
| 4 | Wall System | Envelope | WS-001…008 | 8 | ✅ Validated |
| 5 | Insulation | Envelope | INS-001…008 | 8 | ✅ Validated |
| 6 | Flooring | Finishes | FLR-001…007 | 7 | ✅ Validated |
| 7 | HVAC | Systems | HVAC-001…005 | 5 | ✅ Validated |
| 8 | Glazing | Envelope | GLZ-001…004 | 4 | ✅ Validated |
| 9 | Doors | Finishes | DOR-001…005 | 5 | ✅ Validated |
| 10 | Windows | Finishes | WIN-001…005 | 5 | ✅ Validated |
| 11 | Wall Finish | Finishes | WF-001…005 | 5 | ✅ Validated |
| 12 | Electrical | Systems | ELEC-001…004 | 4 | ✅ Validated |
| 13 | Plumbing | Systems | PLB-001…005 | 5 | ✅ Validated |
| 14 | Ceiling | Finishes | CEIL-001…005 | 5 | ✅ Validated |
| 15 | Lighting Strategy | Systems | LGT-001…005 | 5 | ✅ Validated |
| 16 | Solar | Systems | SOL-001…005 | 5 | ✅ Validated |
| 17 | Rainwater Harvesting | Systems | RWH-001…004 | 4 | ✅ Validated |
| 18 | Waterproofing | Systems | WP-001…005 | 5 | ✅ Validated |
| 19 | Soil Treatment | Systems | ST-001…004 | 4 | ✅ Validated |
| 20 | Roof Type | Structure | RT-001…005 | 5 | ✅ Validated |
| 21 | Column Grid | Structure | CG-001…004 | 4 | ✅ Validated |
| 22 | Floor System | Structure | FS-001…004 | 4 | ✅ Validated |
| 23 | Green Rating Target | Sustainability | GR-001…004 | 4 | ✅ Validated |
| 24 | Waste Management | Systems | WM-001…004 | 4 | ✅ Validated |
| 25 | Senior-Friendly | Special | SF-001…004 | 4 | ✅ Validated |
| 26 | High-Seismic | Special | SZ-001…004 | 4 | ✅ Validated |
| 27 | Flood-Prone | Special | FP-001…004 | 4 | ✅ Validated |

### VERIFY flag resolution — completed 2026-04-09
All 49 flagged rows validated and corrected via `fix_verify_flags.py`. `verify_flags = 'None'` on all 134 rows.

**Value corrections made (not just flag-clearing):**

| Row | Field | Old | New | Source |
|---|---|---|---|---|
| ENV-ROOF-002 | annual_minor_maint_factor | 0.05 | 0.01 | BRE Digest 345 clay tile |
| WS-007 CSEB | major_maintenance_cost_factor | 0.20 | 0.12 | Auroville Earth Institute |
| WS-003 Porotherm | major_maintenance_cost_factor | 0.25 | 0.10 | Wienerberger India |
| WS-006 Rammed Earth | annual_minor_maint_factor | 0.05 | 0.02 | CRATerre guidelines |
| SOL-004 hybrid PV+battery | base / install (/sqft) | 85 / 18 | 195 / 45 | Luminous/SolarEdge India 2024 |
| SOL-005 off-grid | base / install (/sqft) | 145 / 30 | 380 / 75 | Loom Solar off-grid quotes 2024 |
| SF-004 aging-in-place | base / install (/sqft) | 55 / 20 | 85 / 30 | Lift shaft + automation market |
| SZ-004 seismic retrofit | base / install (/sqft) | 45 / 35 | 180 / 120 | IS 13935; NDMA guidelines |
| FP-004 amphibious design | base / install (/sqft) | 65 / 30 | 180 / 75 | CWRDM Kerala; pile foundation |

All other rows validated against CPWD DSR 2023, Karnataka PWD SOR 2024-25, IS codes, South India market rates 2024 — values were in range, only flags cleared.

---

## Append Scripts Created (reference)

| Script | Subcategories added | Rows | Running total |
|---|---|---|---|
| `generate_registry.py` | Structural System, Foundation, Roofing, Wall System, Insulation, Flooring, HVAC, Glazing, Doors | 54 | 54 |
| `append_windows.py` | Windows | 5 | 59 |
| `append_wall_finish.py` | Wall Finish | 5 | 64 |
| `append_electrical.py` | Electrical | 4 | 68 |
| `append_plumbing.py` | Plumbing | 5 | 73 |
| `append_ceiling.py` | Ceiling | 5 | 78 |
| `append_lighting.py` | Lighting Strategy | 5 | 83 |
| `append_solar.py` | Solar | 5 | 88 |
| `append_rainwater.py` | Rainwater Harvesting | 4 | 92 |
| `append_waterproofing.py` | Waterproofing | 5 | 97 |
| `append_soil_treatment.py` | Soil Treatment | 4 | 101 |
| `append_roof_type.py` | Roof Type | 5 | 106 |
| `append_column_grid.py` | Column Grid | 4 | 110 |
| `append_floor_system.py` | Floor System | 4 | 114 |
| `append_green_rating.py` | Green Rating Target | 4 | 118 |
| `append_waste_mgmt.py` | Waste Management | 4 | 122 |
| `append_senior_friendly.py` | Senior-Friendly | 4 | 126 |
| `append_high_seismic.py` | High-Seismic | 4 | 130 |
| `append_flood_prone.py` | Flood-Prone | 4 | **134** |
| `fix_verify_flags.py` | *(patches existing rows, no new rows)* | 0 | **134** |

---

## How to Import to Supabase

```sql
-- Step 1: Create the components table (49 columns matching registry.csv headers)
-- Step 2: Import via Supabase Dashboard → Table Editor → Import CSV
-- Or use the CLI:
supabase db execute --file import_registry.sql
```

The simulator will query:
```sql
SELECT * FROM components
WHERE subcategory_name = 'Flooring'
  AND climate_zone ILIKE '%Warm-Humid%'
ORDER BY sort_order;
```

---

## Next Steps (in priority order)

1. ~~**Build the 27 subcategory registry**~~ ✅ Done — 134 rows, all subcategories complete
2. ~~**Resolve VERIFY flags**~~ ✅ Done — all 49 flags resolved, 0 remaining
3. **Import to Supabase** — create `components` table, import registry.csv
4. **Wire simulator to registry** — replace hardcoded `decisions` array in `BuildSimulator.tsx` with a Supabase fetch keyed on `subcategory_name`
5. **Build hover tooltip UI** — on snap slider hover show: photo, cost, lifespan, durability score, `tooltip_detail`, pros/cons
6. **Wire AI scoring engine** — `Let AI Decide` scores each option in a subcategory on 4 weights, picks best fit for user's climate zone + budget
7. **Build Report cost breakdown** — stage-wise table using `base_cost_per_sqft_inr + installation_cost_per_sqft_inr` per selected option
8. **Add `image_url` column** — curate ~5 photos per subcategory, upload to Supabase Storage, add column to registry

---

## Key Design Decisions Already Made

- **Spectrum slider**: equidistant snap stops, blue→violet→gold colour scale (economical → premium)
- **AI button label**: "Let AI Decide" (not "Let Yojane Decide")
- **AI scoring weights**: Durability 35% · Climate fit 30% · Value 20% · Carbon 15%
- **Cost unit**: `base_cost_per_sqft_inr` = material only; `installation_cost_per_sqft_inr` = labour
- **HVAC/Doors/Windows cost**: normalised to ₹/sqft of conditioned area or leaf/opening area respectively
- **Solar cost**: normalised to ₹/sqft of built-up area of house
- **Registry scope**: South India (TN, KA, KL, AP) · CPWD DSR 2023 · Karnataka PWD SOR 2024-25 · ECBC 2017 · IS codes
