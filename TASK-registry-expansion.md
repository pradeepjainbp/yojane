# Task: Expand Registry to Cover All Decision Points

> **Author:** Claude (session 2026-04-10)  
> **Status:** Ready to implement  
> **Estimated scope:** ~90 new registry rows + updates to `decision-points.ts`

---

## Background & Architecture

Yojane has two modes for rendering a decision card:

1. **Spectrum Picker** — decision has `subcategory: 'Wall System'` and `options: []`. At runtime, the simulator fetches all `Component` rows with that `subcategory_name` from Supabase, orders them by `spectrum_position`, and renders a slider. The `chosen_option_id` saved to the DB is a `component_id` like `WS-002`.

2. **List Picker** — decision has `options: [{ id, label, hint }]` and no `subcategory`. Options are hardcoded in `src/data/decision-points.ts`. The `chosen_option_id` is a plain string like `MORTAR-CM16`.

**Goal of this task:** Migrate all 22 List Picker decisions to Spectrum Picker by adding their options as registry rows in `src/data/registry.csv` and updating `decision-points.ts` accordingly.

**Why:** Consistency in UI, unlocks cost calculation for all decisions (spectrum picks have `base_cost_per_sqft_inr`), enables future AI scoring and override UI.

---

## Key Files

| File | Role |
|------|------|
| `src/data/registry.csv` | Source of truth — imported to Supabase `components` table |
| `src/data/decision-points.ts` | Decision definitions — change `options: [...]` to `subcategory: '...'` + `options: []` |
| `src/types/index.ts` | `DecisionPoint` type — already has `subcategory?: string` |
| `supabase/schema.sql` | DB schema reference |
| `src/app/build/[id]/BuildSimulator.tsx` | Fetches all components on mount, groups by `subcategory_name` |

### Registry CSV Column Reference (49 columns)

```
component_id, category_name, subcategory_name, name, display_name, description,
region, climate_zone, spectrum_position, sort_order,
base_cost_per_sqft_inr, installation_cost_per_sqft_inr, cost_confidence, cost_last_updated, cost_source_notes,
expected_lifespan_years, replacement_cost_factor, major_maintenance_cycle_years,
major_maintenance_cost_factor, annual_minor_maint_factor, maintenance_complexity, lifecycle_source_notes,
thermal_resistance_score, acoustic_score, durability_score, moisture_resistance,
fire_rating, energy_impact_modifier, accessibility_score, thermal_source_notes,
max_floors_supported, min_floors_required, max_span_supported_m,
incompatible_with, compatible_with, requires_component, climate_restrictions,
hard_block_rule, advisory_rule, advisory_message, advisory_severity, constraint_source_notes,
ai_advisory_notes, pros, cons, tooltip_detail,
status, verify_flags, data_filled_by
```

**spectrum_position** values (ordered): `Basic` → `Intermediate` → `Standard` → `Performance` → `Heavy-Standard` → `Premium`

Use `Active` for status. Use `Medium` for cost_confidence when exact data isn't available. Leave advisory/constraint fields empty (`None` or blank) unless there's a real constraint.

---

## The 22 Decisions to Migrate

For each decision below, the table gives:
- Current hardcoded options (these become registry rows)
- Proposed `component_id` prefix
- Proposed `subcategory_name` (must match exactly in both CSV and `decision-points.ts`)

---

### A2 — Excavation Depth
**subcategory_name:** `Excavation Depth`  
**category_name:** `Structure`  
**ID prefix:** `EXC`

| component_id | display_name | spectrum_position | sort_order | base_cost_per_sqft_inr | install_cost | lifespan | durability_score | notes |
|---|---|---|---|---|---|---|---|---|
| EXC-001 | 600 mm (2 ft) | Basic | 1 | 5 | 3 | — | 5 | Soft/medium soil with good bearing |
| EXC-002 | 900 mm (3 ft) | Intermediate | 2 | 8 | 5 | — | 7 | Standard depth for most residential plots |
| EXC-003 | 1200 mm (4 ft) | Performance | 3 | 12 | 7 | — | 8 | Hard strata or high water table |
| EXC-004 | 1500 mm (5 ft) | Premium | 4 | 18 | 10 | — | 9 | Deep bearing required or waterlogged soil |

