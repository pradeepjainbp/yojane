-- Fix sort_order so each subcategory is ordered cheapest → most expensive
-- Generated 2026-04-10

-- Ceiling
UPDATE components SET sort_order = 2 WHERE component_id = 'CEIL-005';  -- Metal Tile / Lay-in Grid Ceiling (₹110/sqft)
UPDATE components SET sort_order = 3 WHERE component_id = 'CEIL-002';  -- POP False Ceiling (Plaster of Paris) (₹140/sqft)
UPDATE components SET sort_order = 4 WHERE component_id = 'CEIL-003';  -- Gypsum Board False Ceiling (Drywall) (₹180/sqft)
UPDATE components SET sort_order = 5 WHERE component_id = 'CEIL-004';  -- Timber / Wooden Ceiling Panel (₹370/sqft)

-- Floor System
UPDATE components SET sort_order = 1 WHERE component_id = 'FS-003';  -- Hollow Core Precast Slab (₹190/sqft)
UPDATE components SET sort_order = 2 WHERE component_id = 'FS-001';  -- Solid RCC Slab (Conventional) (₹243/sqft)
UPDATE components SET sort_order = 3 WHERE component_id = 'FS-002';  -- Ribbed / Waffle Slab (₹270/sqft)

-- Flooring
UPDATE components SET sort_order = 3 WHERE component_id = 'FLR-004';  -- Kotah Stone (₹96/sqft)
UPDATE components SET sort_order = 4 WHERE component_id = 'FLR-003';  -- Vitrified Tile (₹107/sqft)
UPDATE components SET sort_order = 6 WHERE component_id = 'FLR-007';  -- Engineered Wood / Laminate (₹180/sqft)
UPDATE components SET sort_order = 7 WHERE component_id = 'FLR-006';  -- Indian Marble (₹250/sqft)

-- Insulation
UPDATE components SET sort_order = 3 WHERE component_id = 'INS-005';  -- Rockwool Slab (50mm) (₹22/sqft)
UPDATE components SET sort_order = 5 WHERE component_id = 'INS-008';  -- Glasswool Board (50mm) (₹34/sqft)
UPDATE components SET sort_order = 6 WHERE component_id = 'INS-003';  -- EPS Board (50mm) (₹37/sqft)
UPDATE components SET sort_order = 8 WHERE component_id = 'INS-006';  -- XPS Board (50mm) (₹66/sqft)

-- Lighting Strategy
UPDATE components SET sort_order = 2 WHERE component_id = 'LGT-005';  -- Passive Daylighting + Solar Tubes (₹60/sqft)
UPDATE components SET sort_order = 3 WHERE component_id = 'LGT-002';  -- Standard LED Downlights + Ceiling Fans (₹63/sqft)
UPDATE components SET sort_order = 4 WHERE component_id = 'LGT-003';  -- Layered Lighting Design (Ambient + Task + Accent) (₹125/sqft)
UPDATE components SET sort_order = 5 WHERE component_id = 'LGT-004';  -- Smart Dimmable LED System (₹195/sqft)

-- Plinth Filling
UPDATE components SET sort_order = 2 WHERE component_id = 'PFILL-003';  -- Quarry Dust (M-Sand) Filling (₹10/sqft)
UPDATE components SET sort_order = 3 WHERE component_id = 'PFILL-002';  -- River Sand Filling (₹11/sqft)

-- Plumbing
UPDATE components SET sort_order = 2 WHERE component_id = 'PLB-003';  -- uPVC Plumbing (Cold Water Only) (₹97/sqft)
UPDATE components SET sort_order = 3 WHERE component_id = 'PLB-002';  -- CPVC Concealed Plumbing (₹125/sqft)

-- Roof Type
UPDATE components SET sort_order = 1 WHERE component_id = 'RT-002';  -- Sloped Gable Roof (Pitched) (₹150/sqft)
UPDATE components SET sort_order = 2 WHERE component_id = 'RT-004';  -- Hip Roof (Four-Slope) (₹180/sqft)
UPDATE components SET sort_order = 3 WHERE component_id = 'RT-001';  -- Flat RCC Roof Slab (₹243/sqft)
UPDATE components SET sort_order = 4 WHERE component_id = 'RT-005';  -- Barrel Vault / Shell Roof (₹305/sqft)
UPDATE components SET sort_order = 5 WHERE component_id = 'RT-003';  -- Madras Terrace (Lime Concrete) (₹370/sqft)

