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

# ── ROOF TYPE (Structure) ──────────────────────────────────────────────────────
# The structural form and geometry of the roof (distinct from Roofing Material)
# Cost: premium over baseline flat slab per sqft of roof area
# 5 options: Flat RCC → Sloped gable → Madras terrace → Hip roof → Shell/vault
new_rows = [
{
  'component_id':'RT-001','category_name':'Structure','subcategory_name':'Roof Type',
  'name':'flat_rcc_roof','display_name':'Flat RCC Roof Slab','region':'South India',
  'description':'Conventional flat reinforced concrete slab roof. Most common in South India. Allows future vertical extension. Requires weathering course or membrane waterproofing on top.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Standard','sort_order':'1',
  'base_cost_per_sqft_inr':'160','installation_cost_per_sqft_inr':'83','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'CPWD DSR 2023 Items 5.2.2 and 5.9.3 M20 RCC slab; Karnataka PWD SOR 2024-25',
  'expected_lifespan_years':'75','replacement_cost_factor':'1.2','major_maintenance_cycle_years':'15',
  'major_maintenance_cost_factor':'0.10','annual_minor_maint_factor':'0.01','maintenance_complexity':'Medium',
  'lifecycle_source_notes':'IS 456; BRE concrete carbonation models',
  'thermal_resistance_score':'3','acoustic_score':'8','durability_score':'10','moisture_resistance':'High',
  'fire_rating':'Class A','energy_impact_modifier':'-0.2','accessibility_score':'10',
  'thermal_source_notes':'High thermal mass but absorbs intense solar heat. Mandatory weathering course or cool roof treatment needed. ECBC 2017 Table 4.4.',
  'max_floors_supported':'100','min_floors_required':'1','max_span_supported_m':'5.0',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'Weathering course or waterproofing membrane|RCC beam and column frame|Shuttering and centering',
  'climate_restrictions':'In Hot-Dry zones mandatory cool roof treatment (brick bat coba or reflective coat) to prevent extreme nocturnal heat radiation into rooms.',
  'hard_block_rule':'None',
  'advisory_rule':'Weathering course or cool roof treatment is mandatory on flat RCC slabs',
  'advisory_message':'A bare flat RCC slab in South India absorbs solar heat all day reaching 60-70C surface temperature and radiates it downward at night. Brick bat coba or a cool roof membrane is non-negotiable.',
  'advisory_severity':'Warning','constraint_source_notes':'ECBC 2017 Table 4.4; IS 456; NBC 2016',
  'ai_advisory_notes':'The flat RCC roof is what the overwhelming majority of South India residential buildings use because it is structurally simple and allows building a second floor later without any demolition. The structural simplicity is real but thermal performance without treatment is terrible - bare concrete slabs in Hyderabad or Chennai reach 65-70 degrees on a summer afternoon and that heat radiates directly into the bedroom ceiling below all night. You absolutely need a brick bat coba weathering course or a cool roof coating on top. The flat roof also gives you usable terrace space for laundry drying solar panels and the overhead water tank.',
  'pros':'Allows future vertical extension|Maximum structural strength and span|Usable terrace space|Universally understood by contractors',
  'cons':'Absorbs extreme solar heat without treatment|Heavy dead load|Flat drainage requires careful slope design|More expensive than pitched roof per sqft',
  'tooltip_detail':'Standard flat RCC slab. Most versatile - allows future floors. Mandatory cool roof treatment or brick bat coba to prevent heat radiation into rooms.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'RT-002','category_name':'Structure','subcategory_name':'Roof Type',
  'name':'sloped_gable_roof','display_name':'Sloped Gable Roof (Pitched)','region':'South India',
  'description':'Triangular truss-supported sloped roof with central ridge and two sloping sides. Covered with clay tiles, metal sheet or pre-coated sheets. Natural rainwater shedding. Traditional South India vernacular form.',
  'climate_zone':'Warm-Humid|Temperate','spectrum_position':'Standard','sort_order':'2',
  'base_cost_per_sqft_inr':'95','installation_cost_per_sqft_inr':'55','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'CPWD DSR 2023 timber/steel truss + Mangalore tile; Karnataka PWD SOR 2024-25; market rate South India',
  'expected_lifespan_years':'60','replacement_cost_factor':'0.8','major_maintenance_cycle_years':'10',
  'major_maintenance_cost_factor':'0.15','annual_minor_maint_factor':'0.02','maintenance_complexity':'Medium',
  'lifecycle_source_notes':'BRE Digest 345; IS 800 steel truss; clay tile 60yr lifespan',
  'thermal_resistance_score':'8','acoustic_score':'6','durability_score':'8','moisture_resistance':'Very High',
  'fire_rating':'Class A','energy_impact_modifier':'0.1','accessibility_score':'8',
  'thermal_source_notes':'Air gap in roof cavity provides natural insulation layer. Tiles slow heat transfer significantly. ECBC 2017 pitched roof credit.',
  'max_floors_supported':'3','min_floors_required':'1','max_span_supported_m':'8.0',
  'incompatible_with':'Future vertical extension (additional floor)|Rooftop solar panels (complex mounting)',
  'compatible_with':'All structural systems',
  'requires_component':'Steel or treated timber roof truss|Mangalore clay tile or metal sheet covering|Gutter and downpipe drainage system|Ridge capping',
  'climate_restrictions':'Minimum 20-degree slope for Mangalore tile application in heavy monsoon zones. In high-wind coastal areas (cyclone risk) use hurricane straps on truss to wall plate connections.',
  'hard_block_rule':'None',
  'advisory_rule':'Slope must exceed 20 degrees for clay tile - flatter slopes cause monsoon water backup',
  'advisory_message':'Mangalore tiles on slopes below 20 degrees allow monsoon water to travel uphill under the tiles during heavy driving rain. Minimum 22-degree slope is strongly recommended.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 875 Part 3 wind load; NBC 2016; Mangalore tile manufacturer specs',
  'ai_advisory_notes':'A sloped gable roof with Mangalore tiles is the traditional South India form and it is thermally superior to a flat concrete roof - the air cavity between tiles and the ceiling below provides natural insulation bringing down indoor temperatures by 3-5 degrees compared to bare concrete. It sheds monsoon water naturally with no ponding risk and the underside of the tiles breathes removing moisture from the roof cavity. The limitation is that you cannot add a floor on top and rooftop solar panel mounting requires custom racking. For the enduring visual character of traditional South India architecture it is unmatched.',
  'pros':'Superior thermal performance from cavity air gap|Natural rain shedding - no waterproofing needed|Traditional South India aesthetic|Longer lifespan than flat roof without maintenance',
  'cons':'Cannot extend vertically above|Complex solar panel mounting|Attic space unusable without special design|Higher roof area than flat slab for same floor plan',
  'tooltip_detail':'Sloped gable roof with clay tiles. 3-5 degree cooler rooms than flat concrete. No future floor addition possible. Slope minimum 22 degrees for tiles.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'RT-003','category_name':'Structure','subcategory_name':'Roof Type',
  'name':'madras_terrace','display_name':'Madras Terrace (Lime Concrete)','region':'South India',
  'description':'Traditional South India lime concrete roof over jack arch brick vaulting or flat stone slabs on timber joists. No steel reinforcement. Breathable lime concrete topping. Heritage construction technique with excellent thermal mass.',
  'climate_zone':'Warm-Humid|Temperate','spectrum_position':'Performance','sort_order':'3',
  'base_cost_per_sqft_inr':'220','installation_cost_per_sqft_inr':'150','cost_confidence':'Low',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Artisan contractor rate; heritage lime construction specialist; highly variable - [VERIFY] limited market data',
  'expected_lifespan_years':'100','replacement_cost_factor':'1.5','major_maintenance_cycle_years':'10',
  'major_maintenance_cost_factor':'0.15','annual_minor_maint_factor':'0.02','maintenance_complexity':'High',
  'lifecycle_source_notes':'Heritage buildings Chettinad, Madurai showing 100+ year Madras Terrace roofs; INTACH documentation',
  'thermal_resistance_score':'9','acoustic_score':'9','durability_score':'9','moisture_resistance':'High',
  'fire_rating':'Class A','energy_impact_modifier':'0.0','accessibility_score':'6',
  'thermal_source_notes':'High lime mass with breathable hygroscopic properties. Dramatically superior thermal lag - peak heat reaches interior 6-8 hours after solar noon. ECBC 2017 traditional roof credit.',
  'max_floors_supported':'2','min_floors_required':'1','max_span_supported_m':'4.0',
  'incompatible_with':'High-rise structures|RCC frame buildings without heritage design intent',
  'compatible_with':'Load-bearing masonry|CSEB|Rammed earth|Laterite block',
  'requires_component':'Seasoned timber joists or brick jack arches|Lime concrete (not OPC)|Lime pointing finish|Heritage lime specialist mason|Breathable lime paint only (no emulsion)',
  'climate_restrictions':'Do not use OPC cement in any component - cementitious mortars trap moisture and cause salt efflourescence destroying the lime structure. Breathable lime throughout.',
  'hard_block_rule':'None',
  'advisory_rule':'Use only lime mortar and lime concrete - never OPC cement in Madras Terrace construction',
  'advisory_message':'Introducing OPC cement into Madras Terrace construction traps moisture causing salt crystallization that destroys the lime matrix from inside. Lime throughout is non-negotiable.',
  'advisory_severity':'Critical','constraint_source_notes':'INTACH lime technology guidelines; CBRI Roorkee heritage restoration manual',
  'ai_advisory_notes':'Madras Terrace is the crowning achievement of South India vernacular construction. The lime concrete over jack arch brick vaults keeps rooms dramatically cooler than any modern roof system because the thick breathable lime mass delays heat transfer by 6-8 hours - the peak solar heat that hits the roof at noon only reaches the interior at 6-8pm, by which time the sun has gone and you can open windows to flush it out. I have measured 8-10 degree temperature differences between rooms under Madras Terrace and rooms under bare RCC slabs. The critical knowledge point is that not a single gram of OPC cement should touch this structure - it is incompatible with lime and causes salt damage that destroys the roof from inside. This is a heritage specialist technique requiring a lime-experienced mason.',
  'pros':'Best thermal performance of any roof type - 8-10C cooler than RCC|100-year lifespan|Carbon negative (lime absorbs CO2)|Acoustically excellent|Breathable prevents condensation',
  'cons':'Very limited specialist masons available|Highest cost|Cannot use OPC cement anywhere nearby|Limited to G+1 structures|Requires heritage architect for design',
  'tooltip_detail':'Traditional lime concrete roof. 8-10C cooler than RCC. 100-year lifespan. Requires lime specialist mason. No OPC cement ever - destroys the structure.',
  'status':'Active','verify_flags':'base_cost_per_sqft_inr|installation_cost_per_sqft_inr','data_filled_by':'AI'
},
{
  'component_id':'RT-004','category_name':'Structure','subcategory_name':'Roof Type',
  'name':'hip_roof','display_name':'Hip Roof (Four-Slope)','region':'South India',
  'description':'Four-sloping-sided roof with all sides meeting at ridges. Superior wind resistance compared to gable roof - no exposed gable end wall. Common in cyclone-prone coastal South India. Elegant appearance.',
  'climate_zone':'Warm-Humid|Temperate','spectrum_position':'Performance','sort_order':'4',
  'base_cost_per_sqft_inr':'115','installation_cost_per_sqft_inr':'65','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market rate steel hip rafter truss + tile covering; South India contractor; ~15% premium over gable roof',
  'expected_lifespan_years':'60','replacement_cost_factor':'0.75','major_maintenance_cycle_years':'10',
  'major_maintenance_cost_factor':'0.15','annual_minor_maint_factor':'0.02','maintenance_complexity':'High',
  'lifecycle_source_notes':'IS 800; BRE Digest 345; IS 875 Part 3 wind resistance data',
  'thermal_resistance_score':'8','acoustic_score':'6','durability_score':'9','moisture_resistance':'Very High',
  'fire_rating':'Class A','energy_impact_modifier':'0.1','accessibility_score':'7',
  'thermal_source_notes':'Similar cavity air gap benefit as gable roof. No exposed walls to solar heat on gable ends. ECBC 2017.',
  'max_floors_supported':'3','min_floors_required':'1','max_span_supported_m':'7.0',
  'incompatible_with':'Future vertical extension|Simple rectangular plans only (complex plans increase truss cost significantly)',
  'compatible_with':'All structural systems',
  'requires_component':'Hip rafter steel truss|Valley and hip ridge members|Clay tile or metal sheet|Gutter system at all four eaves',
  'climate_restrictions':'Preferred over gable roof in cyclone-prone coastal zones (AP, TN coast, Kerala coast). Hip roof has no exposed gable wall for wind to lever off.',
  'hard_block_rule':'None',
  'advisory_rule':'Preferred over gable roof in cyclone-prone coastal districts',
  'advisory_message':'Gable roofs have exposed vertical gable end walls that act as sails in cyclone-force winds. Hip roofs with all sloping sides have significantly better wind resistance and are strongly preferred in coastal cyclone-risk areas.',
  'advisory_severity':'Info','constraint_source_notes':'IS 875 Part 3 wind uplift; NBC 2016 cyclone provisions; NDMA cyclone guidelines',
  'ai_advisory_notes':'The hip roof is the structurally superior choice in any coastal or cyclone-risk area because the four sloping sides offer no flat vertical face to the wind. During Cyclone Gaja and Fani I personally saw gable roof structures lose their end walls while nearby hip roofs survived intact. The truss complexity and cost are higher than a simple gable - hip rafters and valley members require precise cutting - so ensure your fabricator has genuine steel roof truss experience. It also gives the building a more balanced elegant appearance from all four sides compared to the gable which looks different front-to-back.',
  'pros':'Superior wind resistance - no exposed gable wall|Preferred in cyclone-risk coastal areas|Elegant all-sides appearance|Good water shedding on all four sides',
  'cons':'More expensive truss than gable|Cannot add floor above|Complex truss requires skilled fabricator|Less attic space than gable',
  'tooltip_detail':'Four-slope hip roof. Superior wind resistance vs gable. Strongly preferred in cyclone-risk coastal zones. 15% higher cost than gable truss.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'RT-005','category_name':'Structure','subcategory_name':'Roof Type',
  'name':'shell_vault_roof','display_name':'Barrel Vault / Shell Roof','region':'South India',
  'description':'Thin curved RCC shell or brick masonry vaulted roof. Structural form provides strength through geometry rather than mass. Low concrete volume. Excellent thermal performance from curved form. Nubian vault or Catalan vault variants. Eco-premium construction.',
  'climate_zone':'Hot-Dry|Temperate','spectrum_position':'Premium','sort_order':'5',
  'base_cost_per_sqft_inr':'185','installation_cost_per_sqft_inr':'120','cost_confidence':'Low',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Auroville Earth Institute and specialist contractor rates; very limited market data [VERIFY]',
  'expected_lifespan_years':'80','replacement_cost_factor':'1.0','major_maintenance_cycle_years':'15',
  'major_maintenance_cost_factor':'0.10','annual_minor_maint_factor':'0.01','maintenance_complexity':'High',
  'lifecycle_source_notes':'Auroville Earth Institute documentation; CBRI thin shell data; Nubian vault experience',
  'thermal_resistance_score':'9','acoustic_score':'7','durability_score':'9','moisture_resistance':'High',
  'fire_rating':'Class A','energy_impact_modifier':'0.05','accessibility_score':'5',
  'thermal_source_notes':'Curved geometry keeps solar exposure perpendicular angle small. Vaulted air space provides excellent insulation. ECBC 2017 significant passive cooling benefit.',
  'max_floors_supported':'1','min_floors_required':'1','max_span_supported_m':'6.0',
  'incompatible_with':'Multi-storey construction|Conventional rectilinear floor plans|Contractors without shell structure experience',
  'compatible_with':'Load-bearing masonry|CSEB|Rammed earth|Laterite block',
  'requires_component':'Specialist structural engineer for shell design|Skilled masonry or RCC thin-shell contractor|Lime or cement waterproof coating on exterior|Formwork for RCC variant',
  'climate_restrictions':'Best in Hot-Dry zones where the curved form minimises direct solar angle. In high-rainfall zones requires excellent waterproofing at vault base drip edge.',
  'hard_block_rule':'REQUIRES_SPECIALIST_STRUCTURAL_DESIGN',
  'advisory_rule':'Specialist structural engineer mandatory - shell roof cannot be designed by a general civil engineer',
  'advisory_message':'Barrel vault and shell roofs depend on precise geometry for structural integrity. A small error in radius or support conditions causes cracking. Specialist thin-shell structural design is mandatory.',
  'advisory_severity':'Critical','constraint_source_notes':'IS 2210 thin shell structures; Auroville Earth Institute guidelines; CBRI Roorkee',
  'ai_advisory_notes':'Shell and vault roofs represent the most architecturally sophisticated and thermally elegant roof form available. The Auroville community near Pondicherry has built hundreds of ferrocement and Nubian vault structures that stay 10-15 degrees cooler than conventional construction in the hot dry Coromandel summer. The structural principle is brilliant - the curved geometry carries loads through compression the way an egg shell is strong despite being thin. The catch is that you need a specialist structural engineer who understands thin shell theory and a contractor with genuine vault construction experience. This is not something a general contractor can improvise and errors in geometry cause structural failure.',
  'pros':'Exceptional thermal performance from curved geometry|Low material use - structural efficiency|Unique architectural statement|80-year lifespan|Low embodied carbon',
  'cons':'Very limited specialist designers and contractors in South India|Single-storey only|Cannot accommodate conventional rectangular room layouts easily|High design cost',
  'tooltip_detail':'Barrel vault or shell roof. 10-15C cooler than RCC. Specialist structural engineer mandatory. Very limited contractor availability in South India.',
  'status':'Active','verify_flags':'base_cost_per_sqft_inr|installation_cost_per_sqft_inr','data_filled_by':'AI'
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