**decision-points.ts change for A2:**
```ts
// REMOVE: options: [{ id: 'EXC-600', ... }, ...]
// ADD:
subcategory: 'Excavation Depth',
options: [],
default_option: null,
```

---

### A3 — Concrete Mix Grade
**subcategory_name:** `Concrete Mix`  
**category_name:** `Structure`  
**ID prefix:** `CONC`

| component_id | display_name | spectrum_position | sort_order | base_cost_per_sqft_inr | install_cost | durability_score | notes |
|---|---|---|---|---|---|---|---|
| CONC-001 | M15 (PCC) | Basic | 1 | 40 | 20 | 5 | PCC only — walkways, leveling, lean concrete |
| CONC-002 | M20 (Standard RCC) | Intermediate | 2 | 52 | 25 | 7 | Standard — slabs, beams, columns G+1/G+2 |
| CONC-003 | M25 (High Strength) | Performance | 3 | 62 | 28 | 8 | G+3 and above, seismic zones III–IV |
| CONC-004 | M30 (Structural Premium) | Premium | 4 | 75 | 32 | 10 | G+4+, heavy loads, seismic zone V |

**decision-points.ts change for A3:**
```ts
subcategory: 'Concrete Mix',
options: [],
default_option: null,
```

---

### A4 — Steel Reinforcement Grade
**subcategory_name:** `Steel Grade`  
**category_name:** `Structure`  
**ID prefix:** `STEEL`

| component_id | display_name | spectrum_position | sort_order | base_cost_per_sqft_inr | install_cost | durability_score | notes |
|---|---|---|---|---|---|---|---|
| STEEL-001 | Fe 415 | Basic | 1 | 28 | 8 | 6 | Older BIS standard — still available |
| STEEL-002 | Fe 500 | Intermediate | 2 | 32 | 8 | 8 | Current BIS standard — most common |
| STEEL-003 | Fe 500D (Ductile) | Performance | 3 | 35 | 9 | 9 | Recommended for seismic zones III–IV |
| STEEL-004 | Fe 550 | Premium | 4 | 40 | 10 | 10 | Seismic zones IV–V, tall buildings |

---

### A5 — Damp Proof Course (DPC)
**subcategory_name:** `Damp Proof Course`  
**category_name:** `Structure`  
**ID prefix:** `DPC`

| component_id | display_name | spectrum_position | sort_order | base_cost_per_sqft_inr | install_cost | moisture_resistance | notes |
|---|---|---|---|---|---|---|---|
| DPC-001 | Cement mortar (1:3) | Basic | 1 | 3 | 2 | Medium | Standard — most common in South India |
| DPC-002 | Bituminous felt | Intermediate | 2 | 8 | 4 | High | Better waterproofing, moderate cost |
| DPC-003 | Polymer-modified membrane | Premium | 3 | 18 | 8 | Very High | Best performance, flood-prone plots |

---

### A7 — Plinth Height
**subcategory_name:** `Plinth Height`  
**category_name:** `Structure`  
**ID prefix:** `PLINTH`

| component_id | display_name | spectrum_position | sort_order | base_cost_per_sqft_inr | install_cost | notes |
|---|---|---|---|---|---|---|
| PLINTH-001 | 450 mm (1.5 ft) | Basic | 1 | 8 | 5 | Low — level/gently sloped plots |
| PLINTH-002 | 600 mm (2 ft) | Intermediate | 2 | 12 | 7 | Standard — Karnataka/Tamil Nadu norm |
| PLINTH-003 | 750 mm (2.5 ft) | Performance | 3 | 16 | 9 | Elevated — flood-prone / low-lying |
| PLINTH-004 | 900 mm (3 ft) | Premium | 4 | 22 | 12 | High — heavy rainfall zones, high flood risk |

---

### A8 — Plinth Filling Material
**subcategory_name:** `Plinth Filling`  
**category_name:** `Structure`  
**ID prefix:** `PFILL`

| component_id | display_name | spectrum_position | sort_order | base_cost_per_sqft_inr | install_cost | notes |
|---|---|---|---|---|---|---|
| PFILL-001 | Murrum / laterite | Basic | 1 | 4 | 3 | Local, good compaction, economical |
| PFILL-002 | River sand | Intermediate | 2 | 7 | 4 | Easy compaction, drains well |
| PFILL-003 | Quarry dust (M-sand) | Performance | 3 | 6 | 4 | Good drainage, Karnataka availability |

