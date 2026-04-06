# Yojane — Pending Work Tracker
> Last updated: April 2026

---

## 🔴 Critical / Blocking (app doesn't work without these)

### 1. Material Registry — Stages B through F
**What:** Every decision card in Stages B–F currently shows "Data coming soon" because only Stage A (Foundation) materials are in the registry (`materials-foundation.ts`). The spectrum UI and AutoDecide engine both depend on cost + spec data.

**Files to create:**
- `src/data/materials-walls.ts` — AAC blocks, red brick, fly ash, laterite, SCB, HCB (decisions B1–B6)
- `src/data/materials-roofing.ts` — flat RCC, pitched truss, tiles, Galvalume, waterproofing (C1–C6)
- `src/data/materials-interiors.ts` — flooring, wall finish, doors, windows, countertops (D1–D9)
- `src/data/materials-mep.ts` — CPVC/PPR pipes, wiring, solar, sewage, geysers (E1–E10)
- `src/data/materials-landscape.ts` — compound wall, gate, driveway, garden, lighting (F1–F5)

**Effort:** High — real data from Karnataka PWD SOR needed for each entry (~200 material entries total)

---

### 2. Google Maps Pin Drop (Onboarding Step 2)
**What:** Currently shows a placeholder box. Users can't drop a pin to set their actual plot location. All climate/seismic/soil parameters are manually selected — should be auto-derived from coordinates.

**What's needed:**
- Add Google Maps JavaScript API key to `.env.local` (`NEXT_PUBLIC_GOOGLE_MAPS_KEY`)
- Enable Maps JavaScript API + Elevation API in Google Cloud Console
- Replace placeholder in `src/app/dashboard/new/page.tsx` (Step: Plot Location) with actual map
- Auto-derive: climate zone, seismic zone, rainfall, soil type, elevation from lat/lng

---

### 3. Images / Visual References for Material Choices
**What:** Decision cards show only text + specs. Users have no visual sense of what each material looks like. This was flagged by you directly.

**What's needed:**
- A set of photos/illustrations for each material option (AAC block texture, Mangalore tile appearance, granite vs vitrified tile, UPVC window frame, etc.)
- Add to spectrum picker: thumbnail image alongside the option name
- Low-cost approach: use CC-licensed photos or simple vector illustrations

---

## 🟡 Important / Should-have for v1 launch

### 4. Architect Layer
**What:** Spec Section 8 — the "80% architect" feature. Orientation analysis, cross-ventilation mapping, room proportion checks, privacy gradient scoring, Vastu conflict display.

**Currently:** Orientation bonus/penalty exists in scoring engine but is not surfaced to the user with any explanation or visualisation.

**What's needed:**
- An "Architect Insights" panel in the simulator sidebar
- Shows: sun path analysis for chosen road-facing direction, ventilation quality rating, recommended room placements
- Vastu conflict alerts (when vastu_enabled = true and a choice conflicts with optimal thermal/acoustic decision)

---

### 5. Build Report — Full Sections
**What:** Current report (`/build/[id]/report`) is a good skeleton but missing:

| Section | Status |
|---------|--------|
| A: Project Summary | ✅ Done |
| B: Decision Log | ✅ Partial (missing "alternatives considered" column) |
| C: Cost Breakdown | ❌ Missing — no stage-wise cost table, no material vs labour split, no pie chart |
| D: Score Summary | ✅ Partial (cards exist, but no sub-component radar chart) |
| E: Maintenance Calendar | ✅ Partial (only Stage A has maintenance data) |
| F: "Consider Reviewing" Recommendations | ❌ Missing — the diplomatic suggestions section |

---

### 6. Cost Override (Contractor Quote Entry)
**What:** Spec Section 13.4 — users should be able to enter their actual contractor quote for any material and see how it compares to the PWD benchmark. The `cost_override` field exists in the DB but is not exposed in the UI.

**What's needed:**
- Small "Enter actual quote" button on each selected option in the decision card
- Shows delta vs benchmark (e.g. "Your quote: ₹72/block · Benchmark: ₹65/block · +11% above")

---

### 7. Build Sharing (Read-only Link)
**What:** Spec Section 13.3 — generate a shareable link for any build. The `shared_links` table exists in the DB but the feature is not built.

