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
  'component_id':'UPS-001','category_name':'Systems','subcategory_name':'UPS Provision',
  'name':'ups_no_provision','display_name':'No UPS Provision','region':'South India',
  'description':'No dedicated inverter or UPS circuit wiring. All circuits powered from BESCOM/TNEB grid only. Only suitable for areas with fully reliable 24/7 power supply and no planned inverter or home battery system.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Basic','sort_order':'1',
  'base_cost_per_sqft_inr':'0','installation_cost_per_sqft_inr':'0','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'No additional cost',
  'expected_lifespan_years':'25','replacement_cost_factor':'0.5','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'No UPS wiring - standard electrical lifespan applies',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'6','moisture_resistance':'Medium',
  'fire_rating':'Class A','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'Future inverter installation without rewiring','compatible_with':'All electrical systems',
  'requires_component':'None',
  'climate_restrictions':'None',
  'hard_block_rule':'None',
  'advisory_rule':'Not recommended for most South India locations - power cuts of 2-6 hours common in many areas',
  'advisory_message':'Without UPS wiring provision any future inverter installation requires partial rewiring of the distribution board and dedicated circuit routing - adding Rs 15000-25000 to future installation cost.',
  'advisory_severity':'Warning','constraint_source_notes':'BESCOM/TNEB outage data',
  'ai_advisory_notes':'No UPS provision made sense when inverters were expensive luxury items and South India power supply was more reliable. In 2024 Bangalore areas outside the CBD still experience 2-4 hour scheduled power cuts in summer and unscheduled outages during monsoon. Without any UPS wiring the inverter can only power the circuits it is hardwired to which requires partial rewiring of the distribution board after construction. The DB board rewiring alone costs Rs 8000-12000 and if separate UPS circuit conduits are needed through plastered walls the total can reach Rs 20000-30000. The pre-provision cost during construction is Rs 2000-3000 for an extra conduit and changeover switch position in the DB. This is a straightforward economic decision.',
  'pros':'No upfront cost|Simplest electrical installation',
  'cons':'No power backup for any circuit|Future inverter addition requires DB rewiring and conduit work|Not suitable for most South India locations with power cuts|Rs 15000-25000 additional cost to add later',
  'tooltip_detail':'No UPS wiring. Not recommended for most South India areas. Adding later costs Rs 15000-25000 in rewiring.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'UPS-002','category_name':'Systems','subcategory_name':'UPS Provision',
  'name':'ups_essentials_circuit','display_name':'Essentials Circuit (Lights + Fans)','region':'South India',
  'description':'Dedicated UPS/inverter circuit for essential loads: all lights, ceiling fans, router, and one TV point per floor. Separate wiring from a changeover switch in the distribution board. Covers 80% of household inconvenience from power cuts at 20% of whole-house backup cost.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Intermediate','sort_order':'2',
  'base_cost_per_sqft_inr':'4','installation_cost_per_sqft_inr':'3','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Dedicated UPS circuit wiring + changeover switch; Bangalore electrician rates 2024; normalized per sqft',
  'expected_lifespan_years':'20','replacement_cost_factor':'0.4','major_maintenance_cycle_years':'5',
  'major_maintenance_cost_factor':'0.05','annual_minor_maint_factor':'0.005','maintenance_complexity':'Low',
  'lifecycle_source_notes':'UPS circuit wiring lifespan 20-25 years; inverter battery replacement every 3-5 years (separate cost)',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'7','moisture_resistance':'Medium',
  'fire_rating':'Class A','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All residential configurations|Tubular/Li-ion inverter battery',
  'requires_component':'Changeover switch or ATS in distribution board|Separate 2.5 sqmm copper circuit for lights and fans|Inverter battery space in utility area (minimum 1 sqm)',
  'climate_restrictions':'None',
  'hard_block_rule':'None',
  'advisory_rule':'Reserve space for inverter battery (minimum 1sqm ventilated area) in utility or store room',
  'advisory_message':'Lead-acid inverter batteries must be placed in ventilated locations away from living areas as they emit hydrogen gas during charging. Lithium-ion batteries are safer but require adequate space and ventilation. Plan for this space.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 1651; inverter manufacturer installation guidelines',
  'ai_advisory_notes':'The essentials circuit with a 4-hour battery backup for lights fans and router covers 80 percent of the practical inconvenience from power cuts at 20 percent of the cost of a whole-house backup system. During a typical South India power cut what you actually need to be comfortable is functioning ceiling fans, lights to see by and a working internet router. The AC can wait - running fans makes a significant difference in comfort. The changeover switch in the distribution board is a simple manual or automatic transfer switch that takes 5 minutes to install during the electrical work and costs Rs 800-1500. The conduit for the separate UPS circuit needs to run parallel to the main circuit conduit. Plan the inverter battery location carefully - lead acid batteries emit hydrogen gas during charging and need ventilation away from sleeping areas. A small store room or utility area corner with a 1 sqm footprint is ideal.',
  'pros':'Covers 80% of power cut inconvenience at low cost|Simple standard installation|All contractors understand this|Easy to scale up battery capacity later|Lights + fans + router - the essential comfort needs',
  'cons':'Does not support AC or other high-power loads|Battery needs replacement every 3-5 years|Lead acid battery needs ventilated location|Cannot support EV charging',
  'tooltip_detail':'Essentials circuit for lights, fans, router. Best value UPS provision. Reserve ventilated 1sqm space for battery.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'UPS-003','category_name':'Systems','subcategory_name':'UPS Provision',
  'name':'ups_whole_house_backup','display_name':'Whole-House Backup (All Circuits)','region':'South India',
  'description':'All household circuits connected to inverter/battery backup through automatic transfer switch. Includes AC circuits, kitchen appliances, and all power sockets. Premium lithium-ion battery system or large inverter bank. For areas with severe and frequent power cuts.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Premium','sort_order':'3',
  'base_cost_per_sqft_inr':'10','installation_cost_per_sqft_inr':'7','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Full ATS + high-capacity wiring + large battery system; Bangalore specialist rates 2024; normalized per sqft',
  'expected_lifespan_years':'15','replacement_cost_factor':'0.7','major_maintenance_cycle_years':'3',
  'major_maintenance_cost_factor':'0.2','annual_minor_maint_factor':'0.015','maintenance_complexity':'High',
  'lifecycle_source_notes':'Li-ion battery 10-15 year lifespan; lead acid 5-7 years for high-cycle whole house use',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'8','moisture_resistance':'Medium',
  'fire_rating':'Class A','energy_impact_modifier':'0.05','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All residential configurations|Solar grid-tied system|Li-ion home battery',
  'requires_component':'High-capacity ATS or automatic changeover|Heavy gauge wiring for AC circuits|Lithium-ion battery system (preferred)|Dedicated battery room or large utility space|Annual inspection',
  'climate_restrictions':'None',
  'hard_block_rule':'None',
  'advisory_rule':'Use lithium-ion battery for whole-house backup - lead acid loses capacity rapidly under AC load cycles',
  'advisory_message':'Whole-house backup with AC inclusion requires Li-ion batteries. Lead-acid batteries lose 30-40% capacity within 2 years when regularly discharged deeply by AC loads. The economics work only with Li-ion.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 1651; Li-ion battery safety standards; installer guidelines',
  'ai_advisory_notes':'Whole house backup makes genuine sense for plots in areas that have 4-6 hour cuts on a daily basis during summer particularly in some parts of Tamil Nadu and Andhra Pradesh where scheduled load shedding is still a reality. For Bangalore it is generally over-specified as grid reliability has improved significantly in most layouts. The critical technology decision is the battery. If you put lead-acid batteries in a whole-house backup system that regularly runs your 1.5 ton AC for 3-4 hours daily the batteries will be at 60 percent capacity within 18 months and need replacement within 3 years. Lithium-ion batteries handle deep cycling gracefully and last 10-15 years. The upfront cost is 3-4x more than lead acid but the lifecycle cost is lower. If you are also considering solar this system integrates naturally as a home battery storage system combining the backup benefit with solar self-consumption optimisation.',
  'pros':'Complete backup including AC - no lifestyle change during cuts|Integrates with solar battery storage|Automatic transfer - no manual intervention|Li-ion system lasts 10-15 years',
  'cons':'Highest cost|Li-ion battery essential (3-4x lead acid cost)|Requires dedicated battery space|Annual maintenance|Overkill for most Bangalore locations with good grid reliability',
  'tooltip_detail':'Whole-house backup including AC. Use Li-ion batteries only - lead acid fails rapidly under AC load. High cost but necessary for high-cut areas.',
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