---

### A9 — Underground Water Tank (Sump)
**subcategory_name:** `Underground Water Tank`  
**category_name:** `Systems`  
**ID prefix:** `UWT`

| component_id | display_name | spectrum_position | sort_order | base_cost_per_sqft_inr | install_cost | lifespan | notes |
|---|---|---|---|---|---|---|---|
| UWT-001 | No underground tank | Basic | 1 | 0 | 0 | — | Only if municipal supply fully reliable |
| UWT-002 | Pre-moulded plastic (Sintex) | Intermediate | 2 | 5 | 3 | 15 | Fastest install, lowest cost, shorter life |
| UWT-003 | Ferro-cement tank | Performance | 3 | 10 | 6 | 25 | Lighter, faster to build, moderate cost |
| UWT-004 | RCC sump (in-situ) | Premium | 4 | 18 | 12 | 40 | Most durable, 30+ year life — standard |

---

### B3 — Wall Configuration
**subcategory_name:** `Wall Configuration`  
**category_name:** `Envelope`  
**ID prefix:** `WCFG`

| component_id | display_name | spectrum_position | sort_order | base_cost_per_sqft_inr | install_cost | thermal_resistance_score | notes |
|---|---|---|---|---|---|---|---|
| WCFG-001 | Single wythe | Basic | 1 | 0 | 0 | 4 | Standard construction — economical |
| WCFG-002 | Cavity wall | Performance | 2 | 15 | 8 | 7 | Air gap — better thermal, coastal / humid |
| WCFG-003 | Insulated cavity | Premium | 3 | 28 | 12 | 9 | Cavity + insulation — premium thermal |

---

### B4 — Mortar Type
**subcategory_name:** `Mortar Type`  
**category_name:** `Structure`  
**ID prefix:** `MORT`

| component_id | display_name | spectrum_position | sort_order | base_cost_per_sqft_inr | install_cost | notes |
|---|---|---|---|---|---|---|
| MORT-001 | Cement mortar 1:6 | Basic | 1 | 4 | 3 | Standard — most residential masonry |
| MORT-002 | Cement mortar 1:4 | Intermediate | 2 | 5 | 3 | Stronger — load-bearing, exposed walls |
| MORT-003 | Thin-bed mortar | Performance | 3 | 9 | 4 | For AAC blocks — precision jointing |
| MORT-004 | Polymer-modified mortar | Premium | 4 | 14 | 5 | Better adhesion and flexibility |

**Note:** Add constraint in B4 — when B2 is `WS-002` (AAC Block), recommend `MORT-003`.

---

### B5 — Lintel & Sunshade (Chajja)
**subcategory_name:** `Lintel & Sunshade`  
**category_name:** `Envelope`  
**ID prefix:** `LINT`

| component_id | display_name | spectrum_position | sort_order | base_cost_per_sqft_inr | install_cost | energy_impact_modifier | notes |
|---|---|---|---|---|---|---|---|
| LINT-001 | RCC lintel only | Basic | 1 | 5 | 3 | 0.0 | Structural minimum — no solar shading |
| LINT-002 | Lintel + sunshade (chajja) | Intermediate | 2 | 10 | 6 | 0.1 | Recommended — reduces heat gain 15–25% |
| LINT-003 | Band + deep extended chajja | Premium | 3 | 18 | 10 | 0.2 | Best solar shading — integrated band beam |

---

### C5 — Parapet / Edge Detail
**subcategory_name:** `Parapet`  
**category_name:** `Envelope`  
**ID prefix:** `PARA`

| component_id | display_name | spectrum_position | sort_order | base_cost_per_sqft_inr | install_cost | notes |
|---|---|---|---|---|---|---|
| PARA-001 | Brick masonry parapet | Basic | 1 | 6 | 4 | Traditional, economical, maintenance-free |
| PARA-002 | RCC parapet | Intermediate | 2 | 10 | 6 | Stronger, better weathering — most common |
| PARA-003 | Metal railing | Performance | 3 | 14 | 7 | Open/modern aesthetic — needs edge trim |

---

### D5 — Kitchen Countertop
**subcategory_name:** `Kitchen Countertop`  
**category_name:** `Finishes`  
**ID prefix:** `CTOP`

