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
  'component_id':'EXC-001','category_name':'Structure','subcategory_name':'Excavation Depth',
  'name':'excavation_600mm','display_name':'600 mm (2 ft)','region':'South India',
  'description':'Shallow excavation of 600mm depth. Suitable only where soil bearing capacity is confirmed adequate at this depth by soil investigation. Typically limited to soft-to-medium soils with very good bearing.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Basic','sort_order':'1',
  'base_cost_per_sqft_inr':'5','installation_cost_per_sqft_inr':'3','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Karnataka PWD SOR 2024-25 earthwork rates; normalized per sqft of footprint',
  'expected_lifespan_years':'60','replacement_cost_factor':'0','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'Foundation depth is permanent - no replacement cycle',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'5','moisture_resistance':'Medium',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'2','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'G+2 or above without soil test confirmation','compatible_with':'Strip foundation|Isolated footing',
  'requires_component':'Soil bearing capacity test (SBC) confirming adequacy at 600mm',
  'climate_restrictions':'Not suitable for expansive (black cotton) soils or waterlogged areas without additional investigation.',
  'hard_block_rule':'None',
  'advisory_rule':'Mandatory soil test before finalising at 600mm depth',
  'advisory_message':'600mm excavation is only safe if a soil bearing capacity test confirms adequate load-bearing at this depth. Assuming shallow depth without a test is a serious structural risk.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 1904; NBC 2016 Part 6',
  'ai_advisory_notes':'Six hundred millimetres is the minimum excavation depth I will ever accept and only when a proper soil test confirms good bearing capacity at that level. In South India we have significant variation in soil - the red laterite soils of coastal Karnataka and parts of Tamil Nadu can be quite competent at shallow depths but black cotton soil found in parts of the Deccan and north Karnataka swells and shrinks dramatically with moisture changes and you absolutely cannot use a shallow foundation there. Before you decide on excavation depth insist on a soil bearing capacity test from a geotechnical lab - it costs Rs 8000-15000 and tells you exactly where the firm strata is. Skipping this test to save money is how houses crack within five years.',
  'pros':'Lowest excavation cost|Faster foundation work|Less earthwork disposal',
  'cons':'Only suitable for sites with confirmed high SBC at shallow depth|Not suitable for G+2 and above without investigation|Risk of settlement if soil weakens with water',
  'tooltip_detail':'600mm excavation. Only for confirmed good bearing soils. Soil test mandatory before use.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'EXC-002','category_name':'Structure','subcategory_name':'Excavation Depth',
  'name':'excavation_900mm','display_name':'900 mm (3 ft)','region':'South India',
  'description':'Standard excavation depth of 900mm. Most appropriate for the majority of South India residential plots on medium-to-hard soils. This is the conventional default for G+1 to G+2 residential construction.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Intermediate','sort_order':'2',
  'base_cost_per_sqft_inr':'8','installation_cost_per_sqft_inr':'5','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Karnataka PWD SOR 2024-25 earthwork rates; standard residential depth; normalized per sqft',
  'expected_lifespan_years':'60','replacement_cost_factor':'0','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'Foundation depth is permanent - no replacement cycle',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'7','moisture_resistance':'Medium',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'3','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'Strip foundation|Isolated footing|Plinth beam',
  'requires_component':'Soil bearing capacity test recommended',
  'climate_restrictions':'May need increase in high-rainfall zones with water table within 600mm of surface.',
  'hard_block_rule':'None',
  'advisory_rule':'None',
  'advisory_message':'','advisory_severity':'','constraint_source_notes':'IS 1904; NBC 2016 Part 6',
  'ai_advisory_notes':'Nine hundred millimetres is the standard excavation depth that most good contractors in Bangalore Chennai and Hyderabad will quote by default and it is correct for most residential plots. The logic is simple - you want to get below the zone of seasonal moisture variation which in South India is typically 600-750mm and then another 150mm into undisturbed firm strata. For a G+1 house on ordinary red soil or medium-hard murrum this depth is sufficient. Where I see contractors cut corners is when they stop at 750mm and call it 900mm - measure it yourself with a plumb line. The other issue is that most contractors excavate and backfill with loose soil rather than properly compacted material which causes settlement. Insist on proper plate compaction testing at every 150mm lift of backfill.',
  'pros':'Standard depth for most South India soils|Good for G+1 to G+2 construction|Widely understood by all contractors|Economical',
  'cons':'May be insufficient for black cotton soils|Needs increase for G+3 and above|Water table depth must be checked',
  'tooltip_detail':'Standard 900mm excavation. Suitable for most South India residential plots. Confirm water table depth.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'EXC-003','category_name':'Structure','subcategory_name':'Excavation Depth',
  'name':'excavation_1200mm','display_name':'1200 mm (4 ft)','region':'South India',
  'description':'Deep excavation of 1200mm. Required for hard rocky strata encountered at depth, areas with high water table, or G+3 and above construction. Also appropriate for black cotton soil where deeper firm strata must be reached.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Performance','sort_order':'3',
  'base_cost_per_sqft_inr':'12','installation_cost_per_sqft_inr':'7','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Karnataka PWD SOR 2024-25 deep earthwork rates; normalized per sqft',
  'expected_lifespan_years':'60','replacement_cost_factor':'0','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'Foundation depth is permanent - no replacement cycle',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'8','moisture_resistance':'High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'5','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'Strip foundation|Isolated footing|Raft foundation',
  'requires_component':'Geotechnical soil investigation report|Dewatering pump if water table encountered',
  'climate_restrictions':'Essential in high water table areas and zones with seasonally waterlogged soils.',
  'hard_block_rule':'None',
  'advisory_rule':'Dewatering required if water table encountered during excavation',
  'advisory_message':'If water seeps into excavation at this depth, a dewatering pump is mandatory before concrete is poured. Pouring concrete into a water-filled trench is a critical structural failure.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 1904; IS 3955; NBC 2016',
  'ai_advisory_notes':'Twelve hundred millimetres is where you end up when the soil investigation reveals that the bearing stratum is deeper than expected or when you are building G+3 and above and need the extra embedment depth for load transfer. In many parts of interior Karnataka and Andhra the topsoil is soft for the first 600-800mm and then transitions to murrum or rock - in these cases going to 1200mm puts your foundation firmly in the competent layer. The critical issue at this depth is water. If your plot has a seasonal water table within one and a half metres of surface you will hit water during excavation and you must have a dewatering pump on site before you start. Pouring foundation concrete with water in the trench is one of the most serious construction defects I know.',
  'pros':'Reaches firm strata in most South India soil conditions|Suitable for G+3 and above|Good for high water table sites with dewatering|Black cotton soil management',
  'cons':'Higher excavation cost and time|Dewatering may be needed|More earthwork disposal|Requires equipment for deep cuts',
  'tooltip_detail':'1200mm deep excavation. For G+3 and above or deep bearing soils. Dewatering pump needed if water table is encountered.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'EXC-004','category_name':'Structure','subcategory_name':'Excavation Depth',
  'name':'excavation_1500mm','display_name':'1500 mm (5 ft)','region':'South India',
  'description':'Maximum standard excavation depth of 1500mm for residential construction. Required for deep bearing strata, very high water table zones, heavily loaded structures, or sites with highly compressible surface soils. Beyond this depth pile foundations are typically more economical.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Premium','sort_order':'4',
  'base_cost_per_sqft_inr':'18','installation_cost_per_sqft_inr':'10','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Karnataka PWD SOR 2024-25 deep earthwork + shoring rates; normalized per sqft',
  'expected_lifespan_years':'60','replacement_cost_factor':'0','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'Foundation depth is permanent - no replacement cycle',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'9','moisture_resistance':'High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'8','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'Raft foundation|Pile foundation|Isolated footing with plinth beam',
  'requires_component':'Detailed geotechnical investigation report|Dewatering system|Shoring or trench support for safety',
  'climate_restrictions':'Mandatory in waterlogged plots and low-lying areas with high groundwater.',
  'hard_block_rule':'None',
  'advisory_rule':'Trench safety shoring required at 1500mm depth per IS 3764',
  'advisory_message':'At 1500mm depth, excavation trench walls must be shored or battered per IS 3764 safety requirements. Unsupported vertical trenches at this depth are a collapse risk to workers.',
  'advisory_severity':'Strong-Warning','constraint_source_notes':'IS 1904; IS 3764; NBC 2016',
  'ai_advisory_notes':'At fifteen hundred millimetres you are at the limit of practical hand excavation and into territory where you need to seriously consider whether a pile foundation would be more economical. The main situations where I specify this depth are waterlogged plots near lakes or rivers in Bangalore and Chennai where the seasonal water table is high and you need to get well below it before encountering firm soil. At this depth you have mandatory safety requirements - IS 3764 requires either shoring the trench walls or battering them at a safe angle because unsupported vertical walls at 1.5m can collapse and kill workers. Always have dewatering in place before excavation begins and pour concrete the same day you reach formation level - do not leave an open 1.5m trench overnight.',
  'pros':'Reaches deepest firm strata|Best for heavily loaded structures|Essential for waterlogged plots|Maximum foundation stability',
  'cons':'Highest excavation cost|Mandatory shoring for worker safety|Dewatering essential|Consider pile foundation as alternative',
  'tooltip_detail':'1500mm deep excavation. Maximum standard residential depth. Trench shoring mandatory. Consider piles as alternative.',
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
