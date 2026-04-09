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

# ── WASTE MANAGEMENT (Systems) ─────────────────────────────────────────────────
# On-site household waste management system
# Cost: INR per sqft of built-up area
# 4 options: No provision → Segregation bins → Composting → Biogas plant
new_rows = [
{
  'component_id':'WM-001','category_name':'Systems','subcategory_name':'Waste Management',
  'name':'no_waste_provision','display_name':'No On-Site Waste System','region':'South India',
  'description':'No dedicated waste management infrastructure. All waste (mixed) collected by municipal door-to-door service. No segregation, composting or biogas. Standard for most South India residential construction.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Baseline','sort_order':'1',
  'base_cost_per_sqft_inr':'0','installation_cost_per_sqft_inr':'0','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'No capital cost. Municipal collection fees vary by corporation.',
  'expected_lifespan_years':'0','replacement_cost_factor':'0','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'N/A',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'10','moisture_resistance':'High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'1.0','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'Municipal solid waste collection access',
  'climate_restrictions':'None','hard_block_rule':'None',
  'advisory_rule':'Provide minimum segregation storage area - wet and dry bins - in kitchen design',
  'advisory_message':'SWM Rules 2016 mandate source segregation of waste into wet (organic) and dry (recyclable) at household level. Design a minimum 2-bin storage niche in the kitchen utility area.',
  'advisory_severity':'Info','constraint_source_notes':'Solid Waste Management Rules 2016; Municipal Solid Waste guidelines',
  'ai_advisory_notes':'No dedicated waste system is the starting point for most homes and is fine if municipal collection is reliable. However the Solid Waste Management Rules 2016 legally require source segregation at the household level - so at minimum every house should design a 2-bin storage niche (wet and dry) in the kitchen utility area. This costs nothing to build and makes daily waste segregation practical. If you have any outdoor space a composting bin for kitchen wet waste eliminates 40-60% of the waste that goes to the overloaded municipal system.',
  'pros':'Zero upfront cost|No maintenance|Relies on municipal system',
  'cons':'100% dependent on municipal collection reliability|Contributes to overloaded landfills|SWM Rules 2016 segregation requirement unenforced but legally applicable|Organic waste creates odour without management',
  'tooltip_detail':'No on-site waste system. At minimum design 2-bin wet/dry segregation niche in kitchen. SWM Rules 2016 require source segregation.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'WM-002','category_name':'Systems','subcategory_name':'Waste Management',
  'name':'segregation_recycling','display_name':'Segregation + Dry Waste Recycling Station','region':'South India',
  'description':'Dedicated 3-bin wet/dry/reject segregation station in utility area with built-in storage for segregated dry recyclables (paper, plastic, metal, glass). Monthly pickup by kabadiwala or recycling aggregator. Meets SWM Rules 2016 compliance.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Standard','sort_order':'2',
  'base_cost_per_sqft_inr':'3','installation_cost_per_sqft_inr':'2','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Cost of built-in 3-bin cabinet + dedicated utility shelf; normalised per sqft',
  'expected_lifespan_years':'20','replacement_cost_factor':'0.8','major_maintenance_cycle_years':'5',
  'major_maintenance_cost_factor':'0.10','annual_minor_maint_factor':'0.01','maintenance_complexity':'Low',
  'lifecycle_source_notes':'SWM Rules 2016; cabinet lifespan 20yr',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'8','moisture_resistance':'High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0.98','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'Built-in 3-bin cabinet in utility area (wet/dry/reject)|Ventilated outdoor dry waste storage niche|Kabadiwala or Recyclekaro/Sahaas aggregator contact',
  'climate_restrictions':'In high-humidity zones ventilate the dry waste storage cabinet to prevent mould on paper and cardboard recyclables.',
  'hard_block_rule':'None',
  'advisory_rule':'Size wet waste bin for max 3-day storage before municipal collection - larger bins create odour',
  'advisory_message':'A wet organic waste bin holding more than 3 days of kitchen waste creates significant odour in South India heat and humidity. Design the wet bin for max 10-12 litres (2-3 days) with a tight-fitting lid and direct connection to composting or municipal pickup route.',
  'advisory_severity':'Info','constraint_source_notes':'SWM Rules 2016; BBMP/GHMC waste management guidelines',
  'ai_advisory_notes':'Proper waste segregation at source is genuinely easy to achieve with the right kitchen design and it makes a real difference to how much goes to landfill. The key is designing the 3-bin station into the kitchen utility layout before construction - retrofitting bins into a finished kitchen is always unsatisfactory. In Bangalore services like Hasiru Dala and Sahaas pick up segregated dry recyclables for free monthly and will pay you for certain materials. The wet organic waste should ideally feed a composting system - even a small balcony composting unit handles 1-2 person kitchen waste easily.',
  'pros':'SWM Rules 2016 compliant|Reduces landfill contribution significantly|Dry recyclables earn money from kabadiwala|Low cost to implement during construction',
  'cons':'Requires behaviour change from household members|Wet bin needs frequent emptying in South India heat|Municipal collection unreliability affects system',
  'tooltip_detail':'3-bin segregation station built into kitchen. Low cost, high impact. Dry recyclables earn income from kabadiwala. Wet bin max 3-day capacity.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'WM-003','category_name':'Systems','subcategory_name':'Waste Management',
  'name':'composting_system','display_name':'On-Site Composting (Kitchen + Garden Waste)','region':'South India',
  'description':'Dedicated composting unit processing kitchen organic waste and garden trimmings into compost for garden use. Options: aerobic bin composting (balcony), pit composting (garden plot) or tumbler composting. Eliminates 40-60% of household waste from landfill.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Performance','sort_order':'3',
  'base_cost_per_sqft_inr':'5','installation_cost_per_sqft_inr':'2','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market rate composting bin or pit construction; normalised per sqft; compost bin Rs 800-2500',
  'expected_lifespan_years':'15','replacement_cost_factor':'0.8','major_maintenance_cycle_years':'3',
  'major_maintenance_cost_factor':'0.15','annual_minor_maint_factor':'0.02','maintenance_complexity':'Medium',
  'lifecycle_source_notes':'BBMP composting guidelines; Hasiru Dala operational data',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'8','moisture_resistance':'High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0.95','accessibility_score':'8',
  'thermal_source_notes':'No thermal contribution. Composting reduces methane from landfill organics.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'Apartments above ground floor without terrace access|Very small plots below 600sqft without outdoor space',
  'compatible_with':'All structural systems with outdoor or terrace access',
  'requires_component':'Compost bin or pit location in garden or terrace|Access from kitchen without long path|Cocopeat or dry leaf cover material|Garden hose access for moisture management',
  'climate_restrictions':'In very hot dry summers (Hyderabad, interior TN) compost bins need shading and more frequent moisture addition to prevent drying out.',
  'hard_block_rule':'None',
  'advisory_rule':'Compost bin must be within 10m of kitchen to encourage daily use',
  'advisory_message':'A composting bin more than 10-15 meters from the kitchen door will be used inconsistently. Site the compost unit at the back of the kitchen or in an easily accessible corner of the garden.',
  'advisory_severity':'Info','constraint_source_notes':'BBMP composting guidelines; practical observation South India',
  'ai_advisory_notes':'Home composting is the most impactful single waste management decision a South India homeowner can make. A 4-person household in Bangalore generates roughly 400-600 grams of kitchen organic waste daily and virtually all of it can be composted rather than going to the overloaded BBMP collection system. The resulting compost is excellent garden fertiliser. The setup cost is minimal - a plastic compost bin costs Rs 1500-2500 or a brick-lined pit costs Rs 3000-5000. The key design requirement is locating the compost unit within comfortable walking distance of the kitchen door - bins at the far end of a large garden are abandoned within weeks. In apartment buildings terrace composting or community composting units serve multiple households.',
  'pros':'Eliminates 40-60% of household waste from landfill|Free organic garden fertiliser|Reduces kitchen odour from organic waste|Very low cost to implement',
  'cons':'Requires regular management (turning, moisture)|Must be sited near kitchen door for compliance|Not suitable for high-rise apartments without terrace|Fruit flies if managed incorrectly',
  'tooltip_detail':'On-site composting eliminates 40-60% of landfill waste. Locate within 10m of kitchen door. Free compost for garden. Low cost, high impact.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'WM-004','category_name':'Systems','subcategory_name':'Waste Management',
  'name':'biogas_plant','display_name':'Biogas Plant (Kitchen Waste to Cooking Gas)','region':'South India',
  'description':'Compact household biogas digester (1-2 cubic meter) converting kitchen organic waste and food scraps into biogas for cooking and slurry for fertiliser. Eliminates LPG dependency for 1-2 cooking hours per day for a 4-6 person family.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate','spectrum_position':'Premium','sort_order':'4',
  'base_cost_per_sqft_inr':'8','installation_cost_per_sqft_inr':'4','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market rate HomeBiogas/Biotech Kerala 1-2m3 domestic unit Rs 12000-25000 installed; normalised per sqft 1500sqft house',
  'expected_lifespan_years':'20','replacement_cost_factor':'0.7','major_maintenance_cycle_years':'5',
  'major_maintenance_cost_factor':'0.15','annual_minor_maint_factor':'0.02','maintenance_complexity':'High',
  'lifecycle_source_notes':'MNRE biogas programme; Biotech Kerala operational data; SNV biogas manual',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'7','moisture_resistance':'Medium',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0.88','accessibility_score':'6',
  'thermal_source_notes':'Biogas replaces LPG cooking reducing fossil fuel carbon. Slurry improves soil health reducing chemical fertiliser. ECBC 2017.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'High-rise apartments without ground floor access|Plots below 600sqft without outdoor space',
  'compatible_with':'All structural systems with outdoor space',
  'requires_component':'Outdoor space 2-3 sqm for digester|Biogas pipe from digester to kitchen burner|Dedicated biogas-compatible burner|Slurry tank or garden discharge point|MNRE-approved installer',
  'climate_restrictions':'Biogas production slows significantly below 15C. In higher altitude South India zones (Ooty, Kodaikanal, Coorg) production drops in winter months. Not suitable in cold highland zones.',
  'hard_block_rule':'BLOCK_IN_COLD_HIGHLAND_ZONES_BELOW_15C',
  'advisory_rule':'Digester must be sited in full sun - gas production proportional to digester temperature',
  'advisory_message':'Biogas digesters operate best at 30-35C. Siting in shade reduces gas production by 30-50%. Place in direct sun, away from tree cover.',
  'advisory_severity':'Warning','constraint_source_notes':'MNRE biogas programme guidelines; SNV biogas manual; IS 9478',
  'ai_advisory_notes':'Household biogas is a genuinely magical system - you put food scraps in one end and get cooking gas and liquid fertiliser out the other. Kerala has the highest density of household biogas plants in India with over 400000 units installed through the Biotech Kerala programme. A 2 cubic meter unit handles the organic waste from a 4-6 person family and produces enough gas for 1-2 hours of cooking daily eliminating 30-40% of LPG consumption. The slurry discharge is excellent liquid fertiliser for the garden. The installation must be done by an MNRE-approved installer and the digester absolutely must be in direct sun - shade cuts gas production dramatically. Not suitable for cold highland zones where below 15C temperatures kill the bacteria.',
  'pros':'Cooking gas from food waste - 30-40% LPG saving|Slurry is excellent garden fertiliser|Eliminates organic waste landfill contribution|MNRE subsidy available',
  'cons':'Requires outdoor space|Digester must be in full sun|Cold highland zones not suitable|Daily feeding and management required|Requires MNRE-approved installer',
  'tooltip_detail':'Household biogas digester converts kitchen waste to cooking gas. 30-40% LPG saving. Sited in full sun. MNRE subsidy available. Kerala has 400,000 units.',
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
