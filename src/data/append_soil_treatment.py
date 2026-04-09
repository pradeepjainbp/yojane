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

# ── SOIL TREATMENT (Systems) ────────────────────────────────────────────────────
# Anti-termite and soil treatment beneath foundation and plinth
# Cost: INR per sqft of built-up area (ground floor footprint)
# 4 options: None → Chemical (pre-construction) → Reticulation pipes → Physical barrier
new_rows = [
{
  'component_id':'ST-001','category_name':'Systems','subcategory_name':'Soil Treatment',
  'name':'no_soil_treatment','display_name':'No Soil Treatment','region':'South India',
  'description':'No anti-termite soil treatment or physical barrier. Completely unprotected structure against subterranean termite attack. High risk in South India where termite activity is prevalent across all soil types.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Baseline','sort_order':'1',
  'base_cost_per_sqft_inr':'0','installation_cost_per_sqft_inr':'0','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'No capital cost.',
  'expected_lifespan_years':'0','replacement_cost_factor':'0','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'N/A - termite damage begins within 3-7 years without treatment in South India.',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'3','moisture_resistance':'High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'1.0','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'None',
  'climate_restrictions':'None',
  'hard_block_rule':'None',
  'advisory_rule':'Strongly not recommended in South India - termites are present in virtually all soil types',
  'advisory_message':'South India has among the highest termite activity in the world. Without pre-construction soil treatment subterranean termites typically establish colonies in wooden elements (door frames, furniture, roof timber) within 3-7 years. Remedial treatment after construction is 4-5x more expensive than pre-construction treatment.',
  'advisory_severity':'Strong-Warning','constraint_source_notes':'IS 6313 Part 2; NBC 2016; Pest Control India of India (PCAI) guidelines',
  'ai_advisory_notes':'I have never recommended skipping soil treatment to any client in South India and I never will. We have some of the most aggressive subterranean termite species in the world here - Odontotermes and Coptotermes can demolish door frames and wooden furniture within a few years of establishment. Pre-construction chemical treatment costs Rs 8000-15000 for a 1500 sqft house and is permanent for 10 years. Remedial treatment after the termites are already inside the walls costs Rs 40000-80000 and requires drilling through finished floors. There is no rational financial argument for skipping this.',
  'pros':'Zero upfront cost',
  'cons':'Termite damage almost certain within 5-10 years|Remedial cost 4-5x pre-construction treatment|Structural timber and door frames at risk|IS 6313 recommends treatment for all buildings',
  'tooltip_detail':'No soil treatment. Very high termite risk in South India. Pre-construction chemical treatment costs Rs 8000-15000. Remedial cost is 4-5x more. Do not skip.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'ST-002','category_name':'Systems','subcategory_name':'Soil Treatment',
  'name':'chemical_pre_construction','display_name':'Pre-Construction Chemical Soil Treatment','region':'South India',
  'description':'Chlorpyrifos or Bifenthrin emulsion injected and drenched into sub-grade soil, trench walls, backfill and plinth perimeter before PCC and foundation casting. IS 6313 Part 2 compliant. Standard anti-termite treatment.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Standard','sort_order':'2',
  'base_cost_per_sqft_inr':'8','installation_cost_per_sqft_inr':'4','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market rate licensed pest control operator; Karnataka PWD SOR 2024-25 anti-termite; normalised per sqft',
  'expected_lifespan_years':'10','replacement_cost_factor':'0.6','major_maintenance_cycle_years':'10',
  'major_maintenance_cost_factor':'0.50','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'IS 6313 Part 2; chemical efficacy 8-12 years depending on soil type and rainfall',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'7','moisture_resistance':'High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'1.0','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'Licensed pest control operator (PCO) with IS 6313 certification|Chlorpyrifos 1% or Bifenthrin 0.05% emulsion|Pump sprayer and injection rods|Treatment certificate for Occupancy Certificate',
  'climate_restrictions':'In very high rainfall zones (Kerala, Coastal Karnataka) chemical leaches faster through soil - re-treatment cycle is 7-8 years rather than 10.',
  'hard_block_rule':'None',
  'advisory_rule':'Treatment must be done by IS 6313 licensed PCO - certificate required for OC in most jurisdictions',
  'advisory_message':'Anti-termite treatment certificate from a licensed pest control operator is required for Occupancy Certificate in BBMP, GHMC and many South India municipal jurisdictions. Ensure treatment is done before PCC pouring.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 6313 Part 2; BBMP/GHMC building regulations; NBC 2016',
  'ai_advisory_notes':'Pre-construction chemical soil treatment is the most cost-effective anti-termite measure available. For Rs 8-15 per sqft you get 10 years of protection. The timing is critical - treatment must happen in four stages: excavation bottom, trench walls and backfill, top soil around plinth, and plinth area before PCC. Missing any stage leaves an entry point. Always use a licensed pest control operator with IS 6313 certification because the BBMP and most South India corporations require their certificate for the Occupancy Certificate. Chlorpyrifos is the most common active ingredient but Bifenthrin is now preferred by many operators as it is less toxic to humans while equally effective against termites.',
  'pros':'Lowest cost effective protection|10-year efficacy|IS 6313 compliant|Treatment certificate satisfies OC requirement',
  'cons':'Chemical treatment degrades over time - re-treatment at 10 years|Slight environmental concern with soil chemicals|Does not protect against aerial termites|Efficacy reduced in very high rainfall',
  'tooltip_detail':'Standard pre-construction chemical anti-termite treatment. IS 6313 compliant. Licensed PCO certificate needed for Occupancy Certificate.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'ST-003','category_name':'Systems','subcategory_name':'Soil Treatment',
  'name':'reticulation_pipe_system','display_name':'Reticulation Pipe Anti-Termite System','region':'South India',
  'description':'Perforated pipe network embedded in soil below foundation perimeter that allows repeated chemical injection from service points at ground level. Enables chemical renewal without excavation. For premium construction and high-risk termite zones.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Performance','sort_order':'3',
  'base_cost_per_sqft_inr':'18','installation_cost_per_sqft_inr':'8','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market rate Bayer Agenda Reticulation / Dow Sentricon; specialist PCO Bangalore/Chennai; normalised per sqft',
  'expected_lifespan_years':'30','replacement_cost_factor':'0.5','major_maintenance_cycle_years':'5',
  'major_maintenance_cost_factor':'0.30','annual_minor_maint_factor':'0.01','maintenance_complexity':'Medium',
  'lifecycle_source_notes':'IS 6313 Part 3; pipe system 30yr lifespan; chemical AMC contract 5yr renewal',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'8','moisture_resistance':'High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'1.0','accessibility_score':'9',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'Perforated HDPE pipe network below foundation perimeter|Service port injection points at plinth level|Annual maintenance contract with licensed PCO|Chemical injection pump',
  'climate_restrictions':'In high rainfall zones pipes must have check valves to prevent chemical dilution from groundwater intrusion.',
  'hard_block_rule':'None',
  'advisory_rule':'Sign Annual Maintenance Contract with licensed PCO at time of installation',
  'advisory_message':'Reticulation pipe systems only provide value if chemicals are refreshed every 5 years through the pipes. Without an AMC contract the pipes become useless after the initial chemical degrades.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 6313 Part 3; manufacturer maintenance protocol',
  'ai_advisory_notes':'Reticulation pipe systems are the intelligent upgrade for anyone who wants long-term termite protection without the disruption of excavating and re-treating every 10 years. The perforated HDPE pipe network is buried below the foundation perimeter during construction and service ports emerge at plinth level. When the chemical needs renewal you simply connect a pump to the service port and inject fresh chemical through the entire network without touching the finished flooring or landscaping. The annual maintenance contract is not optional - without it the system provides no benefit after the initial chemical degrades at 8-10 years.',
  'pros':'Chemical renewal without excavation or floor breaking|30-year pipe system lifespan|Renewable protection indefinitely|Ideal for high-value finished interiors',
  'cons':'Higher upfront cost than simple treatment|AMC contract ongoing cost|Requires periodic chemical injection|Needs specialist PCO for maintenance',
  'tooltip_detail':'Embedded pipe network for repeatable chemical injection. Never need to dig for re-treatment. AMC contract mandatory for long-term protection.',
  'status':'Active','verify_flags':'base_cost_per_sqft_inr','data_filled_by':'AI'
},
{
  'component_id':'ST-004','category_name':'Systems','subcategory_name':'Soil Treatment',
  'name':'physical_barrier_hdpe','display_name':'Physical Barrier (HDPE Sheet + Chemical)','region':'South India',
  'description':'Combination of HDPE physical barrier sheet beneath foundation slab and chemical treatment. HDPE sheet (0.5-1mm) blocks termite passage through the slab. Combined approach gives highest protection. Used in eco-conscious and high-risk construction.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Premium','sort_order':'4',
  'base_cost_per_sqft_inr':'28','installation_cost_per_sqft_inr':'12','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market rate HDPE termite barrier sheet + chemical treatment; specialist contractors; normalised per sqft',
  'expected_lifespan_years':'25','replacement_cost_factor':'0.5','major_maintenance_cycle_years':'10',
  'major_maintenance_cost_factor':'0.20','annual_minor_maint_factor':'0.005','maintenance_complexity':'Low',
  'lifecycle_source_notes':'IS 6313 Part 3; HDPE sheet 25yr lifespan; chemical component 10yr',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'9','moisture_resistance':'Very High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'1.0','accessibility_score':'9',
  'thermal_source_notes':'HDPE moisture barrier also reduces capillary damp rising through the slab - secondary benefit.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'0.5mm HDPE barrier sheet (full slab coverage)|Sealing tape at joints and penetrations|Pre-construction chemical treatment|Licensed PCO certification',
  'climate_restrictions':'In coastal areas HDPE barrier also provides additional protection against capillary moisture.',
  'hard_block_rule':'None',
  'advisory_rule':'All pipe and column penetrations through HDPE sheet must be sealed with manufacturer-specified sealant',
  'advisory_message':'Termites can penetrate HDPE barrier through any unsealed penetration point (pipes, columns, service entries). Every penetration must be sealed with the manufacturer specified collar and sealant.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 6313 Part 3; HDPE barrier installation guide',
  'ai_advisory_notes':'The physical HDPE barrier in combination with chemical treatment is the most thorough anti-termite system available for residential construction. The HDPE sheet is a genuine physical barrier that termites cannot chew through unlike chemical treatments which degrade over time. The combination of chemical treatment below the HDPE and physical blocking above creates a double barrier. The installation quality is critical - every pipe and column penetration through the sheet must be sealed with the manufacturer specified collar because termites will find any gap within a few years. This is the approach I recommend for eco-conscious clients who are uncomfortable with repeated chemical applications but still need robust termite protection.',
  'pros':'Physical barrier never degrades like chemicals|Combined system offers highest protection|HDPE also reduces capillary damp through slab|Long 25-year effective protection',
  'cons':'Higher cost than chemical only|HDPE joint and penetration sealing quality is critical|Requires careful installation coordination with foundation work|Cannot be added after foundation is cast',
  'tooltip_detail':'HDPE physical barrier + chemical. Dual protection. Highest termite resistance. All pipe penetrations through sheet must be sealed - termites find any gap.',
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
