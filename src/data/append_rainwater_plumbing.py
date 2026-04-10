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
  'component_id':'RWPL-001','category_name':'Systems','subcategory_name':'Rainwater Plumbing',
  'name':'rainwater_plumbing_combined','display_name':'Combined Roof + Waste Pipes','region':'South India',
  'description':'Single drainage system combining roof rainwater discharge with household wastewater. Simplest and cheapest plumbing approach. Cannot be used with rainwater harvesting systems as collected water would be contaminated with grey water.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Basic','sort_order':'1',
  'base_cost_per_sqft_inr':'2','installation_cost_per_sqft_inr':'1','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Combined drain plumbing normalized per sqft; Karnataka PWD SOR 2024-25 reference',
  'expected_lifespan_years':'25','replacement_cost_factor':'0.5','major_maintenance_cycle_years':'10',
  'major_maintenance_cost_factor':'0.08','annual_minor_maint_factor':'0.005','maintenance_complexity':'Low',
  'lifecycle_source_notes':'SWR PVC pipe lifespan 25-30 years',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'6','moisture_resistance':'High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'Rainwater harvesting systems (C6)|Grey water reuse','compatible_with':'Plots without RWH requirement',
  'requires_component':'SWR PVC pipes|Gully traps|Inspection chambers',
  'climate_restrictions':'Not acceptable for plots where BBMP mandates RWH (above 1200 sqft in most Bangalore layouts).',
  'hard_block_rule':'None',
  'advisory_rule':'Not compatible with any rainwater harvesting system - incompatible with C6 RWH decisions',
  'advisory_message':'If you have selected a rainwater harvesting system (C6), you cannot use combined plumbing. Separate roof drain pipes are required to collect clean rainwater separately from grey water.',
  'advisory_severity':'Warning','constraint_source_notes':'BBMP Rainwater Harvesting Bye-laws; TNPCB regulations',
  'ai_advisory_notes':'Combined plumbing made sense when rainwater harvesting was not mandatory and water was not scarce but that is no longer the situation in most South India cities. BBMP has made rainwater harvesting mandatory for all plots above 1200 sqft in Bangalore and a combined drainage system makes it technically impossible to implement RWH because the rooftop water is mixed with wastewater. If you know that you will eventually do RWH - and you should because the BBMP occupancy certificate increasingly requires it - then installing separate pipes from the start costs a few thousand rupees more whereas retrofitting separate downpipes after construction requires extensive work breaking out plastered walls. I recommend separate pipes for all new construction regardless of current RWH plans.',
  'pros':'Lowest drainage cost|Simple installation|No maintenance of separate systems',
  'cons':'Cannot be used with any RWH system|Not BBMP compliant for plots above 1200 sqft|Wastes rooftop rainwater to sewer|Retrofit is expensive and disruptive',
  'tooltip_detail':'Combined rainwater and waste pipes. Cheapest but incompatible with any rainwater harvesting. Not BBMP compliant for large plots.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'RWPL-002','category_name':'Systems','subcategory_name':'Rainwater Plumbing',
  'name':'rainwater_plumbing_separate','display_name':'Separate Roof Drain Pipes','region':'South India',
  'description':'Dedicated SWR PVC downpipes from roof to ground for rainwater, completely separate from the household wastewater drainage system. Enables rainwater harvesting by routing clean roof water to sump or recharge pit. Standard specification for BBMP compliance.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Intermediate','sort_order':'2',
  'base_cost_per_sqft_inr':'5','installation_cost_per_sqft_inr':'3','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Separate SWR downpipe addition cost; Bangalore plumber rates 2024; normalized per sqft',
  'expected_lifespan_years':'25','replacement_cost_factor':'0.5','major_maintenance_cycle_years':'10',
  'major_maintenance_cost_factor':'0.06','annual_minor_maint_factor':'0.005','maintenance_complexity':'Low',
  'lifecycle_source_notes':'SWR PVC pipe lifespan 25-30 years',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'7','moisture_resistance':'High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0.1','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'Rainwater harvesting systems (C6)|Recharge pit|Collection tank',
  'requires_component':'110-160mm SWR PVC downpipes|First flush diverter|Gutter or parapet spout at roof|Inspection chamber at base',
  'climate_restrictions':'In high rainfall areas above 1500mm annual size drainpipes adequately for peak monsoon flow.',
  'hard_block_rule':'None',
  'advisory_rule':'First flush diverter mandatory to exclude initial dirty runoff from storage',
  'advisory_message':'The first 1-2mm of rainfall after a dry period washes dust, bird droppings and pollutants from the roof surface. A first flush diverter valve automatically discards this initial flow and then routes clean water to storage.',
  'advisory_severity':'Warning','constraint_source_notes':'BBMP RWH Bye-laws; IS 15797',
  'ai_advisory_notes':'Separate downpipes are the standard I recommend for all new construction in Bangalore regardless of current RWH plans because once the plaster goes on adding separate downpipes requires breaking channel tracks in finished walls which is expensive and messy. The 110mm SWR pipes run from the roof outlets down the external wall face typically tucked into the plinth junction and terminate at an inspection chamber at ground level from where they go to the recharge pit or sump. The first flush diverter is a cheap but important accessory - it is a simple valve that diverts the first 20-30 litres of roof runoff to waste because this water contains the accumulated dust and bird droppings from the dry period. After the initial flush is diverted the valve closes and clean water flows to your storage. Without this the first heavy rain after summer puts a very dirty load into your sump.',
  'pros':'BBMP compliant for plots above 1200 sqft|Enables rainwater harvesting|Clean water separation|Marginal cost over combined system|First flush diverter improves harvested water quality',
  'cons':'Higher cost than combined system|Slightly more complex installation|Requires first flush diverter for clean harvesting|Separate inspection chambers needed',
  'tooltip_detail':'Separate roof drainpipes. Standard for BBMP compliance and RWH. Install first flush diverter. Do during construction not after.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'RWPL-003','category_name':'Systems','subcategory_name':'Rainwater Plumbing',
  'name':'rainwater_plumbing_dual_greywater','display_name':'Dual System with Grey Water Reuse','region':'South India',
  'description':'Full dual-pipe drainage system separating roof rainwater, bathroom grey water (washbasin, shower), and blackwater (WC). Grey water is treated and reused for toilet flushing and garden irrigation. Full BBMP compliance. Maximum water conservation system.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Premium','sort_order':'3',
  'base_cost_per_sqft_inr':'12','installation_cost_per_sqft_inr':'8','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Dual drain system plus grey water treatment unit; South India specialist plumber rates 2024; normalized per sqft',
  'expected_lifespan_years':'20','replacement_cost_factor':'0.6','major_maintenance_cycle_years':'5',
  'major_maintenance_cost_factor':'0.15','annual_minor_maint_factor':'0.015','maintenance_complexity':'High',
  'lifecycle_source_notes':'Grey water treatment system lifespan 15-20 years; pipe system 25 years',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'7','moisture_resistance':'High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0.2','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'Full RWH system (C6 RWH-004)|IGBC Green Homes compliance',
  'requires_component':'Separate grey water collection pipes|Grey water treatment unit (biofilter or constructed wetland)|Treated water storage|Garden or flushing reuse connection|BBMP discharge approval',
  'climate_restrictions':'Most valuable in water-scarce cities (Bangalore, Hyderabad). Less critical in high-rainfall zones with abundant groundwater.',
  'hard_block_rule':'None',
  'advisory_rule':'Grey water treatment system requires regular maintenance - not suitable for low-maintenance households',
  'advisory_message':'A grey water reuse system requires monthly maintenance of filter media and annual inspection of the treatment unit. This system is not suitable for households that cannot commit to this maintenance schedule.',
  'advisory_severity':'Warning','constraint_source_notes':'BBMP grey water regulations; IS 16095; CPHEEO Manual',
  'ai_advisory_notes':'Dual drainage with grey water reuse is the gold standard for water conservation in South India and makes particularly good sense in Bangalore where water scarcity is acute and BWSSB has been rationing supply in many areas. A typical South India household generates 80-100 litres per person per day of grey water from showers washbasins and kitchen sinks. Treated and reused for toilet flushing and garden irrigation this eliminates 30-40 percent of total water demand. The system requires a grey water treatment unit - either a biofilter or a constructed wetland filter bed - and separate collection pipes that must be installed during construction since retrofitting is essentially impossible without major disruption. The ongoing maintenance requirement is real: the filter media needs cleaning and replacement every 3-6 months and the treatment unit needs an annual inspection. If your household will not commit to this maintenance the system will smell and fail within a year.',
  'pros':'Maximum water conservation - 30-40% demand reduction|Full BBMP and IGBC compliance|Reduces BWSSB water bill significantly|Environmental responsibility|Good for water-scarce locations',
  'cons':'Highest cost and complexity|Must be installed during construction - retrofitting not practical|Regular maintenance mandatory - monthly filter cleaning|Requires household commitment to maintenance|Complex plumbing requires specialist installer',
  'tooltip_detail':'Dual grey water reuse system. Maximum water saving but requires monthly maintenance commitment. Install during construction only.',
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