| component_id | display_name | spectrum_position | sort_order | base_cost_per_sqft_inr | install_cost | durability_score | notes |
|---|---|---|---|---|---|---|---|
| CTOP-001 | Ceramic tile | Basic | 1 | 25 | 10 | 5 | Economical but grout needs maintenance |
| CTOP-002 | Granite | Intermediate | 2 | 55 | 18 | 9 | Most popular in Karnataka — durable, heat-resistant |
| CTOP-003 | Solid surface (Corian) | Performance | 3 | 90 | 22 | 7 | Seamless, repairable scratches |
| CTOP-004 | Engineered quartz | Premium | 4 | 120 | 28 | 10 | Non-porous, low maintenance |

---

### D6 — Bathroom Fixtures Grade
**subcategory_name:** `Bathroom Fixtures`  
**category_name:** `Finishes`  
**ID prefix:** `BATH`

| component_id | display_name | spectrum_position | sort_order | base_cost_per_sqft_inr | install_cost | notes |
|---|---|---|---|---|---|---|
| BATH-001 | Economy | Basic | 1 | 12 | 6 | Cera, Hindware economy range |
| BATH-002 | Mid-range | Intermediate | 2 | 25 | 10 | Jaquar, Parryware, Hindware premium |
| BATH-003 | Premium | Premium | 3 | 60 | 18 | Kohler, TOTO, Duravit |

---

### E4 — Electrical Load Planning
**subcategory_name:** `Electrical Load`  
**category_name:** `Systems`  
**ID prefix:** `ELOAD`

| component_id | display_name | spectrum_position | sort_order | base_cost_per_sqft_inr | install_cost | notes |
|---|---|---|---|---|---|---|
| ELOAD-001 | 5 kW single phase | Basic | 1 | 8 | 5 | Small 1–2 BHK, no/minimal AC |
| ELOAD-002 | 10 kW three phase | Intermediate | 2 | 14 | 8 | Standard 3 BHK with 2–3 ACs |
| ELOAD-003 | 15 kW three phase + EV ready | Premium | 3 | 22 | 12 | Future-ready — EV, home office, solar |

---

### E5 — Electrical Points Density
**subcategory_name:** `Electrical Points`  
**category_name:** `Systems`  
**ID prefix:** `EPOINTS`

| component_id | display_name | spectrum_position | sort_order | base_cost_per_sqft_inr | install_cost | notes |
|---|---|---|---|---|---|---|
| EPOINTS-001 | Basic | Basic | 1 | 4 | 3 | 1–2 sockets per room, no data/USB |
| EPOINTS-002 | Standard | Intermediate | 2 | 8 | 5 | 3–4 sockets, TV point, 1 data point |
| EPOINTS-003 | Premium | Premium | 3 | 16 | 9 | 5+ sockets, USB, data, EV, home automation conduit |

---

### E7 — Water Heating System
**subcategory_name:** `Water Heating`  
**category_name:** `Systems`  
**ID prefix:** `WH`

| component_id | display_name | spectrum_position | sort_order | base_cost_per_sqft_inr | install_cost | energy_impact_modifier | notes |
|---|---|---|---|---|---|---|---|
| WH-001 | Electric geyser | Basic | 1 | 3 | 2 | -0.2 | Instant/storage — low upfront, high running cost |
| WH-002 | Gas geyser | Intermediate | 2 | 5 | 3 | -0.1 | Fast, consistent — needs PNG connection |
| WH-003 | Solar water heater | Performance | 3 | 12 | 6 | 0.2 | Best for South India — 4–5 year payback |
| WH-004 | Heat pump | Premium | 4 | 20 | 10 | 0.3 | 60% less electricity than geyser |

---

### E8 — Rainwater Plumbing
**subcategory_name:** `Rainwater Plumbing`  
**category_name:** `Systems`  
**ID prefix:** `RWPL`

| component_id | display_name | spectrum_position | sort_order | base_cost_per_sqft_inr | install_cost | notes |
|---|---|---|---|---|---|---|
| RWPL-001 | Combined roof + waste pipes | Basic | 1 | 2 | 1 | Cheapest — not recommended if RWH planned |
| RWPL-002 | Separate roof drain pipes | Intermediate | 2 | 5 | 3 | Standard for RWH — dedicated downpipes |
| RWPL-003 | Dual system with grey water | Premium | 3 | 12 | 8 | Full RWH + grey water reuse — BBMP compliant |