-- Roofing Material
UPDATE components SET sort_order = 1 WHERE component_id = 'ENV-ROOF-002';  -- Mangalore Clay Tile (₹36/sqft)
UPDATE components SET sort_order = 2 WHERE component_id = 'ENV-ROOF-001';  -- Galvanized Iron (GI) Sheet (₹50/sqft)
UPDATE components SET sort_order = 3 WHERE component_id = 'ENV-ROOF-004';  -- Pre-coated Metal Sheet (₹61/sqft)
UPDATE components SET sort_order = 4 WHERE component_id = 'ENV-ROOF-003';  -- Concrete RCC Slab (₹243/sqft)

-- Structural System
UPDATE components SET sort_order = 3 WHERE component_id = 'UB-STR-005';  -- Light Gauge Steel Frame (LGSF) (₹1200/sqft)
UPDATE components SET sort_order = 4 WHERE component_id = 'UB-STR-003';  -- Standard RCC Frame (M25 Grade) (₹1320/sqft)
UPDATE components SET sort_order = 5 WHERE component_id = 'UB-STR-006';  -- Precast Concrete Panels (₹1450/sqft)
UPDATE components SET sort_order = 6 WHERE component_id = 'UB-STR-007';  -- Hybrid Composite (Steel Columns + RCC Slab) (₹1450/sqft)
UPDATE components SET sort_order = 7 WHERE component_id = 'UB-STR-004';  -- High-Performance RCC Frame (Coastal) (₹1520/sqft)

-- Wall Finish
UPDATE components SET sort_order = 1 WHERE component_id = 'WF-003';  -- POP Putty + Paint Finish (₹40/sqft)
UPDATE components SET sort_order = 2 WHERE component_id = 'WF-001';  -- Cement Sand Plaster (₹50/sqft)
UPDATE components SET sort_order = 3 WHERE component_id = 'WF-002';  -- Gypsum Plaster (Machine / Hand) (₹60/sqft)

-- Wall System
UPDATE components SET sort_order = 1 WHERE component_id = 'WS-005';  -- Fly Ash Brick (₹205/sqft)
UPDATE components SET sort_order = 2 WHERE component_id = 'WS-004';  -- Hollow Concrete Block (₹225/sqft)
UPDATE components SET sort_order = 3 WHERE component_id = 'WS-007';  -- CSEB (Earth Block) (₹250/sqft)
UPDATE components SET sort_order = 4 WHERE component_id = 'WS-002';  -- Solid Block (AAC) (₹260/sqft)
UPDATE components SET sort_order = 5 WHERE component_id = 'WS-003';  -- Porotherm (Hollow Clay) (₹290/sqft)
UPDATE components SET sort_order = 6 WHERE component_id = 'WS-001';  -- Wire-cut Red Brick (₹310/sqft)
UPDATE components SET sort_order = 7 WHERE component_id = 'WS-008';  -- Double-Wythe Cavity Wall (₹520/sqft)
UPDATE components SET sort_order = 8 WHERE component_id = 'WS-006';  -- Stabilized Rammed Earth (₹700/sqft)

-- Waterproofing
UPDATE components SET sort_order = 1 WHERE component_id = 'WP-002';  -- Cementitious Waterproofing Coating (₹46/sqft)
UPDATE components SET sort_order = 2 WHERE component_id = 'WP-001';  -- Brick Bat Coba (Weathering Course) (₹60/sqft)

-- Windows
UPDATE components SET sort_order = 1 WHERE component_id = 'WIN-005';  -- Louvred / Jalousie Ventilation Window (₹145/sqft)
UPDATE components SET sort_order = 2 WHERE component_id = 'WIN-001';  -- Aluminium Sliding Window (₹220/sqft)
UPDATE components SET sort_order = 3 WHERE component_id = 'WIN-002';  -- uPVC Sliding / Casement Window (₹335/sqft)
UPDATE components SET sort_order = 4 WHERE component_id = 'WIN-003';  -- Thermally Broken Aluminium Window (₹485/sqft)
UPDATE components SET sort_order = 5 WHERE component_id = 'WIN-004';  -- Timber / Wooden Casement Window (₹640/sqft)
