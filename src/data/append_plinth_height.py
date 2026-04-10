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
  'component_id':'PLINTH-001','category_name':'Structure','subcategory_name':'Plinth Height',
  'name':'plinth_450mm','display_name':'450 mm (1.5 ft)','region':'South India',
  'description':'Plinth height of 450mm above external ground level. Suitable for gently sloped or well-drained level plots with no flooding history. Minimum typically allowed by most South India municipal codes.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Basic','sort_order':'1',
  'base_cost_per_sqft_inr':'8','installation_cost_per_sqft_inr':'5','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Karnataka PWD SOR 2024-25 filling and masonry rates; normalized per sqft of footprint',
  'expected_lifespan_years':'60','replacement_cost_factor':'0','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'Permanent structural element - no replacement cycle',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'6','moisture_resistance':'Low',
  'fire_rating':'Class A','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'None',
  'climate_restrictions':'Not recommended for high rainfall zones above 1500mm annual precipitation or low-lying areas.',
  'hard_block_rule':'None',
  'advisory_rule':'Verify no flooding history in last 20 years before accepting 450mm plinth',
  'advisory_message':'450mm plinth is only safe if the plot has confirmed good drainage and no flooding history. Check with neighbours and local records about waterlogging during heavy monsoon events.',
  'advisory_severity':'Warning','constraint_source_notes':'NBC 2016; Local municipal building regulations',
  'ai_advisory_notes':'Four fifty millimetres is the bare minimum I would accept for a plinth and only in very specific conditions - a plot with excellent drainage on gently sloping terrain in a city like Bangalore where the surrounding streets are well above the finished road level. In most South India contexts this height is too low. The problem is not the average monsoon but the extreme monsoon - in 2022 and 2015 Bangalore had rainfall events that flooded areas that had never flooded before and houses with 450mm plinths took water in while 600mm plinths were safe. Before accepting this height walk around your plot during heavy rain and check the drainage direction and ask your neighbours about the worst flooding they have seen.',
  'pros':'Lowest construction cost|Easiest access - fewer steps|Minimises filling material quantity',
  'cons':'Vulnerable to even moderate flooding|Not suitable for low-lying or high-rainfall areas|Difficult to raise later without major work',
  'tooltip_detail':'450mm plinth - minimum height. Only for well-drained level plots with confirmed no flooding history.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'PLINTH-002','category_name':'Structure','subcategory_name':'Plinth Height',
  'name':'plinth_600mm','display_name':'600 mm (2 ft)','region':'South India',
  'description':'Standard plinth height of 600mm above external ground level. Most common specification across Karnataka and Tamil Nadu for residential construction. Provides adequate protection against normal monsoon runoff and minor surface flooding.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Intermediate','sort_order':'2',
  'base_cost_per_sqft_inr':'12','installation_cost_per_sqft_inr':'7','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Karnataka PWD SOR 2024-25; standard residential specification; normalized per sqft',
  'expected_lifespan_years':'60','replacement_cost_factor':'0','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'Permanent structural element - no replacement cycle',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'7','moisture_resistance':'Medium',
  'fire_rating':'Class A','energy_impact_modifier':'0','accessibility_score':'9',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'None',
  'climate_restrictions':'Consider 750mm for high-rainfall zones above 2000mm annual precipitation.',
  'hard_block_rule':'None',
  'advisory_rule':'None','advisory_message':'','advisory_severity':'',
  'constraint_source_notes':'NBC 2016; BBMP/TNPCB building bylaws',
  'ai_advisory_notes':'Six hundred millimetres is the standard I specify for most residential plots in Bangalore Chennai and Hyderabad and it is the right default choice for any plot in a normal residential layout with good surrounding infrastructure. Two feet of clearance above external ground provides good protection against the sheet flow you get during a heavy monsoon hour. The vastu consideration is real - traditional Indian architecture always raised the plinth to symbolically separate the sacred interior from the external ground and practically to keep out insects and moisture. From a purely practical standpoint the 600mm plinth also gives you a useful visual base to the building and allows the DPC to function properly. The only reason to go lower is site access for elderly residents.',
  'pros':'Standard height for most South India conditions|Good monsoon protection|Acceptable by most municipal codes|Wide contractor familiarity',
  'cons':'Insufficient for flood-prone or low-lying plots|Creates access step for elderly/wheelchair users|More filling material than 450mm',
  'tooltip_detail':'600mm standard plinth. Best default for most South India plots. Upgrade to 750mm for high rainfall or low-lying areas.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'PLINTH-003','category_name':'Structure','subcategory_name':'Plinth Height',
  'name':'plinth_750mm','display_name':'750 mm (2.5 ft)','region':'South India',
  'description':'Elevated plinth of 750mm above external ground level. Recommended for flood-prone areas, low-lying plots, and zones with annual rainfall above 2000mm. Also specified for plots adjacent to water bodies or in areas with poor municipal drainage.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Performance','sort_order':'3',
  'base_cost_per_sqft_inr':'16','installation_cost_per_sqft_inr':'9','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Karnataka PWD SOR 2024-25; elevated plinth filling and masonry; normalized per sqft',
  'expected_lifespan_years':'60','replacement_cost_factor':'0','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'Permanent structural element - no replacement cycle',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'8','moisture_resistance':'High',
  'fire_rating':'Class A','energy_impact_modifier':'0','accessibility_score':'8',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'Well-compacted filling material|Steps or ramp for access',
  'climate_restrictions':'Recommended for plots in Kerala, coastal Karnataka and coastal Tamil Nadu where annual rainfall exceeds 2000mm.',
  'hard_block_rule':'None',
  'advisory_rule':'Provide steps or access ramp - 750mm requires at least 3 steps at entry',
  'advisory_message':'At 750mm plinth height, at least 3 steps are required at entry points. Design adequate landing areas for safety and consider a ramp for elderly residents.',
  'advisory_severity':'Warning','constraint_source_notes':'NBC 2016; IS 3764 accessibility',
  'ai_advisory_notes':'Seven fifty millimetres is my recommendation for any plot that shows even a hint of flooding risk or is in a high-rainfall coastal zone. The extra 150mm over the standard 600mm costs very little in absolute terms - maybe Rs 4-5 per sqft of footprint more - but gives you meaningful additional protection against that once-in-ten-years extreme rainfall event. I specifically recommend this for plots in Mangalore Udupi Kochi and the Kerala coast where heavy rain events routinely put 400-500mm of rain down in 24 hours and urban drainage systems cannot handle it. The access steps are a real consideration - three steps at 250mm each means you need a proper landing design. Include a ramp for elderly household members.',
  'pros':'Good protection against moderate flooding events|Recommended for coastal and high-rainfall zones|Better vastu compliance - elevated dignified entry|Reduces termite and insect access',
  'cons':'Requires 3+ entry steps - access challenge for elderly|More filling material and cost than 600mm|Taller compound wall needed at boundary',
  'tooltip_detail':'750mm elevated plinth. Recommended for coastal, high-rainfall zones and low-lying plots. Plan 3 access steps and ramp for elderly.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'PLINTH-004','category_name':'Structure','subcategory_name':'Plinth Height',
  'name':'plinth_900mm','display_name':'900 mm (3 ft)','region':'South India',
  'description':'High plinth of 900mm above external ground level. Required for heavily flood-prone plots, low-lying land near lakes or rivers, or areas with documented extreme flooding history. Maximum practical plinth height for residential construction.',
  'climate_zone':'Warm-Humid|Temperate','spectrum_position':'Premium','sort_order':'4',
  'base_cost_per_sqft_inr':'22','installation_cost_per_sqft_inr':'12','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Karnataka PWD SOR 2024-25; high plinth filling and masonry; normalized per sqft',
  'expected_lifespan_years':'60','replacement_cost_factor':'0','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'Permanent structural element - no replacement cycle',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'9','moisture_resistance':'Very High',
  'fire_rating':'Class A','energy_impact_modifier':'0','accessibility_score':'6',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'Well-compacted filling in 150mm lifts with plate compaction|Steps minimum 4|Ramp for wheelchair or elderly access',
  'climate_restrictions':'Primarily relevant for high-rainfall coastal zones and flood-prone areas.',
  'hard_block_rule':'None',
  'advisory_rule':'Mandatory ramp or step with handrail at all entry points for 900mm plinth',
  'advisory_message':'At 900mm (3 feet) a minimum of 4 steps are required. A proper handrail and preferably a ramp are mandatory for safety and elderly access. Design this into the site plan.',
  'advisory_severity':'Strong-Warning','constraint_source_notes':'NBC 2016; IS 3764',
  'ai_advisory_notes':'Nine hundred millimetres is the maximum practical plinth height for residential construction and I specify it only when the flooding risk is clearly documented and severe - plots adjacent to Bangalore lakes that overflowed in the 2022 floods plots near Chennai rivers in the Adyar basin or low-lying Kerala coastal plots with historical inundation. The practical challenge is access - four steps at 225mm is a significant climb and you absolutely must design a ramp for any elderly household member or future mobility needs. The compaction of filling material at this height is critical - if you fill loosely to 900mm and do not compact in 150mm lifts with a plate compactor the filling will settle over the first two monsoons and you will have a floor that slopes toward the walls causing serious dampness issues.',
  'pros':'Maximum flood protection for high-risk sites|Essential for documented flood-prone plots|Reduces all ground-borne moisture and pest risk',
  'cons':'Highest cost and filling material|Mandatory ramp for elderly access|Significant access steps|Compaction quality critical to prevent settlement',
  'tooltip_detail':'900mm maximum residential plinth. Only for documented flood-prone plots. Mandatory ramp for elderly. Compaction in 150mm lifts essential.',
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