**Note:** Advisory when C6 is `RWH-004` (dual system), recommend `RWPL-003`.

---

### E10 — Inverter / UPS Wiring
**subcategory_name:** `UPS Provision`  
**category_name:** `Systems`  
**ID prefix:** `UPS`

| component_id | display_name | spectrum_position | sort_order | base_cost_per_sqft_inr | install_cost | notes |
|---|---|---|---|---|---|---|
| UPS-001 | No UPS provision | Basic | 1 | 0 | 0 | Only if grid supply fully reliable |
| UPS-002 | Essentials circuit | Intermediate | 2 | 4 | 3 | Lights, fans, router — 4 dedicated circuits |
| UPS-003 | Whole-house backup | Premium | 3 | 10 | 7 | All circuits on backup — frequent cut areas |

---

### F1 — Compound Wall
**subcategory_name:** `Compound Wall`  
**category_name:** `External`  
**ID prefix:** `CWALL`

| component_id | display_name | spectrum_position | sort_order | base_cost_per_sqft_inr | install_cost | durability_score | notes |
|---|---|---|---|---|---|---|---|
| CWALL-001 | Live hedge | Basic | 1 | 5 | 3 | 4 | Green, permeable — needs maintenance |
| CWALL-002 | Metal palisade / grille | Intermediate | 2 | 18 | 8 | 6 | Open, modern — good visibility |
| CWALL-003 | Precast concrete panels | Standard | 3 | 25 | 10 | 7 | Fast installation, economical |
| CWALL-004 | Random rubble stone | Performance | 4 | 35 | 18 | 8 | Aesthetic, vernacular — moderate cost |
| CWALL-005 | Brick masonry | Premium | 5 | 45 | 22 | 9 | Traditional, strong, maintenance-free |

---

### F2 — Gate & Entry
**subcategory_name:** `Gate & Entry`  
**category_name:** `External`  
**ID prefix:** `GATE`

| component_id | display_name | spectrum_position | sort_order | base_cost_per_sqft_inr | install_cost | notes |
|---|---|---|---|---|---|---|
| GATE-001 | Wooden gate | Basic | 1 | 15 | 8 | Aesthetic — needs termite treatment |
| GATE-002 | MS fabricated gate | Intermediate | 2 | 25 | 10 | Most common, powder-coated |
| GATE-003 | Aluminium gate | Performance | 3 | 35 | 12 | Light, rust-free |
| GATE-004 | Wrought iron gate | Standard | 4 | 45 | 18 | Decorative — high maintenance |
| GATE-005 | Automated sliding gate | Premium | 5 | 80 | 30 | Motor + remote, highest convenience |

---

### F3 — Driveway & Paving
**subcategory_name:** `Driveway Paving`  
**category_name:** `External`  
**ID prefix:** `DRIVE`

| component_id | display_name | spectrum_position | sort_order | base_cost_per_sqft_inr | install_cost | notes |
|---|---|---|---|---|---|---|
| DRIVE-001 | Gravel / crushed stone | Basic | 1 | 5 | 2 | Permeable, lowest cost — needs top-up |
| DRIVE-002 | Plain cement concrete (PCC) | Intermediate | 2 | 18 | 8 | Durable, low maintenance |
| DRIVE-003 | Interlocking paver blocks | Performance | 3 | 28 | 12 | Permeable, repairable, attractive |
| DRIVE-004 | Exposed aggregate concrete | Premium | 4 | 35 | 15 | Non-slip, attractive texture |

---

### F4 — Garden / Landscape
**subcategory_name:** `Garden Landscape`  
**category_name:** `External`  
**ID prefix:** `GARD`

| component_id | display_name | spectrum_position | sort_order | base_cost_per_sqft_inr | install_cost | energy_impact_modifier | notes |
|---|---|---|---|---|---|---|---|
| GARD-001 | No landscaping | Basic | 1 | 0 | 0 | 0.0 | All hardscape — minimal maintenance |
| GARD-002 | Basic lawn + border planting | Intermediate | 2 | 8 | 4 | 0.05 | Simple, low cost, periodic care |
| GARD-003 | Designed landscape | Performance | 3 | 20 | 10 | 0.15 | Shade trees — long-term cooling benefit |
| GARD-004 | Terrace / rooftop garden | Premium | 4 | 35 | 18 | 0.2 | Premium — insulation + stormwater benefit |

