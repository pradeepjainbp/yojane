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

# ── RAINWATER HARVESTING (Systems) ─────────────────────────────────────────────
# Cost: INR per sqft of built-up area (system cost normalised)
# 4 options: None → Recharge pit → Rooftop collection tank → Full dual-pipe system
new_rows = [
{
  'component_id':'RWH-001','category_name':'Systems','subcategory_name':'Rainwater Harvesting',
  'name':'no_rwh','display_name':'No Rainwater Harvesting','region':'South India',
  'description':'No rainwater collection or groundwater recharge provision. All water from BWSSB/CMWSSB/KWA municipal supply or borewell. 100% dependent on external water sources.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Baseline','sort_order':'1',
  'base_cost_per_sqft_inr':'0','installation_cost_per_sqft_inr':'0','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'No capital cost.',
  'expected_lifespan_years':'0','replacement_cost_factor':'0','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'N/A',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'10','moisture_resistance':'High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'1.0','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'Municipal water connection or borewell',
  'climate_restrictions':'None',
  'hard_block_rule':'MANDATORY_RWH_IN_BBMP_JURISDICTION',
  'advisory_rule':'RWH is mandatory for plots above 30x40ft in BBMP and CMDA jurisdiction',
  'advisory_message':'BBMP (Bangalore) and CMDA (Chennai) legally mandate rainwater harvesting for plots above 30x40ft. Occupancy Certificate can be denied without RWH installation.',
  'advisory_severity':'Critical','constraint_source_notes':'BBMP Rainwater Harvesting Byelaw 2009; CMDA Development Regulations; BDA Byelaws',
  'ai_advisory_notes':'Skipping rainwater harvesting is not legally permissible for most urban plots in South India. BBMP in Bangalore, CMDA in Chennai and BDA in Bangalore all mandate RWH for plots above a minimum size - typically 30x40 or 1200 sqft. Failure to install means the corporation can refuse your Occupancy Certificate. Even where it is not legally mandatory it is a significant missed opportunity - a simple recharge pit costs Rs 15000-30000 and can recharge the local borewell reducing water bills meaningfully.',
  'pros':'Zero upfront cost','cons':'Illegal for most urban plots above 1200sqft|100% water bill dependency|Borewell depletion in summer|OC may be denied',
  'tooltip_detail':'No RWH. Legally mandatory in most South India urban jurisdictions for plots above 1200sqft. Check local byelaws before skipping.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'RWH-002','category_name':'Systems','subcategory_name':'Rainwater Harvesting',
  'name':'recharge_pit','display_name':'Groundwater Recharge Pit','region':'South India',
  'description':'Simple perforated pit or trench filled with gravel and filter media to redirect rooftop and surface runoff into ground for borewell recharge. Minimum code-compliant RWH. Meets BBMP/CMDA mandatory requirements.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Basic','sort_order':'2',
  'base_cost_per_sqft_inr':'5','installation_cost_per_sqft_inr':'3','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'CPWD DSR 2023; market rate recharge pit excavation + gravel + filter media; normalised per sqft',
  'expected_lifespan_years':'20','replacement_cost_factor':'0.5','major_maintenance_cycle_years':'3',
  'major_maintenance_cost_factor':'0.20','annual_minor_maint_factor':'0.03','maintenance_complexity':'Low',
  'lifecycle_source_notes':'CGWB guidelines; filter media replacement 5-7 years',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'7','moisture_resistance':'High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0.95','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution. Groundwater recharge reduces urban heat island marginally.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'Plots on rocky hard-rock sites with no soil percolation',
  'compatible_with':'All structural systems',
  'requires_component':'Perforated PVC pipe|20-40mm gravel filter media|Fine sand layer|Mosquito-proof mesh cover|Downpipe diverter from roof drainage',
  'climate_restrictions':'In black cotton soil areas percolation is very low - recharge pit effectiveness is minimal. Consult hydrogeologist.',
  'hard_block_rule':'None',
  'advisory_rule':'Clean filter media annually before monsoon to prevent clogging',
  'advisory_message':'Recharge pit filter media clogs with silt within 2-3 monsoons if not cleaned. Annual pre-monsoon cleaning is essential or the pit fills with mud and becomes useless.',
  'advisory_severity':'Warning','constraint_source_notes':'CGWB RWH manual; BBMP byelaws',
  'ai_advisory_notes':'The recharge pit is the minimum RWH system and satisfies BBMP and CMDA compliance at very low cost. A properly built pit of 1.5m diameter and 3m depth filled with graded gravel can recharge 500-1000 litres per hour of heavy rain into the aquifer, measurably improving your borewell water level over the monsoon season. The critical maintenance point is cleaning the filter gravel before every monsoon - silt from the roof blocks the voids in one season and turns the pit into a mud trap. The first flush diverter is also important - the first 5-10 minutes of rain washes bird droppings and dust off the roof and should be diverted to drain, not into the recharge pit.',
  'pros':'Meets BBMP/CMDA legal requirement|Recharges borewell - better water level|Low cost|Passive - no power or operator needed',
  'cons':'Does not store water for direct use|Clogs without annual maintenance|Ineffective on rocky sites|First flush contamination without diverter',
  'tooltip_detail':'Minimum-cost RWH recharge pit. Meets BBMP/CMDA legal requirement. Annual pre-monsoon cleaning mandatory or it clogs and stops working.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'RWH-003','category_name':'Systems','subcategory_name':'Rainwater Harvesting',
  'name':'collection_storage_tank','display_name':'Rooftop Collection + Underground Storage Tank','region':'South India',
  'description':'Rooftop runoff collected via gutters, filtered and stored in underground RCC or HDPE sump (10000-20000 litres). Used for garden irrigation, car washing, toilet flushing. Reduces municipal water consumption 30-50%.',
  'climate_zone':'Warm-Humid|Temperate','spectrum_position':'Performance','sort_order':'3',
  'base_cost_per_sqft_inr':'22','installation_cost_per_sqft_inr':'10','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market rate 15000L RCC underground sump + filtration + gutters; normalised per sqft 1500sqft house',
  'expected_lifespan_years':'30','replacement_cost_factor':'0.6','major_maintenance_cycle_years':'5',
  'major_maintenance_cost_factor':'0.15','annual_minor_maint_factor':'0.02','maintenance_complexity':'Medium',
  'lifecycle_source_notes':'RCC sump 30yr; HDPE tank 20yr; filter cartridge 1-2yr',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'8','moisture_resistance':'High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0.9','accessibility_score':'8',
  'thermal_source_notes':'No thermal contribution. Underground storage keeps water cool passively.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'Flat roofs without perimeter parapet gutters|Very small plots below 600sqft',
  'compatible_with':'All structural systems with guttered roof drainage',
  'requires_component':'Perimeter gutters and downpipes|First-flush diverter|Sand and gravel filter unit|Underground sump or HDPE tank|Submersible pump for reuse|Overflow to recharge pit',
  'climate_restrictions':'Only viable in areas with minimum 600mm annual rainfall. In Hot-Dry zones like interior Tamil Nadu collection is insufficient for meaningful storage - recharge pit is better.',
  'hard_block_rule':'None',
  'advisory_rule':'First-flush diverter is mandatory - do not collect the first 10 minutes of rain',
  'advisory_message':'The first rain of a dry spell washes months of bird droppings, dust and debris off the roof into your collection system. A first-flush diverter that discards the first 20-25 litres per 100sqm of roof area is essential for water quality.',
  'advisory_severity':'Warning','constraint_source_notes':'CGWB RWH manual; IS 15797 water quality; NBC 2016',
  'ai_advisory_notes':'A rooftop collection and storage system is a fantastic investment for South India homes with gardens, cars to wash or borewell dependency. A 1500sqft roof in Bangalore receiving 970mm annual rainfall can collect roughly 100000-120000 litres per year after losses - enough to run a garden and supplement toilet flushing. The siting of the underground sump is critical - it must be at least 15 feet from any septic tank or soak pit to prevent contamination. The first-flush diverter is not optional - the first rain after summer carries intense contamination from the roof surface. This water must be discarded automatically before collection begins.',
  'pros':'30-50% reduction in municipal water use|Reduces water bills significantly|Garden and toilet flushing use|Underground storage keeps water cool',
  'cons':'High initial cost for sump construction|Pump required for reuse|Seasonal - depends on monsoon|First flush contamination without diverter',
  'tooltip_detail':'Stores rooftop rainwater in underground sump. 30-50% water bill reduction. First-flush diverter mandatory. Sump 15ft from septic tank.',
  'status':'Active','verify_flags':'base_cost_per_sqft_inr','data_filled_by':'AI'
},
{
  'component_id':'RWH-004','category_name':'Systems','subcategory_name':'Rainwater Harvesting',
  'name':'dual_pipe_full_system','display_name':'Full Dual-Pipe RWH System (Potable + Non-Potable)','region':'South India',
  'description':'Complete dual-pipe plumbing system with separate non-potable network for toilet flushing, garden and car wash supplied from treated harvested rainwater. Includes slow-sand filter + UV treatment for partial potable use. Most water-efficient residential system.',
  'climate_zone':'Warm-Humid|Temperate','spectrum_position':'Premium','sort_order':'4',
  'base_cost_per_sqft_inr':'42','installation_cost_per_sqft_inr':'20','cost_confidence':'Low',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market estimate dual-pipe plumbing + UV treatment + large sump; very site-specific; normalised per sqft [VERIFY]',
  'expected_lifespan_years':'30','replacement_cost_factor':'0.6','major_maintenance_cycle_years':'3',
  'major_maintenance_cost_factor':'0.20','annual_minor_maint_factor':'0.03','maintenance_complexity':'High',
  'lifecycle_source_notes':'RCC sump 30yr; UV lamp replacement annual; sand filter media 5yr',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'8','moisture_resistance':'High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0.85','accessibility_score':'6',
  'thermal_source_notes':'No thermal contribution. Significant reduction in municipal water pumping energy.',
  'max_floors_supported':'5','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'Apartment buildings without dedicated RWH authority|Sites below 1200sqft',
  'compatible_with':'All structural systems on adequate plot area',
  'requires_component':'Dual pipe network (colour-coded blue potable + grey non-potable)|Large underground sump 25000L+|First-flush diverter|Slow sand filter|UV steriliser for partial potable treatment|Pressure pump|Annual water quality testing',
  'climate_restrictions':'Only viable where annual rainfall exceeds 750mm. In Hot-Dry zones system must be supplemented by borewell or tanker during 6-8 month dry season.',
  'hard_block_rule':'None',
  'advisory_rule':'Annual water quality testing mandatory before using treated RWH for potable purposes',
  'advisory_message':'Harvested rainwater treated with UV only is not reliably safe for drinking without periodic bacteriological testing. Annual water quality certificate from a NABL-accredited lab is mandatory.',
  'advisory_severity':'Strong-Warning','constraint_source_notes':'IS 10500 drinking water standard; CGWB RWH manual; NBC 2016 Part 9',
  'ai_advisory_notes':'The full dual-pipe system is the gold standard for water self-sufficiency and is particularly valuable for large plots in water-scarce interior Tamil Nadu or Karnataka. By running a completely separate pipe network for non-potable uses (toilets, garden, car wash) you can supply 40-60% of household water needs from harvested rain in a good monsoon year. The complexity and cost are significant - dual plumbing during construction adds 15-20% to plumbing cost. Water quality is the key concern - I only recommend using treated harvested water for potable purposes after annual NABL lab testing. For non-potable uses it is perfectly safe with a basic sand filter and UV treatment.',
  'pros':'50-70% water self-sufficiency|Lowest water bills possible|Future-proof against water scarcity|Non-potable use reduces pressure on municipal supply',
  'cons':'Highest cost and complexity|Dual plumbing must be installed during construction - cannot retrofit|Annual lab testing required|Water shortage in long dry seasons',
  'tooltip_detail':'Full dual-pipe RWH for 50-70% water independence. Must be built in during construction. Annual water quality testing mandatory.',
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
