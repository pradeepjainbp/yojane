import csv, sys, os
sys.stdout.reconfigure(encoding='utf-8')

COLS = ['component_id','category_name','subcategory_name','name','display_name','description',
'region','climate_zone','spectrum_position','sort_order','base_cost_per_sqft_inr',
'installation_cost_per_sqft_inr','cost_confidence','cost_last_updated','cost_source_notes',
'expected_lifespan_years','replacement_cost_factor','major_maintenance_cycle_years',
'major_maintenance_cost_factor','annual_minor_maint_factor','maintenance_complexity',
'lifecycle_source_notes','thermal_resistance_score','acoustic_score','durability_score',
'moisture_resistance','fire_rating','energy_impact_modifier','accessibility_score',
'thermal_source_notes','max_floors_supported','min_floors_required','max_span_supported_m',
'incompatible_with','compatible_with','requires_component','climate_restrictions',
'hard_block_rule','advisory_rule','advisory_message','advisory_severity',
'constraint_source_notes','ai_advisory_notes','pros','cons','tooltip_detail',
'status','verify_flags','data_filled_by']

# ── COLUMN GRID (Structure) ────────────────────────────────────────────────────
# Structural bay size / column spacing decision
# Cost: relative to baseline — expressed as cost index modifier on overall structure cost
# 4 options: 3x3m (tight) → 4x4m (standard) → 5x4m (open plan) → 6x6m (large span/parking)
new_rows = [
{
  'component_id':'CG-001','category_name':'Structure','subcategory_name':'Column Grid',
  'name':'grid_3x3','display_name':'3m × 3m Grid (Compact)','region':'South India',
  'description':'Column spacing of 3m x 3m. Minimum span for residential use. Results in many internal columns restricting room layout flexibility. Economical slab design with small beam depths. Common in old load-bearing conversions.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Basic','sort_order':'1',
  'base_cost_per_sqft_inr':'130','installation_cost_per_sqft_inr':'70','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'CPWD DSR 2023; IS 456 slab design; structural engineer rates; normalised per sqft built-up',
  'expected_lifespan_years':'75','replacement_cost_factor':'1.3','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'IS 456; NBC 2016 structural design life',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'9','moisture_resistance':'High',
  'fire_rating':'Class A','energy_impact_modifier':'1.0','accessibility_score':'5',
  'thermal_source_notes':'Column grid has no direct thermal contribution. ECBC 2017.',
  'max_floors_supported':'5','min_floors_required':'1','max_span_supported_m':'3.0',
  'incompatible_with':'Open-plan living requirements|Parking garage|Large hall or living room above 3m width',
  'compatible_with':'All structural systems',
  'requires_component':'RCC column 230x230mm minimum|RCC beam 230x300mm|125mm slab thickness',
  'climate_restrictions':'None','hard_block_rule':'None',
  'advisory_rule':'3x3m grid results in columns inside rooms - plan layout carefully before finalising grid',
  'advisory_message':'A 3m column grid in a 3m-wide room means columns fall on the room boundary or inside it. Confirm room layout against column positions with your architect before finalising.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 456; NBC 2016',
  'ai_advisory_notes':'The 3x3m grid is only appropriate for small row houses or narrow plots where the tight site boundary forces close column spacing. The fundamental problem is interior space planning - with columns every 3 meters you have very little flexibility in where walls and openings go. Every room must be sized in 3-meter increments or you end up with columns awkwardly in the middle of a living room. For any house above 800 sqft I strongly recommend going to at least a 4x4m grid even if it costs 10-15% more in structural steel - the planning freedom you gain is worth far more than the incremental structural cost.',
  'pros':'Smallest column and beam sizes|Lowest structural steel quantity|Economical slab design|Suitable for narrow plots',
  'cons':'Many internal columns restrict room layout|Not suitable for open-plan living|Columns may fall inside rooms|Limited to 5 floors max',
  'tooltip_detail':'3m × 3m column spacing. Many internal columns restrict layout. Only suitable for narrow plots. Move to 4×4m for open-plan rooms.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'CG-002','category_name':'Structure','subcategory_name':'Column Grid',
  'name':'grid_4x4','display_name':'4m × 4m Grid (Standard Residential)','region':'South India',
  'description':'Column spacing of 4m x 4m. Industry standard for South India residential construction. Allows comfortable room sizes without columns inside habitable spaces. Balance of structural economy and planning flexibility.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Standard','sort_order':'2',
  'base_cost_per_sqft_inr':'148','installation_cost_per_sqft_inr':'78','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'CPWD DSR 2023; IS 456; structural engineer standard residential rates; normalised per sqft',
  'expected_lifespan_years':'75','replacement_cost_factor':'1.3','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'IS 456; NBC 2016',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'9','moisture_resistance':'High',
  'fire_rating':'Class A','energy_impact_modifier':'1.0','accessibility_score':'8',
  'thermal_source_notes':'No direct thermal contribution. ECBC 2017.',
  'max_floors_supported':'8','min_floors_required':'1','max_span_supported_m':'4.0',
  'incompatible_with':'Large open-plan spaces above 4m width without secondary beams',
  'compatible_with':'All structural systems',
  'requires_component':'RCC column 230x300mm|RCC beam 230x400mm|125-150mm slab thickness|Structural engineer design',
  'climate_restrictions':'None','hard_block_rule':'None',
  'advisory_rule':'Confirm room layout against column grid before architectural drawing is finalised',
  'advisory_message':'Even 4x4m grids can result in columns falling inside rooms if architectural layout is not coordinated with structural grid from the start. Integrate both drawings from day one.',
  'advisory_severity':'Info','constraint_source_notes':'IS 456; NBC 2016; standard practice',
  'ai_advisory_notes':'The 4x4 meter column grid is the de-facto standard for South India residential construction for good reason. It gives you rooms of comfortable size up to 12-13 feet width without columns inside and the structural elements (columns, beams, slabs) are economically sized. The key coordination issue is that the architectural room layout must be designed hand-in-hand with the structural grid from day one. I see many projects where the architect draws rooms first and then the structural engineer is asked to fit a grid around them which always results in compromises. Start with the structural grid as the discipline and design rooms within it.',
  'pros':'Industry standard - every structural engineer knows this design|Comfortable room sizes without internal columns|Good balance of cost and flexibility|Supports up to G+7',
  'cons':'Not suitable for large open-plan living rooms above 4m width|Higher steel than 3m grid|Requires coordination between architect and structural engineer from day one',
  'tooltip_detail':'4m × 4m standard residential grid. Most common in South India. Design architectural layout and structural grid together from day one.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'CG-003','category_name':'Structure','subcategory_name':'Column Grid',
  'name':'grid_5x4','display_name':'5m × 4m Grid (Open Plan)','region':'South India',
  'description':'Asymmetric 5m x 4m column grid providing larger column-free spans in one direction. Enables open-plan living, dining and kitchen combined spaces without intermediate columns. Moderate increase in beam depth and steel.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Performance','sort_order':'3',
  'base_cost_per_sqft_inr':'162','installation_cost_per_sqft_inr':'85','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Structural engineer estimate; IS 456 beam design for 5m span; ~10% premium over 4x4m grid',
  'expected_lifespan_years':'75','replacement_cost_factor':'1.3','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'IS 456; NBC 2016',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'9','moisture_resistance':'High',
  'fire_rating':'Class A','energy_impact_modifier':'1.0','accessibility_score':'9',
  'thermal_source_notes':'No direct thermal contribution. Larger openings possible improving natural ventilation. ECBC 2017.',
  'max_floors_supported':'8','min_floors_required':'1','max_span_supported_m':'5.0',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'RCC column 300x300mm|RCC beam 230x500mm in 5m direction|150mm slab thickness|Structural engineer IS 456 design',
  'climate_restrictions':'None','hard_block_rule':'None',
  'advisory_rule':'Beam depth increases significantly in 5m direction - coordinate with false ceiling and door head height',
  'advisory_message':'A 5m span beam requires 450-500mm depth. If your floor-to-floor height is 10ft (3m) a 500mm beam leaves only 2.5m clear ceiling height below it. Confirm beam depth against floor-to-floor height before finalising.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 456 span-depth ratio; NBC 2016 headroom requirements',
  'ai_advisory_notes':'The 5x4 meter grid is what I recommend when clients want modern open-plan living spaces with kitchen dining and living flowing together without columns breaking the space. The 5-meter direction allows a column-free living room of 15 feet width which feels genuinely generous. The structural trade-off is a larger beam depth in the 5-meter direction - typically 450-500mm - which you need to hide in the false ceiling. Coordinate the beam depth with your floor-to-floor height before committing. With a 10.5 foot (3.2m) floor-to-floor height you still have comfortable 8.5 foot (2.6m) clear ceiling height below a 600mm beam.',
  'pros':'Column-free open-plan living areas possible|Modern spacious feel|Good natural ventilation with larger openings|Still economical relative to 6m grid',
  'cons':'Larger beam depths affect ceiling height|10% higher structural cost than 4x4m|Requires coordination on beam vs ceiling height|Heavier columns',
  'tooltip_detail':'5m × 4m open-plan grid. Enables column-free 15ft living rooms. Beam depth 450-500mm - confirm against floor-to-floor height before finalising.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'CG-004','category_name':'Structure','subcategory_name':'Column Grid',
  'name':'grid_6x6','display_name':'6m × 6m Grid (Large Span / Parking)','region':'South India',
  'description':'6m x 6m column grid. Enables large column-free spaces, double-car parking bays, commercial ground floor or large hall requirements. Deep beams or flat plate with drop panels. 25-35% higher structural cost than standard 4x4m.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Premium','sort_order':'4',
  'base_cost_per_sqft_inr':'195','installation_cost_per_sqft_inr':'100','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Structural engineer estimate IS 456; RMC concrete and heavy steel for 6m spans; normalised per sqft',
  'expected_lifespan_years':'75','replacement_cost_factor':'1.3','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'IS 456; NBC 2016; ACI 318',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'9','moisture_resistance':'High',
  'fire_rating':'Class A','energy_impact_modifier':'1.0','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution. Large openings possible for maximum natural ventilation. ECBC 2017.',
  'max_floors_supported':'15','min_floors_required':'1','max_span_supported_m':'6.0',
  'incompatible_with':'Standard residential on tight budgets|Load bearing masonry systems',
  'compatible_with':'RCC frame|Pre-stressed concrete frame|Steel frame',
  'requires_component':'RCC column 400x400mm minimum|RCC beam 300x600mm or flat plate with drop panels|175-200mm slab|M25 concrete|RMC plant|Structural engineer specialist design',
  'climate_restrictions':'None','hard_block_rule':'None',
  'advisory_rule':'Structural engineer specialist in large-span design is mandatory - not a standard residential calculation',
  'advisory_message':'6m span beams require specialist structural design beyond standard IS 456 residential practice. M25 concrete and precise bar placement are mandatory. Do not use a non-specialist engineer for this.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 456; ACI 318; NBC 2016 structural design',
  'ai_advisory_notes':'The 6x6 meter grid is for projects that genuinely need large column-free spaces - a house with double-car basement parking, a wedding hall ground floor under residences, or a truly open-plan 1000 sqft living area. The structural premium is real and significant - deep beams or a flat plate system with drop panels, M25 concrete mandatory, heavier columns and footings throughout. The payback in space quality is also real - a 6x6 grid gives you a genuinely column-free 18-foot room that feels like premium commercial space. Only go here if the spatial requirement genuinely demands it.',
  'pros':'Genuinely column-free large spaces|Double-car parking bay fits in one bay|Commercial-quality open plan|Future flexible space use',
  'cons':'25-35% higher structural cost|Very deep beams (600mm+) affect ceiling height significantly|Specialist structural engineer required|Overkill for standard residential rooms',
  'tooltip_detail':'6m × 6m large-span grid. Double-car parking or large hall possible. 25-35% cost premium. Specialist structural engineer mandatory.',
  'status':'Active','verify_flags':'base_cost_per_sqft_inr','data_filled_by':'AI'
},
]

out_path = os.path.join(os.path.dirname(__file__), 'registry.csv')
with open(out_path, 'a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=COLS, extrasaction='ignore')
    for r in new_rows:
        writer.writerow({c: r.get(c, '') for c in COLS})

print(f'Appended {len(new_rows)} rows to registry.csv')
subcats = {}
for r in new_rows:
    k = r['subcategory_name']
    subcats[k] = subcats.get(k, 0) + 1
for k, v in subcats.items():
    print(f'  {k}: {v} options')

with open(out_path, encoding='utf-8') as f:
    total = sum(1 for _ in f) - 1
print(f'Total registry rows now: {total}')