---

## Step-by-Step Implementation Instructions

### Step 1 — Add rows to registry.csv

Append the ~90 new rows to `src/data/registry.csv` following this structure for each row. All 49 columns must be present (use empty string for unused fields):

```
component_id,category_name,subcategory_name,name,display_name,description,region,climate_zone,spectrum_position,sort_order,base_cost_per_sqft_inr,installation_cost_per_sqft_inr,cost_confidence,cost_last_updated,cost_source_notes,expected_lifespan_years,replacement_cost_factor,major_maintenance_cycle_years,major_maintenance_cost_factor,annual_minor_maint_factor,maintenance_complexity,lifecycle_source_notes,thermal_resistance_score,acoustic_score,durability_score,moisture_resistance,fire_rating,energy_impact_modifier,accessibility_score,thermal_source_notes,max_floors_supported,min_floors_required,max_span_supported_m,incompatible_with,compatible_with,requires_component,climate_restrictions,hard_block_rule,advisory_rule,advisory_message,advisory_severity,constraint_source_notes,ai_advisory_notes,pros,cons,tooltip_detail,status,verify_flags,data_filled_by
```

**Defaults for fields not listed in the tables above:**
- `region`: `South India`
- `climate_zone`: `Warm-Humid;Hot-Dry;Temperate`
- `cost_confidence`: `Medium`
- `cost_last_updated`: `2024-04-01 00:00:00`
- `cost_source_notes`: `Karnataka PWD SOR 2024-25 estimate`
- `replacement_cost_factor`: `1`
- `major_maintenance_cycle_years`: `10`
- `major_maintenance_cost_factor`: `0.1`
- `annual_minor_maint_factor`: `0.01`
- `maintenance_complexity`: `Low`
- `lifecycle_source_notes`: `Domain estimate`
- `thermal_resistance_score`: `5` (neutral, unless specified)
- `acoustic_score`: `5`
- `moisture_resistance`: `Medium`
- `fire_rating`: `Class A`
- `energy_impact_modifier`: `0`
- `accessibility_score`: `High`
- `max_floors_supported`: `4`
- `min_floors_required`: `1`
- `max_span_supported_m`: `6`
- All constraint/advisory/incompatible fields: empty or `None`
- `status`: `Active`
- `verify_flags`: `None`
- `data_filled_by`: `Domain Expert`

**For the `name` field** (internal snake_case identifier): use lowercase with underscores matching display_name. E.g., `600_mm_excavation`, `m20_standard_rcc`, `fe500d_ductile`.

**For `ai_advisory_notes`:** Write a 3–4 sentence paragraph in the voice of an experienced site engineer advising a first-time homeowner. See existing rows in registry.csv for tone. Focus on the most common mistakes related to that option.

**For `pros` and `cons`:** Semicolon-separated list of 3 items each.

**For `tooltip_detail`:** One sentence summary.

---

### Step 2 — Update decision-points.ts

For each of the 22 decisions, change the pattern from:

```ts
// BEFORE (list picker)
{
  id: 'A2',
  label: 'Excavation Depth',
  options: [
    { id: 'EXC-600', label: '600 mm (2 ft)', hint: '...' },
    ...
  ],
  default_option: 'EXC-900',
}
```

To:

```ts
// AFTER (spectrum picker)
{
  id: 'A2',
  label: 'Excavation Depth',
  subcategory: 'Excavation Depth',   // must match subcategory_name in CSV exactly
  options: [],
  default_option: null,
}
```

**Subcategory name mapping for each decision:**

| Decision ID | subcategory value |
|-------------|-------------------|
| A2 | `'Excavation Depth'` |
| A3 | `'Concrete Mix'` |
| A4 | `'Steel Grade'` |
| A5 | `'Damp Proof Course'` |
| A7 | `'Plinth Height'` |
| A8 | `'Plinth Filling'` |
| A9 | `'Underground Water Tank'` |
| B3 | `'Wall Configuration'` |
| B4 | `'Mortar Type'` |
| B5 | `'Lintel & Sunshade'` |
| C5 | `'Parapet'` |
| D5 | `'Kitchen Countertop'` |
| D6 | `'Bathroom Fixtures'` |
| E4 | `'Electrical Load'` |
| E5 | `'Electrical Points'` |
| E7 | `'Water Heating'` |
| E8 | `'Rainwater Plumbing'` |
| E10 | `'UPS Provision'` |
| F1 | `'Compound Wall'` |
| F2 | `'Gate & Entry'` |
| F3 | `'Driveway Paving'` |
| F4 | `'Garden Landscape'` |

