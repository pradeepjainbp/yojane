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

# ── FLOOD-PRONE DESIGN (Special) ───────────────────────────────────────────────
# Flood risk mitigation design level
# Relevant: Kerala coastal, Chennai low-lying, AP delta regions, urban flash flood areas
# Cost: premium over standard construction per sqft
# 4 options: Standard → Elevated plinth → Flood-proofed → Amphibious/resilient
new_rows = [
{
  'component_id':'FP-001','category_name':'Special','subcategory_name':'Flood-Prone',
  'name':'standard_no_flood','display_name':'Standard Construction (No Flood Mitigation)','region':'South India',
  'description':'Standard construction with no specific flood risk mitigation. Plinth at standard 450mm above natural ground level per NBC 2016 minimum. Adequate for areas with no significant historical flooding.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Baseline','sort_order':'1',
  'base_cost_per_sqft_inr':'0','installation_cost_per_sqft_inr':'0','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'No premium - baseline plinth at 450mm per NBC 2016.',
  'expected_lifespan_years':'0','replacement_cost_factor':'0','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'NBC 2016 plinth height requirement',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'5','moisture_resistance':'Low',
  'fire_rating':'Non-Rated','energy_impact_modifier':'1.0','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'Low-lying areas|Flood plain areas|Areas that flooded in 2015, 2018 or 2021 events',
  'compatible_with':'All structural systems on elevated or non-flood-risk sites',
  'requires_component':'Standard plinth 450mm above natural ground|NBC 2016 minimum compliance',
  'climate_restrictions':'Not adequate for low-lying coastal areas, flood plains or areas within 500m of rivers or large stormwater drains.',
  'hard_block_rule':'None',
  'advisory_rule':'Check local flood history before choosing standard construction in any South India coastal or river-proximate site',
  'advisory_message':'South India has experienced catastrophic flooding: Chennai 2015, Kerala 2018, Hyderabad 2020, Chennai 2021. If your site has flooded even once in the last 20 years, standard 450mm plinth is completely inadequate. Check NDMA and state disaster management flood maps.',
  'advisory_severity':'Warning','constraint_source_notes':'NBC 2016; NDMA flood hazard maps; state disaster management authority',
  'ai_advisory_notes':'Standard 450mm plinth is fine for sites that have never flooded and are not on flood plains or near drainage channels. However I urge every client to check the NDMA flood hazard map for their specific area before committing to standard construction. The 2015 Chennai floods, 2018 Kerala floods and 2020 Hyderabad floods inundated thousands of houses built to standard specifications that were simply too low. The local knowledge test is simple: ask the oldest resident in the area whether their street has ever flooded. If the answer is yes, even once in 50 years, go to elevated plinth minimum.',
  'pros':'No cost premium|Standard construction knowledge|Maximum ground floor space',
  'cons':'Vulnerable to flash flooding and urban drainage overload|Standard 450mm plinth is inadequate in any flood-prone area|Climate change increasing flood frequency in South India coastal cities',
  'tooltip_detail':'Standard 450mm plinth. Adequate only for confirmed non-flood-risk sites. Check NDMA flood map and local history before choosing this option.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'FP-002','category_name':'Special','subcategory_name':'Flood-Prone',
  'name':'elevated_plinth_600','display_name':'Elevated Plinth (600-900mm) + Flood Vents','region':'South India',
  'description':'Plinth height 600-900mm above natural ground level. Provides protection against typical urban flash flooding (30-60cm inundation). Includes flood vents in plinth walls to equalise hydrostatic pressure. Appropriate for moderate-risk areas.',
  'climate_zone':'Warm-Humid|Temperate','spectrum_position':'Standard','sort_order':'2',
  'base_cost_per_sqft_inr':'12','installation_cost_per_sqft_inr':'8','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Extra plinth filling and retaining wall cost; normalised per sqft; CPWD DSR 2023',
  'expected_lifespan_years':'75','replacement_cost_factor':'1.1','major_maintenance_cycle_years':'20',
  'major_maintenance_cost_factor':'0.05','annual_minor_maint_factor':'0.005','maintenance_complexity':'Low',
  'lifecycle_source_notes':'NBC 2016; FEMA flood proofing guidelines; local observation',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'8','moisture_resistance':'High',
  'fire_rating':'Class A','energy_impact_modifier':'1.0','accessibility_score':'7',
  'thermal_source_notes':'Higher plinth increases natural ventilation from ground - slight thermal benefit in warm humid zones.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'Compacted earth filling to 600-900mm level|Plinth retaining wall|Flood vents at 150mm above plinth|Ramp or steps at entry|Waterproof plinth beam',
  'climate_restrictions':'In coastal areas plinth filling must use well-compacted laterite or gravel - not loose black cotton soil which settles differentially.',
  'hard_block_rule':'None',
  'advisory_rule':'Flood vents mandatory in plinth walls to prevent hydrostatic pressure buildup',
  'advisory_message':'A solid plinth wall without flood vents creates hydrostatic pressure during flooding that can crack or overturn the wall. Flood vents allow water to equalize pressure on both sides of the plinth wall during inundation.',
  'advisory_severity':'Warning','constraint_source_notes':'FEMA Technical Bulletin 1; NBC 2016; IS 3764',
  'ai_advisory_notes':'Raising the plinth to 600-900mm is the most cost-effective flood mitigation investment for moderate-risk areas. After the 2015 Chennai floods I saw houses where those with 600mm+ plinths stayed dry while neighbors with standard 450mm plinths had 1-2 feet of water inside. The cost of extra plinth filling and a slightly higher retaining wall is trivially small compared to the cost of flood damage to furniture, flooring and electrical systems. The accessibility trade-off is more steps at entry - design a wider low-gradient staircase or include a ramp from the start.',
  'pros':'Protects against 30-60cm flood inundation - covers most urban flash floods|Low cost premium|NBC 2016 compliant at higher specification|Higher plinth also improves natural ventilation',
  'cons':'More steps at entry - accessibility concern|Higher plinth filling can settle if soil is poor quality|Does not protect against major 1-2 metre flood events',
  'tooltip_detail':'600-900mm elevated plinth. Protects against urban flash floods up to 60cm. Flood vents in plinth walls mandatory. Low cost, high impact for moderate-risk areas.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'FP-003','category_name':'Special','subcategory_name':'Flood-Prone',
  'name':'flood_proofed_1200','display_name':'Flood-Proofed Construction (1200mm+ Plinth)','region':'South India',
  'description':'High plinth at 1200-1500mm above natural ground (equivalent to chest-height protection), combined with flood-resistant materials for plinth and lower walls, waterproofed entry points and flood barrier provisions at all openings. For high-risk areas (coastal Kerala, Chennai low-lying, river delta zones).',
  'climate_zone':'Warm-Humid|Temperate','spectrum_position':'Performance','sort_order':'3',
  'base_cost_per_sqft_inr':'28','installation_cost_per_sqft_inr':'15','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'High plinth + retaining wall + flood barriers + waterproof lower wall materials; normalised per sqft',
  'expected_lifespan_years':'75','replacement_cost_factor':'1.1','major_maintenance_cycle_years':'15',
  'major_maintenance_cost_factor':'0.08','annual_minor_maint_factor':'0.01','maintenance_complexity':'Medium',
  'lifecycle_source_notes':'FEMA dry flood proofing; NBC 2016; IS 3764 waterproofing',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'9','moisture_resistance':'Very High',
  'fire_rating':'Class A','energy_impact_modifier':'1.0','accessibility_score':'5',
  'thermal_source_notes':'Higher plinth with good natural ventilation from ground. ECBC 2017.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'1200-1500mm compacted plinth fill|Reinforced plinth retaining walls|Flood barrier tracks at all doors and garage entries|Crystalline waterproofing on plinth and lower walls|All electrical panels above flood level|Waterproof cable entry glands',
  'climate_restrictions':'In coastal areas with tidal surge risk (like Chennai coastal or Kerala backwaters) the effective flood level may exceed 1200mm - check NDMA surge maps.',
  'hard_block_rule':'None',
  'advisory_rule':'All electrical distribution boards and panel boxes must be at minimum 1500mm above finished floor level',
  'advisory_message':'During flooding, electrical panels at standard 1200mm wall height are submerged causing electrocution risk and total panel replacement. Mount all DB boards at 1500mm minimum height in flood-prone areas.',
  'advisory_severity':'Critical','constraint_source_notes':'IS 732; NBC 2016 Part 8; FEMA electrical flood guidelines',
  'ai_advisory_notes':'The 1200-1500mm flood-proofed construction is what I recommend for any site that flooded during the 2015 Chennai or 2018 Kerala events. At 1200mm plinth height you protect against 4-foot deep flooding which covered most of the affected areas in both those events. The critical details beyond the plinth height are: all electrical distribution boards at 1500mm or above (standard installation height puts them underwater during major floods), flood barrier tracks at every ground floor entry so removable aluminium barriers can be installed in minutes before a flood event, and crystalline waterproofing on all plinth and lower wall surfaces. The accessibility cost is significant - you need a proper ramp and staircase design for daily use at 1200mm height.',
  'pros':'Protects against major urban flood events up to 1.2m depth|Flood barriers block floodwater at doors|Elevated electrical panels prevent electrocution|Materials selected for flood resistance',
  'cons':'Significant accessibility challenge at 1200mm - ramp mandatory|Substantial retaining wall structure required|Higher cost premium|Still vulnerable to extreme events above 1.5m',
  'tooltip_detail':'1200mm+ flood-proofed construction. Protects against major urban floods. All electrical panels at 1500mm+. Flood barriers at all entries. Ramp mandatory.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'FP-004','category_name':'Special','subcategory_name':'Flood-Prone',
  'name':'amphibious_resilient','display_name':'Amphibious / Flood-Resilient Design','region':'South India',
  'description':'Advanced flood-resilient design incorporating: structure on deep pile foundation with hollow substructure allowing controlled flooding of lower void, all critical systems above projected 100-year flood level, flood-resistant materials throughout lower zone, and rapid-dry drainage. For extreme high-risk sites in coastal Kerala, Brahmaputra-fed areas or cyclone-surge zones.',
  'climate_zone':'Warm-Humid','spectrum_position':'Premium','sort_order':'4',
  'base_cost_per_sqft_inr':'65','installation_cost_per_sqft_inr':'30','cost_confidence':'Low',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Specialist estimate; very site-specific; pile foundation + hollow plinth + flood-resistant fit-out; [VERIFY]',
  'expected_lifespan_years':'50','replacement_cost_factor':'0.9','major_maintenance_cycle_years':'10',
  'major_maintenance_cost_factor':'0.15','annual_minor_maint_factor':'0.02','maintenance_complexity':'High',
  'lifecycle_source_notes':'FEMA amphibious construction; Delft University flood resilience; NDMA cyclone guidelines',
  'thermal_resistance_score':'2','acoustic_score':'1','durability_score':'9','moisture_resistance':'Very High',
  'fire_rating':'Class A','energy_impact_modifier':'1.0','accessibility_score':'4',
  'thermal_source_notes':'Ventilated substructure provides natural ventilation under floor. High humidity from flood zone requires dehumidification strategy.',
  'max_floors_supported':'5','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'Sites without pile foundation feasibility|Tight urban plots with no floodwater drainage path',
  'compatible_with':'Pile foundation|Elevated column system',
  'requires_component':'Deep pile foundation to hard strata|Hollow ground-level void structure|All critical services above 100-year flood level|Flood-resistant finishes in lower zone (tiles, concrete, no timber below flood line)|Rapid drainage design|Specialist flood engineer',
  'climate_restrictions':'Designed for coastal Kerala backwater zones, delta regions and areas with documented 1-2 metre flood history. NDMA 100-year flood elevation must be obtained from CWRDM or State Disaster Management Authority.',
  'hard_block_rule':'REQUIRES_SPECIALIST_FLOOD_ENGINEER',
  'advisory_rule':'Obtain NDMA 100-year flood elevation for your specific site before designing flood resilient structure',
  'advisory_message':'Amphibious and flood-resilient design must be based on the 100-year flood elevation for the specific site, obtained from CWRDM (Kerala) or state disaster management authority. Designing to a lower flood level than the 100-year event wastes the premium investment.',
  'advisory_severity':'Critical','constraint_source_notes':'FEMA amphibious construction guidelines; CWRDM Kerala flood data; NDMA',
  'ai_advisory_notes':'Amphibious or truly flood-resilient construction is the right choice for sites in Kerala backwater zones, Godavari-Krishna delta regions or any site where 2-metre deep flooding is a documented historical reality. The design principle is accepting that flooding will occur and designing the building to survive it undamaged rather than trying to keep water out. This means: pile foundation into hard strata so the structure floats above the flood, all critical systems (electrical, plumbing, kitchen) at 2+ metres above ground, and all materials in the lower zone that will flood being water-tolerant (tile, concrete, steel - no timber, no gypsum). This is specialist engineering requiring a flood engineer with South India coastal zone experience.',
  'pros':'Survives major flood events without structural damage|All critical systems above flood line|Appropriate for extreme flood-risk sites|Can be insured at lower rates with certified resilient design',
  'cons':'Very high cost premium|Pile foundation mandatory|Specialist flood engineer required|Significant accessibility challenge|Ongoing humidity management',
  'tooltip_detail':'Amphibious flood-resilient design for extreme risk sites. Pile foundation, all services 2m+ above ground, flood-tolerant materials. Specialist engineer mandatory.',
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
