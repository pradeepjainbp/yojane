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
  'component_id':'PARA-001','category_name':'Envelope','subcategory_name':'Parapet',
  'name':'parapet_brick_masonry','display_name':'Brick Masonry Parapet','region':'South India',
  'description':'Traditional brick masonry parapet wall at roof edge, typically 600-900mm high, plastered and painted. Economical, durable, and maintenance-free. Most common parapet in South India residential construction.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Basic','sort_order':'1',
  'base_cost_per_sqft_inr':'6','installation_cost_per_sqft_inr':'4','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Karnataka PWD SOR 2024-25 parapet masonry rates; normalized per sqft of roof perimeter per metre height',
  'expected_lifespan_years':'40','replacement_cost_factor':'0.5','major_maintenance_cycle_years':'15',
  'major_maintenance_cost_factor':'0.15','annual_minor_maint_factor':'0.01','maintenance_complexity':'Low',
  'lifecycle_source_notes':'IS 1905; masonry parapet lifespan data',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'7','moisture_resistance':'Medium',
  'fire_rating':'Class A','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'Parapet provides minimal thermal benefit but shades roof edge.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'Flat RCC roof|All roof systems with flat section',
  'requires_component':'Coping slab or coping tile on top of parapet|Waterproofing at parapet-roof junction|Movement joint at parapet-roof slab connection',
  'climate_restrictions':'In high-rainfall zones coping slab with 40mm overhang essential to prevent water ingress at parapet base.',
  'hard_block_rule':'None',
  'advisory_rule':'Coping slab with drip groove mandatory on top of parapet and waterproofing at parapet-slab junction',
  'advisory_message':'The junction between parapet and roof slab is the most common source of roof leaks in South India. This junction must have flexible waterproofing that can accommodate thermal movement and the parapet top must have a coping slab with drip groove.',
  'advisory_severity':'Strong-Warning','constraint_source_notes':'IS 1905; NBC 2016',
  'ai_advisory_notes':'Brick masonry parapets are the default and they work well when two critical details are done correctly. First the coping - the top of the parapet is fully exposed to sun and rain and must have a RCC or stone coping slab with a 40mm overhang and drip groove on each side to prevent water from running down the parapet face and soaking into the joint between parapet and roof. Second the junction waterproofing - the right angle between the parapet base and the roof slab is under high thermal stress and cracks within a few years without a flexible waterproofing membrane that bridges this joint with a 150mm fillet. Both details are routinely skipped by contractors and both cause the majority of roof leaks I am called to investigate. Specify these details clearly in your drawings and check that they are done.',
  'pros':'Most economical parapet|Maintenance-free once plastered|Familiar to all masons|Privacy screen function',
  'cons':'Junction waterproofing critical - often poorly done|Coping slab detail important|Adds dead load to roof slab|Blocks rooftop views',
  'tooltip_detail':'Brick parapet. Coping slab and parapet-slab junction waterproofing are critical details - most common source of roof leaks.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'PARA-002','category_name':'Envelope','subcategory_name':'Parapet',
  'name':'parapet_rcc','display_name':'RCC Parapet','region':'South India',
  'description':'Reinforced concrete parapet cast as continuation of roof slab edge. Stronger and more durable than brick masonry parapet. Better resistance to seismic loads and wind. Standard for premium construction and multi-storey buildings.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Intermediate','sort_order':'2',
  'base_cost_per_sqft_inr':'10','installation_cost_per_sqft_inr':'6','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'RCC parapet contractor rates Bangalore/Chennai 2024; normalized per sqft of roof perimeter',
  'expected_lifespan_years':'60','replacement_cost_factor':'0.3','major_maintenance_cycle_years':'25',
  'major_maintenance_cost_factor':'0.08','annual_minor_maint_factor':'0.005','maintenance_complexity':'Low',
  'lifecycle_source_notes':'IS 456; RCC parapet lifespan equals structure',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'9','moisture_resistance':'High',
  'fire_rating':'Class A','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'Dense RCC parapet has high thermal mass - minor benefit.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'Flat RCC roof|All roof systems with flat section',
  'requires_component':'M20 concrete|Fe500 steel|Waterproofing at parapet-slab junction|Expansion joint at corners',
  'climate_restrictions':'None',
  'hard_block_rule':'None',
  'advisory_rule':'Expansion joint at parapet corners and mid-span mandatory to prevent cracking',
  'advisory_message':'RCC parapets experience significant thermal expansion and must have expansion joints at corners and at not more than 6m spacing. Without these joints cracks develop at the corners within 2-3 monsoon seasons.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 456; NBC 2016',
  'ai_advisory_notes':'RCC parapets are my specification for premium construction because they are monolithic with the roof slab edge making waterproofing at the junction far easier to achieve than with brick masonry which has an inherent bond line at the slab surface. The critical detail that is almost universally skipped is the expansion joint. An RCC parapet running 10-15 metres without an expansion joint will crack at the corners every time because concrete expands and contracts significantly with the 40-50 degree temperature swings a Bangalore or Chennai roof experiences between winter night and summer afternoon. Place a 10-12mm expansion joint with flexible sealant at every corner and at mid-span of runs longer than 6 metres. Waterproof the junction between parapet and roof with the same treatment as the rest of the roof - this is now a seamless concrete joint rather than a brick-to-slab interface which is a significant advantage.',
  'pros':'Stronger than brick parapet|Better seismic and wind resistance|Monolithic with roof slab - easier waterproofing|60-year lifespan|Clean modern aesthetic',
  'cons':'Higher cost than brick parapet|Expansion joints at corners mandatory|More complex formwork|Cracking at corners if expansion joints omitted',
  'tooltip_detail':'RCC parapet. Stronger and more durable. Expansion joints at corners mandatory. Monolithic waterproofing advantage over brick.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'PARA-003','category_name':'Envelope','subcategory_name':'Parapet',
  'name':'parapet_metal_railing','display_name':'Metal Railing (Open Parapet)','region':'South India',
  'description':'Fabricated metal railing at roof edge instead of solid masonry parapet. MS or stainless steel posts with horizontal rails or glass infill. Open and modern aesthetic. Requires RCC edge beam as base. Standard for contemporary and architect-designed construction.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Performance','sort_order':'3',
  'base_cost_per_sqft_inr':'14','installation_cost_per_sqft_inr':'7','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'MS railing fabrication rates Bangalore 2024; powder coat finish; normalized per sqft of roof perimeter',
  'expected_lifespan_years':'25','replacement_cost_factor':'0.8','major_maintenance_cycle_years':'8',
  'major_maintenance_cost_factor':'0.3','annual_minor_maint_factor':'0.02','maintenance_complexity':'Medium',
  'lifecycle_source_notes':'MS railing coating lifespan 8-12 years; SS railing 25+ years',
  'thermal_resistance_score':'5','acoustic_score':'3','durability_score':'6','moisture_resistance':'Medium',
  'fire_rating':'Class A','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'Open railing allows free air circulation over roof - minor cooling benefit.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'Flat RCC roof|RCC edge beam|Contemporary architecture',
  'requires_component':'RCC edge beam at roof perimeter (mandatory structural base)|MS or SS posts with anchor bolts into edge beam|Powder coat or galvanising for MS|Edge waterproofing detail',
  'climate_restrictions':'In coastal zones within 5km of sea use 316-grade stainless steel only - MS railings corrode within 5 years in salt air.',
  'hard_block_rule':'None',
  'advisory_rule':'Use SS 316 railing within 10km of coastline - MS corrodes in salt air within 5 years',
  'advisory_message':'MS railings in coastal zones corrode rapidly due to salt air. Use 316-grade stainless steel for any railing within 10km of the coast. The cost premium over MS is significant but replacement cost is far higher.',
  'advisory_severity':'Warning','constraint_source_notes':'NBC 2016 Section 2 safety; IS 1161 structural tubes',
  'ai_advisory_notes':'Metal railings give a contemporary open look and are popular in architect-designed homes but they require much more maintenance than solid parapets. Powder-coated MS railing starts to show corrosion at the welds and base plates within 5-8 years in a typical South India climate and needs repainting. In coastal areas it is useless within 3 years unless you use marine-grade 316 stainless steel which is very expensive. The structural base is critical - the railing posts must anchor into a properly designed RCC edge beam not just drilled into the roof slab. I also always require a solid masonry kickboard at the base minimum 200mm high because the open railing allows objects to slide off the roof edge which is a serious safety hazard especially for children. If you choose this aesthetic understand the ongoing maintenance commitment - it is not a set-and-forget specification.',
  'pros':'Open modern aesthetic|Better natural ventilation over roof|Clear views from rooftop|Lighter than solid parapet',
  'cons':'Highest maintenance requirement - repainting every 5-8 years|Corrosion in coastal zones - SS 316 required|Less privacy than solid parapet|Objects can fall through - safety concern|RCC edge beam mandatory',
  'tooltip_detail':'Metal railing parapet. Modern aesthetic but highest maintenance. Use SS 316 near coast. RCC edge beam mandatory base.',
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