Also remove `default_option` string values — or keep as `null`. The spectrum picker defaults to the first item if nothing is selected.

---

### Step 3 — Upload to Supabase

After updating the CSV, run this import via Supabase dashboard or CLI:

```sql
-- Option A: via Supabase Dashboard
-- Go to Table Editor → components → Import CSV → select registry.csv
-- OR via SQL: truncate and re-import all rows

-- Option B: via psql / supabase CLI
\copy components FROM 'src/data/registry.csv' CSV HEADER;
```

Or use the Supabase MCP tool if available in the session.

**Verify after import:**
```sql
SELECT subcategory_name, COUNT(*) FROM components GROUP BY subcategory_name ORDER BY subcategory_name;
```
You should see the 22 new subcategories with the correct row counts.

---

### Step 4 — Update auto-decide.ts (if needed)

Check `src/engine/auto-decide.ts` — it already handles `dp.options[0]?.id` for list pickers. After migration, spectrum decisions are handled differently (they look up components from the registry). Confirm the auto-decide logic uses `componentsBySubcategory[dp.subcategory]` for spectrum-type decisions and does not break.

---

## Secondary Task: Add Decision Points for Unused Registry Subcategories

The registry already has data for these 9 subcategories that have **no decision point** assigned to them:

| subcategory_name | Items | Suggested Decision ID | Stage | Label |
|---|---|---|---|---|
| `HVAC` | 5 | G1 or add to Stage E | E | Cooling Strategy |
| `Glazing` | 4 | Add to Stage B or D | D or B | Window Glazing Type |
| `Ceiling` | 5 | Add to Stage D | D | Ceiling Finish |
| `Column Grid` | 4 | Add to Stage B | B | Structural Column Grid |
| `Floor System` | 4 | Add to Stage B | B | Floor/Slab System |
| `Green Rating Target` | 4 | New Stage G | G | Sustainability Target |
| `Senior-Friendly` | 4 | New Stage G | G | Universal Design / Accessibility |
| `High-Seismic` | 4 | Add to Stage A | A | Seismic Zone Provision |
| `Flood-Prone` | 4 | Add to Stage A | A | Flood Risk Provision |

For each, add a `DecisionPoint` entry in `decision-points.ts` with `subcategory` set and `options: []`. Most of these are in the registry and ready to render immediately.

**Priority order:** HVAC > Glazing > Ceiling > Seismic/Flood (situation-specific) > Column Grid / Floor System (technical, engineer-oriented)

---

## Future: Homeowner vs Engineer Question Classification

Add a `audience` field to `DecisionPoint` type in `src/types/index.ts`:

```ts
export interface DecisionPoint {
  // ... existing fields ...
  audience: 'homeowner' | 'engineer' | 'both'
}
```

Then classify each decision:

| Audience | Decisions |
|----------|-----------|
| `homeowner` | A1, A6, A7, A9, B1, B2, B5, B6, C1–C4, C6, D1–D9, E4, E6, E7, E9, E10, F1–F5 |
| `engineer` | A2, A3, A4, A5, A8, B3, B4, C5, E2, E3, E8 |
| `both` | B5 (lintel), E1 (plumbing), E5 (points density) |

UI feature: add a toggle "Show engineer decisions" in the simulator header. Default to `homeowner` only.

---

## Testing Checklist

After implementation:
- [ ] All 22 newly migrated decisions show as spectrum sliders (not list pickers)
- [ ] Component count in BuildSimulator header increases (was 129, should be ~220+)
- [ ] Clicking each spectrum slider saves a `component_id` (like `EXC-002`) not a plain string
- [ ] Score panel updates when sliding spectrum for new decisions
- [ ] Auto-decide still works for all decisions
- [ ] No TypeScript errors (`npm run build`)
- [ ] No hydration errors in browser console
- [ ] PENDING.md updated to reflect completed items
