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
  'component_id':'DPC-001','category_name':'Structure','subcategory_name':'Damp Proof Course',
  'name':'dpc_cement_mortar','display_name':'Cement Mortar DPC (1:3)','region':'South India',
  'description':'Damp Proof Course using 20mm thick cement mortar in 1:3 ratio (cement:sand) applied at plinth level. Standard economical DPC method widely used across South India for residential construction.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Basic','sort_order':'1',
  'base_cost_per_sqft_inr':'3','installation_cost_per_sqft_inr':'2','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Karnataka PWD SOR 2024-25 plastering rates; DPC application normalized per sqft of wall footprint',
  'expected_lifespan_years':'20','replacement_cost_factor':'0.8','major_maintenance_cycle_years':'20',
  'major_maintenance_cost_factor':'0.8','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'IS 3067; cement mortar DPC typical lifespan 15-25 years',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'6','moisture_resistance':'Medium',
  'fire_rating':'Class A','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'No significant thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All wall systems|All foundation types',
  'requires_component':'Cement OPC 43 or 53 grade|Clean river sand|Proper curing for 7 days',
  'climate_restrictions':'In very high rainfall areas (above 2500mm annual) or flood-prone plots upgrade to bituminous felt or polymer membrane.',
  'hard_block_rule':'None',
  'advisory_rule':'Apply while base concrete is green - not on dry hardened surface',
  'advisory_message':'Cement mortar DPC must be applied while the base concrete below is still slightly green (within 24-48 hours of pour) for good bond. Application on a dry dusty surface fails within a few years.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 3067; IS 2212',
  'ai_advisory_notes':'Cement mortar DPC is the standard choice for most residential construction in Karnataka and Tamil Nadu and it works adequately when applied correctly. The most common failure I see is contractors applying it on a dusty dry surface days after the base concrete has cured - the mortar then has no bond and peels away within a few monsoons allowing moisture to wick up the wall. The DPC must go down while the concrete below is still slightly green and the surface must be wetted and cleaned of dust before application. The 1:3 ratio is important - contractors sometimes use 1:4 or 1:5 to save cement and the result is a porous layer that does not stop moisture. For plots in normal rain zones with no flooding risk cement mortar DPC is the correct and economical choice.',
  'pros':'Lowest cost|Widely understood by all masons|Adequate for most South India plots|Easy repair if damaged',
  'cons':'Shorter lifespan than bituminous or polymer options|Less effective in flood-prone areas|Requires correct application timing for good bond|Degrades if repeatedly saturated',
  'tooltip_detail':'Standard cement mortar DPC. Apply on green concrete within 48 hours. Use 1:3 ratio only. Adequate for most residential plots.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'DPC-002','category_name':'Structure','subcategory_name':'Damp Proof Course',
  'name':'dpc_bituminous_felt','display_name':'Bituminous Felt DPC','region':'South India',
  'description':'Damp Proof Course using bitumen-impregnated hessian felt (Type 1 or Type 2 per IS 1322) sandwiched between cement mortar beds at plinth level. Better moisture barrier than plain cement mortar, moderate cost.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Intermediate','sort_order':'2',
  'base_cost_per_sqft_inr':'8','installation_cost_per_sqft_inr':'4','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'IS 1322 bitumen felt material cost; contractor application rate; Karnataka PWD SOR 2024-25 reference',
  'expected_lifespan_years':'30','replacement_cost_factor':'0.6','major_maintenance_cycle_years':'30',
  'major_maintenance_cost_factor':'0.6','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'IS 1322; bitumen felt lifespan 25-35 years in embedded condition',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'7','moisture_resistance':'High',
  'fire_rating':'Class B','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'No significant thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All wall systems|All foundation types',
  'requires_component':'IS 1322 Type 1 or Type 2 bitumen felt|Hot bitumen or cold bitumen adhesive|Cement mortar bed above and below',
  'climate_restrictions':'Good choice for high rainfall areas. For flood-prone plots with regular inundation upgrade to polymer membrane.',
  'hard_block_rule':'None',
  'advisory_rule':'Overlap felt sheets by minimum 100mm at joints',
  'advisory_message':'Bituminous felt sheets must overlap by minimum 100mm at all joints and the joint must be sealed with hot or cold bitumen adhesive. Gaps at joints create moisture entry points that defeat the DPC purpose.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 1322; IS 3067',
  'ai_advisory_notes':'Bituminous felt DPC is a meaningful upgrade over plain cement mortar and the cost difference is modest - maybe Rs 5-8 per sqft of wall length. The felt creates a genuine continuous impermeable barrier that cement mortar cannot match. The key to installation is overlapping the sheets by at least 100mm at every joint and sealing with bitumen adhesive because any gap will be found by capillary moisture within a few years. I recommend this option for any plot in a coastal or high-rainfall zone or where the finished floor level is less than 600mm above external ground. The typical lifespan is 25-35 years in embedded condition which covers most of the useful life of the building.',
  'pros':'Better moisture barrier than cement mortar|30-year lifespan|Moderate cost|Good for high-rainfall zones',
  'cons':'Higher cost than cement mortar DPC|Joint lapping and sealing critical|Not suitable for regularly flooded plots|Some fire rating reduction vs cement only',
  'tooltip_detail':'Bituminous felt DPC. Better than cement mortar. Overlap sheets 100mm minimum and seal joints with bitumen. Good for high-rainfall zones.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'DPC-003','category_name':'Structure','subcategory_name':'Damp Proof Course',
  'name':'dpc_polymer_membrane','display_name':'Polymer-Modified Membrane DPC','region':'South India',
  'description':'High-performance DPC using polymer-modified bitumen membrane (torch-applied or self-adhesive) at plinth level. Best moisture resistance available. Recommended for flood-prone plots, waterlogged sites, and premium construction.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Premium','sort_order':'3',
  'base_cost_per_sqft_inr':'18','installation_cost_per_sqft_inr':'8','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'STP/Fosroc/Pidilite polymer DPC membrane rates South India 2024; torch-applied; normalized per sqft of wall length',
  'expected_lifespan_years':'40','replacement_cost_factor':'0.5','major_maintenance_cycle_years':'40',
  'major_maintenance_cost_factor':'0.5','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'Polymer membrane DPC manufacturer warranty 15-25 years; practical lifespan 35-50 years embedded',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'9','moisture_resistance':'Very High',
  'fire_rating':'Class B','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'No significant thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All wall systems|All foundation types|Basement construction',
  'requires_component':'IS 16210 compliant polymer modified bitumen membrane|Torch or heat gun for application|Primer coat on concrete surface|Trained waterproofing applicator',
  'climate_restrictions':'Essential for flood-prone plots. Best choice for plots adjacent to lakes or rivers or in low-lying areas.',
  'hard_block_rule':'None',
  'advisory_rule':'Trained applicator required - torch-applied membrane needs certified installer',
  'advisory_message':'Torch-applied polymer membranes require a trained and experienced installer. Incorrect torch application causes membrane burning or inadequate bonding. Use a manufacturer-certified applicator.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 16210; manufacturer installation guidelines',
  'ai_advisory_notes':'Polymer modified membranes are the premium choice for DPC and for any plot that has even a moderate flood or waterlogging risk they are worth every rupee. The torch-applied APP or SBS membranes from brands like STP Fosroc or Pidilite create a seamless monolithic barrier that is genuinely impermeable and has flexibility to handle minor structural movement without cracking. The critical requirement is a trained applicator - this is not something an ordinary mason can do. The torch application temperature must be correct and the membrane must be fully bonded with no air bubbles or the moisture will find the void. For premium construction or any plot in a low-lying area I specify polymer membrane DPC automatically. The extra cost over cement mortar DPC is recovered in the first monsoon when your neighbours have rising damp and you do not.',
  'pros':'Best moisture resistance available|40-year lifespan|Essential for flood-prone plots|Handles minor structural movement without cracking|Seamless application',
  'cons':'Highest DPC cost|Requires trained torch applicator|Cannot be done by ordinary mason|Primer coat required before application',
  'tooltip_detail':'Polymer membrane DPC. Best protection available. Torch-applied by certified installer. Essential for flood-prone or low-lying plots.',
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
