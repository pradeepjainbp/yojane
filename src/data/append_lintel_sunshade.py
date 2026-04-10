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

new_rows = [
{
  'component_id':'LINT-001','category_name':'Envelope','subcategory_name':'Lintel & Sunshade',
  'name':'lintel_rcc_only','display_name':'RCC Lintel Only','region':'South India',
  'description':'Standard RCC lintel beam above all window and door openings. Structural minimum requirement - transfers load around openings to adjacent wall panels. No solar shading element included.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Basic','sort_order':'1',
  'base_cost_per_sqft_inr':'5','installation_cost_per_sqft_inr':'3','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Karnataka PWD SOR 2024-25 RCC lintel rates; normalized per sqft of built-up area',
  'expected_lifespan_years':'60','replacement_cost_factor':'0','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'RCC lintel permanent structural element - same lifespan as structure',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'8','moisture_resistance':'Medium',
  'fire_rating':'Class A','energy_impact_modifier':'-0.05','accessibility_score':'10',
  'thermal_source_notes':'No solar shading. Windows receive full direct solar radiation. Increases cooling load.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All wall systems',
  'requires_component':'M20 concrete|Fe500 steel|Formwork',
  'climate_restrictions':'Not recommended as sole treatment in Hot-Dry or Warm-Humid climates - solar shading via chajja strongly advised.',
  'hard_block_rule':'None',
  'advisory_rule':'Add chajja (sunshade) for south and west facing windows in all South India climates',
  'advisory_message':'South and west facing windows without a chajja receive direct afternoon sun. This can increase indoor temperatures by 3-5°C and significantly increases AC loads in South Indian conditions.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 875 Part 3; ECBC 2017',
  'ai_advisory_notes':'RCC lintel is the structural minimum and every opening needs one regardless of what else you decide. But stopping at the lintel without a chajja in South India is a missed opportunity that you will pay for in AC bills for the life of the house. A window without a chajja on the south or west face in Bangalore receives approximately 4 hours of direct afternoon sun in summer. The glass conducts this heat directly into the living space. A 750mm chajja projection above the window blocks this direct sun while allowing diffuse daylight in. The payback on the additional chajja cost through AC savings is typically 4-6 years. I only accept lintel-only when the opening faces north where there is no direct solar gain problem.',
  'pros':'Lowest cost|Structural minimum requirement|Standard contractor knowledge',
  'cons':'No solar protection - maximum solar heat gain through windows|Higher cooling loads especially on west and south faces|Not recommended for energy-conscious design in South India',
  'tooltip_detail':'RCC lintel only. No solar shading. Add chajja for south and west facing windows to reduce cooling loads.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'LINT-002','category_name':'Envelope','subcategory_name':'Lintel & Sunshade',
  'name':'lintel_with_chajja','display_name':'Lintel + Sunshade (Chajja)','region':'South India',
  'description':'RCC lintel beam with integral or separately cast chajja (sunshade) projecting 450-750mm above the window. Reduces direct solar radiation through glass on south and west faces. Standard recommended specification for South India construction.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Intermediate','sort_order':'2',
  'base_cost_per_sqft_inr':'10','installation_cost_per_sqft_inr':'6','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Karnataka PWD SOR 2024-25 RCC lintel + chajja rates; 600mm projection standard; normalized per sqft',
  'expected_lifespan_years':'60','replacement_cost_factor':'0','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0.002','maintenance_complexity':'Low',
  'lifecycle_source_notes':'RCC chajja permanent element - same lifespan as structure with minimal maintenance',
  'thermal_resistance_score':'6','acoustic_score':'5','durability_score':'8','moisture_resistance':'High',
  'fire_rating':'Class A','energy_impact_modifier':'0.1','accessibility_score':'10',
  'thermal_source_notes':'600mm chajja projection blocks direct summer sun on south face. Reduces solar heat gain by 15-25% for south-facing windows.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All wall systems|All window types',
  'requires_component':'M20 concrete|Fe500 steel|Waterproofing on top surface of chajja|Drip groove at tip',
  'climate_restrictions':'Recommended for all South India climates. Most important for south and west facing openings.',
  'hard_block_rule':'None',
  'advisory_rule':'Drip groove at chajja tip mandatory to prevent water tracking back under chajja to wall',
  'advisory_message':'A chajja without a drip groove (notch) at the tip will allow rain water to track back along the soffit to the wall surface causing dampness and staining below the opening.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 875 Part 3; ECBC 2017; NBC 2016',
  'ai_advisory_notes':'The chajja is one of the most cost-effective passive cooling elements in South India architecture and it has been used for centuries for exactly this reason. A 600mm projection above a south-facing window blocks the high summer sun angle completely while allowing diffuse skylight in through the full window. The detail that every contractor gets wrong is the drip groove - you need a 10-15mm V-groove cut on the underside of the chajja approximately 50mm from the tip so that rain water hitting the top of the chajja drips cleanly to the ground rather than tracking back along the soffit and staining the wall below the window. Also waterproof the top surface of the chajja with two coats of polymer cementitious waterproofing because it is a horizontal slab fully exposed to rain and the standing water will penetrate unprotected concrete and cause spalling within 5-10 years.',
  'pros':'15-25% solar heat gain reduction on south/west faces|Protects window from direct rain reducing weathering|Traditional South India climate-appropriate design|Good payback through reduced AC loads|Permanent no-maintenance element',
  'cons':'Additional cost over lintel only|Slightly increases shadow on garden in winter|Poor installation common - enforce drip groove and waterproofing|Wrong orientation gives little benefit',
  'tooltip_detail':'Lintel + chajja sunshade. Standard South India specification. Drip groove mandatory. Waterproof top surface.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'LINT-003','category_name':'Envelope','subcategory_name':'Lintel & Sunshade',
  'name':'lintel_band_deep_chajja','display_name':'Band Beam + Deep Extended Chajja','region':'South India',
  'description':'Continuous horizontal RCC band beam at sill or lintel level combined with extended 900mm+ chajja projection. Provides maximum solar shading, structural rigidity, and a distinctive horizontal banding aesthetic. Used in energy-efficient and architect-designed construction.',
  'climate_zone':'Hot-Dry|Warm-Humid','spectrum_position':'Premium','sort_order':'3',
  'base_cost_per_sqft_inr':'18','installation_cost_per_sqft_inr':'10','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'RCC band beam + extended chajja contractor rates Bangalore 2024; normalized per sqft',
  'expected_lifespan_years':'60','replacement_cost_factor':'0','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0.002','maintenance_complexity':'Low',
  'lifecycle_source_notes':'RCC band and chajja permanent element - lifespan equals structure',
  'thermal_resistance_score':'8','acoustic_score':'5','durability_score':'9','moisture_resistance':'High',
  'fire_rating':'Class A','energy_impact_modifier':'0.2','accessibility_score':'10',
  'thermal_source_notes':'900mm+ chajja eliminates direct solar gain through windows in all South India latitudes for 80% of daylight hours in summer. Best passive cooling element for facades.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All wall systems|Energy-efficient design|IGBC Green Homes compliance',
  'requires_component':'M20+ concrete|Fe500D steel|Waterproofing on chajja top|Drip groove|Structural engineer approval for cantilever',
  'climate_restrictions':'Highest value in Hot-Dry zones. Also very effective in Warm-Humid coastal zones.',
  'hard_block_rule':'None',
  'advisory_rule':'Structural engineer must verify cantilever design for deep chajja projection beyond 750mm',
  'advisory_message':'A chajja projecting more than 750mm requires structural engineer verification of the cantilever design, reinforcement sizing, and connection to the band beam. Do not rely on rule of thumb for projections beyond this.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 456; IS 875 Part 3; ECBC 2017',
  'ai_advisory_notes':'The continuous band beam with deep chajja is the element I specify for any architect-designed energy-efficient house in South India and it serves double duty - structural and environmental. As a structural element the continuous band beam ties the masonry together at window lintel level significantly improving seismic performance of the wall by creating a stiff horizontal diaphragm. As an environmental element a 900mm+ chajja projection essentially eliminates direct solar gain through the window for most of the day in summer at South India latitudes between 8 and 18 degrees north. The shade angle calculation confirms that a 900mm projection on a wall at 12 degrees north latitude blocks the sun for approximately 8 out of 10 hours of peak summer radiation. The structural engineer must verify the cantilever design for projections beyond 750mm - the reinforcement at the root of the chajja carries high bending moment and this is not something to leave to the contractor to figure out.',
  'pros':'Maximum solar shading - eliminates direct solar gain|Structural benefit of continuous band beam|Improved seismic performance|Distinctive horizontal banding aesthetic|Best passive cooling element available|IGBC and ECBC compliance pathway',
  'cons':'Highest cost|Structural engineer design required for deep projection|Reduces visible sky from inside|Some perceived loss of view through window|More complex formwork',
  'tooltip_detail':'Band beam + 900mm+ chajja. Maximum solar protection. Structural engineer required for cantilever. Best passive cooling element.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
]

out_path = os.path.join(os.path.dirname(__file__), 'registry.csv')
with open(out_path, 'a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=COLS, extrasaction='ignore')
    for r in new_rows:
        writer.writerow({c: r.get(c, '') for c in COLS})

print(f'Appended {len(new_rows)} rows to registry.csv')
for r in new_rows:
    print(f'  {r["component_id"]} — {r["display_name"]}')
with open(out_path, encoding='utf-8') as f:
    total = sum(1 for _ in f) - 1
print(f'Total registry rows now: {total}')