**What's needed:**
- "Share Build" button in the simulator header
- Generates a unique token link (`/share/[token]`)
- Read-only view of the build: decisions, scores, isometric view — no edit capability
- "Fork this build" button for recipients (copies to their own account)

---

### 8. Copy / Duplicate Build
**What:** Spec Section 13.2 — "create a variant" use case (e.g. "Showing Contractor Raju", "If We Stretch Budget 10%"). The `is_copy_of` field exists in the DB but the UI doesn't expose it.

**What's needed:**
- "Duplicate" button on each build card in the dashboard
- Report for copied builds shows "X changes from original build"

---

### 9. PDF Quality
**What:** Current PDF uses `html2canvas` which captures the screen. On dark background this works but the result is a screenshot, not a professionally typeset PDF. For sharing with contractors, a cleaner layout is desirable.

**Improvement options:**
- Switch to `@react-pdf/renderer` for a proper typeset A4 PDF with clean white background
- Or: add a "print-friendly" CSS class that renders white background before capture

---

### 10. Vercel Deployment + Subdomain Setup
**What:** App only runs on `localhost:3000`. For access from `pradeepjainbp.in`, it needs to be deployed.

**Steps:**
1. Push `yojane/` to a GitHub repo (separate from the main website repo, or as a subfolder)
2. Connect to Vercel — auto-deploys on every push
3. Set environment variables in Vercel dashboard (Supabase URL + key, Maps key)
4. Configure `yojane.pradeepjainbp.in` subdomain: add CNAME record in Cloudflare pointing to Vercel
5. Add `https://yojane.pradeepjainbp.in/auth/callback` to Google OAuth authorized redirect URIs
6. Update `NEXT_PUBLIC_APP_URL` in Vercel env vars

---

## 🟢 Nice-to-have / v2 Features (per spec)

### 11. Isometric Building Visualiser (proper)
**What:** Currently a simplified SVG house outline. The spec calls for a full isometric engine using PixiJS with material-specific textures, stage-by-stage construction animation, and toggleable views (Normal / Structural / Thermal / MEP).

**Effort:** Very high — treat as a separate v2 milestone.

---

### 12. 20-Year Fast-Forward Animation
**What:** Spec Section v2 — cinematic time-lapse showing maintenance events, material degradation, cost accumulation over 20 years. Requires Maintenance View toggle.

---

### 13. Achievement Badges
**What:** Monsoon-Proof, Carbon Champion, The Accountant, Vastu Compliant, Renaissance Builder, Explorer. Awarded when score thresholds are met.

---

### 14. "What Yojane Users Chose" Benchmarks
**What:** At each decision point, show distribution of choices made by other users in the same climate zone. Requires aggregated data — only meaningful once user base grows.

---

### 15. Myth Buster Feature (surfaced proactively)
**What:** At each decision point, show a "The contractor might say…" vs "What the data says…" card. The `common_misconception` and `myth_buster_fact` fields are already in the material schema — just needs UI treatment.

---

### 16. BOQ (Bill of Quantities) Generation
**What:** A contractor-ready document with material quantities, specifications, and estimated costs. Requested by you in the conversation. More detailed than the current Build Report.

---

### 17. Demo Mode (Unauthenticated)
**What:** Spec Section 3.1 — unauthenticated users can explore the simulator with a pre-configured sample plot. Currently `/demo` route doesn't exist and login is required for everything.

---

### 18. Additional Building Types (full depth)
**What:** Currently only Individual Residential House has full decision depth (Stages A–F). The UI supports all 5 building types but the decision trees for apartment, commercial, agricultural, and utility are not differentiated.

---

### 19. Integration with pradeepjainbp.in
**What:** A card on the main website (currently the Plant Simulator "coming soon" area or a new card) that links to Yojane and supports Google login passthrough.

---

## 📊 Summary

| Category | Count | Status |
|----------|-------|--------|
| Critical blockers | 3 | 🔴 Not done |
| Important v1 features | 7 | 🟡 Not done |
| v2 / Nice-to-have | 9 | 🟢 Backlog |
| **Total pending** | **19** | |

### Suggested build order
1. Material registry (B–F) — everything else depends on this
2. Google Maps pin drop
3. Images for material choices
4. Cost breakdown section in report
5. Vercel deployment
6. Build sharing
7. Copy/duplicate build
8. Cost override UI
9. Architect Layer panel
10. PDF quality improvement
