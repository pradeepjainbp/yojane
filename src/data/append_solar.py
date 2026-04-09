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

# ── SOLAR (Systems) ────────────────────────────────────────────────────────────
# Cost unit: base_cost_per_sqft_inr = INR per sqft of built-up area (system cost normalised)
# 5 options: No solar → Solar water heater → Grid-tied rooftop PV → Hybrid PV+Battery → Full off-grid
new_rows = [
{
  'component_id':'SOL-001','category_name':'Systems','subcategory_name':'Solar',
  'name':'no_solar','display_name':'No Solar (Grid Only)','region':'South India',
  'description':'100% grid electricity and gas/electric water heating. No rooftop solar provision. Baseline option with maximum grid dependency.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Baseline','sort_order':'1',
  'base_cost_per_sqft_inr':'0','installation_cost_per_sqft_inr':'0','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'No capital cost. Grid electricity at Rs 6-9 per unit South India DISCOMs.',
  'expected_lifespan_years':'0','replacement_cost_factor':'0','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'No system to maintain. Grid tariff escalation 4-6% per year historically.',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'10','moisture_resistance':'High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'3.0','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution. Grid power carbon intensity ~0.82 kg CO2/kWh South India grid.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'DISCOM single or three-phase connection',
  'climate_restrictions':'None','hard_block_rule':'None',
  'advisory_rule':'Reserve roof area and conduit space if solar is planned in the future',
  'advisory_message':'Even if not installing solar now, run a 25mm conduit from rooftop to DB location and keep south-facing roof area clear. Retrofitting later without this preparation is significantly more expensive.',
  'advisory_severity':'Info','constraint_source_notes':'MNRE solar guidelines; DISCOM connection rules',
  'ai_advisory_notes':'Choosing no solar today is not necessarily wrong if budget is tight, but I always ask clients to at least future-proof the building by running a blank conduit from the rooftop to the electrical DB and keeping 100-150 sqft of south-facing roof clear of water tanks and TV dishes. South India electricity tariffs have risen 6-8% every year and the payback period for solar keeps shrinking. A 3kWp system on a 1500 sqft house today pays back in 4-5 years. If you cannot do solar now, at least do not block the option.',
  'pros':'Zero upfront cost|No maintenance|No system complexity',
  'cons':'100% dependent on grid tariff escalation|High carbon footprint|No backup during power cuts',
  'tooltip_detail':'Grid-only baseline. No solar investment. At minimum run a conduit from rooftop to DB to keep the future option open.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'SOL-002','category_name':'Systems','subcategory_name':'Solar',
  'name':'solar_water_heater','display_name':'Solar Water Heater (SWH)','region':'South India',
  'description':'100-200 LPD flat plate or evacuated tube solar water heating system. Eliminates electric geyser load (15-20% of household electricity). Bureau of Energy Efficiency 5-star rated. Most cost-effective first solar investment.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Standard','sort_order':'2',
  'base_cost_per_sqft_inr':'12','installation_cost_per_sqft_inr':'5','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market rate 200LPD flat plate Racold/V-Guard/Supreme Rs 18000-25000; normalised per sqft 1500sqft house',
  'expected_lifespan_years':'15','replacement_cost_factor':'0.8','major_maintenance_cycle_years':'5',
  'major_maintenance_cost_factor':'0.15','annual_minor_maint_factor':'0.02','maintenance_complexity':'Low',
  'lifecycle_source_notes':'BEE SWH standards; IS 12933; manufacturer 5yr warranty on collector',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'7','moisture_resistance':'High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0.8','accessibility_score':'9',
  'thermal_source_notes':'Eliminates 15-20% of household electricity load. Flat plate collector efficiency 60-70%. ECBC 2017 SWH credit.',
  'max_floors_supported':'3','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'North-facing roof slope|Heavily shaded rooftops',
  'compatible_with':'All structural systems with south or east-facing roof access',
  'requires_component':'South or east-facing roof area min 2 sqm per 100LPD|PPR or copper hot water pipes (not uPVC)|Insulated hot water pipe runs|Backup electric element for cloudy days',
  'climate_restrictions':'In coastal high-humidity zones specify evacuated tube collector over flat plate - higher efficiency in diffuse light conditions during monsoon.',
  'hard_block_rule':'None',
  'advisory_rule':'Connect SWH only to PPR or copper pipes — never uPVC which fails at SWH temperatures',
  'advisory_message':'Solar water heaters produce water at 60-80°C in summer. uPVC pipes deform and burst at these temperatures. Only connect to PPR or copper pipe.',
  'advisory_severity':'Critical','constraint_source_notes':'IS 12933; BEE SWH programme; MNRE',
  'ai_advisory_notes':'The solar water heater is the single best-value first solar investment for any South India home. Payback is typically 2-3 years because water heating accounts for 15-20% of household electricity and South India gets 300+ sunny days a year. The installation is simple and any licensed plumber can do it. The critical plumbing mistake I see constantly is connecting the SWH output to uPVC pipes which melt or deform at 70-80 degree water temperatures. Only use PPR or copper for all hot water lines from the SWH. Specify evacuated tube collectors for coastal Kerala and Tamil Nadu where monsoon cloud cover reduces flat plate efficiency.',
  'pros':'Fastest solar payback - 2-3 years|Simple technology easy to maintain|Eliminates 15-20% electricity bill|No inverter or battery needed',
  'cons':'Only heats water - no electricity generation|Backup geyser needed for cloudy periods|Requires south/east roof access|Hard water causes scale inside tubes',
  'tooltip_detail':'Solar water heater. Best-value first solar step. 2-3 year payback. Connect only to PPR or copper pipes - never uPVC.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'SOL-003','category_name':'Systems','subcategory_name':'Solar',
  'name':'grid_tied_pv','display_name':'Grid-Tied Rooftop Solar PV (3-5 kWp)','region':'South India',
  'description':'3-5 kWp monocrystalline PV panels with string inverter, bi-directional net metering. Exports surplus to grid and earns credits. No battery. Covers 60-80% of household electricity consumption for 1500-2500 sqft homes.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Performance','sort_order':'3',
  'base_cost_per_sqft_inr':'48','installation_cost_per_sqft_inr':'12','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'MNRE benchmark cost Rs 45000-55000 per kWp installed 2024; 4kWp system Rs 1.8-2.2L; normalised per sqft 1500sqft house',
  'expected_lifespan_years':'25','replacement_cost_factor':'0.7','major_maintenance_cycle_years':'10',
  'major_maintenance_cost_factor':'0.15','annual_minor_maint_factor':'0.01','maintenance_complexity':'Low',
  'lifecycle_source_notes':'Panel warranty 25yr linear output; inverter replacement cycle 10-12yr; MNRE ALMM list',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'8','moisture_resistance':'High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0.3','accessibility_score':'9',
  'thermal_source_notes':'Panels shade roof surface reducing roof heat gain by 15-20%. Net zero daytime grid draw. ECBC 2017 renewable credit.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'Heavily shaded roof|North-facing only roof',
  'compatible_with':'All structural systems with flat or south-tilted roof',
  'requires_component':'South-facing roof area min 100 sqft per kWp|MS or aluminium mounting structure|MNRE-approved ALMM-listed panels|String inverter|Bi-directional net meter from DISCOM|DC cable tray from roof to inverter|Earthing and lightning protection',
  'climate_restrictions':'Coastal areas require marine-grade aluminium mounting frames and MC4 connectors rated for high humidity. Inland Hot-Dry zones achieve highest generation - Hyderabad and Bangalore plateau outperform coastal areas.',
  'hard_block_rule':'None',
  'advisory_rule':'Apply for DISCOM net-metering approval during construction - approval takes 2-6 months',
  'advisory_message':'Net-metering application to BESCOM/TANGEDCO/KSEB must be submitted during construction. Approval takes 2-6 months. Do not install panels before approval or you cannot legally export power.',
  'advisory_severity':'Warning','constraint_source_notes':'MNRE Net Metering Regulations 2021; DISCOM utility rules; IS 16221',
  'ai_advisory_notes':'A grid-tied solar system is the best financial investment most South India homeowners can make right now. At Rs 45000-55000 per kWp installed, a 4kWp system costs around Rs 1.8-2.2 lakhs and generates roughly 480-560 units per month in Bangalore or Chennai. At current tariffs of Rs 7-9 per unit that is Rs 3500-5000 per month savings - payback in under 4 years with 25 years of near-free electricity after that. The process trap is the DISCOM approval - file the net-metering application with BESCOM or TANGEDCO as soon as your building plan is approved because it takes 2-6 months. Panels must be on the MNRE ALMM approved list for subsidy eligibility. Only buy panels from that list.',
  'pros':'60-80% reduction in electricity bill|25-year panel lifespan|Net metering earns export credits|Panels shade roof reducing heat gain',
  'cons':'No power during grid outages|Net metering approval takes 2-6 months|Inverter replacement after 10-12 years|Requires unshaded south-facing roof',
  'tooltip_detail':'Grid-tied 3-5kWp PV. 60-80% electricity savings. File DISCOM net-metering application during construction - takes 2-6 months.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'SOL-004','category_name':'Systems','subcategory_name':'Solar',
  'name':'hybrid_pv_battery','display_name':'Hybrid Solar PV + Battery Storage','region':'South India',
  'description':'3-5 kWp grid-tied PV with 5-10 kWh lithium battery bank and hybrid inverter. Provides backup power during grid outages. Charges from solar first, grid second. Critical for areas with frequent power cuts.',
  'climate_zone':'Warm-Humid|Hot-Dry|Composite','spectrum_position':'High-Performance','sort_order':'4',
  'base_cost_per_sqft_inr':'85','installation_cost_per_sqft_inr':'18','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market rate 4kWp PV + 10kWh LFP battery + hybrid inverter Rs 3.5-4.5L; normalised per sqft; lithium prices declining',
  'expected_lifespan_years':'15','replacement_cost_factor':'0.7','major_maintenance_cycle_years':'8',
  'major_maintenance_cost_factor':'0.20','annual_minor_maint_factor':'0.02','maintenance_complexity':'Medium',
  'lifecycle_source_notes':'LFP battery cycle life 3000-4000 cycles ~10-12 years; panel 25yr; hybrid inverter 10yr',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'7','moisture_resistance':'Medium',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0.2','accessibility_score':'9',
  'thermal_source_notes':'Battery stores surplus solar. Grid draw near zero for 8-10 months. ECBC 2017 renewable credit maximised.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'South-facing roof area min 100sqft per kWp|MNRE-listed panels|Hybrid inverter (not standard string inverter)|LFP lithium battery bank|Dedicated battery room ventilated|DC cable tray|Bi-directional meter',
  'climate_restrictions':'Battery room must be ventilated and temperature-controlled. LFP batteries degrade faster above 45C — do not install in unventilated roof space in Hot-Dry zones.',
  'hard_block_rule':'None',
  'advisory_rule':'Battery room must be ventilated — do not install batteries in sealed enclosed spaces',
  'advisory_message':'Lithium batteries in enclosed unventilated spaces in South India summer (above 40C) degrade rapidly and carry thermal runaway risk. Provide dedicated ventilated space at ambient temperature.',
  'advisory_severity':'Strong-Warning','constraint_source_notes':'IEC 62619; battery manufacturer installation guide; NBC 2016 Part 8',
  'ai_advisory_notes':'The hybrid system with battery is what I recommend for anyone in areas with frequent power cuts like rural Tamil Nadu, interior Andhra Pradesh or Kerala coastal areas. The 10kWh battery gives you 8-12 hours of essential loads (fans, lights, router, phone charging, one fridge) during a grid outage charged entirely from solar. Choose lithium iron phosphate (LFP) chemistry batteries over lead acid for home use - LFP lasts 3000+ cycles (10-12 years), tolerates partial charge, and has zero maintenance. The battery room temperature matters enormously in South India summers - keep batteries below 40 degrees by installing them in a shaded ventilated room, not on the hot rooftop.',
  'pros':'Full backup power during grid outages|Solar + storage = near grid-independent|LFP battery 10-12 year life|Protects from tariff escalation',
  'cons':'High upfront cost|Battery replacement after 10-12 years|Battery room temperature management critical|More complex system than grid-tied only',
  'tooltip_detail':'Solar PV + lithium battery backup. Grid-independent operation. Ideal for frequent power cut areas. Battery room must be ventilated below 40C.',
  'status':'Active','verify_flags':'base_cost_per_sqft_inr','data_filled_by':'AI'
},
{
  'component_id':'SOL-005','category_name':'Systems','subcategory_name':'Solar',
  'name':'full_off_grid','display_name':'Full Off-Grid Solar System','region':'South India',
  'description':'Standalone PV system with large battery bank (20-30kWh), no grid connection. Sized for 100% energy self-sufficiency. Suitable for remote sites without DISCOM connection or for ultra-premium eco-conscious builds.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Premium','sort_order':'5',
  'base_cost_per_sqft_inr':'145','installation_cost_per_sqft_inr':'30','cost_confidence':'Low',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Estimate for 8kWp PV + 25kWh LFP + off-grid inverter Rs 7-10L; highly site-dependent; normalised per sqft [VERIFY]',
  'expected_lifespan_years':'20','replacement_cost_factor':'0.65','major_maintenance_cycle_years':'5',
  'major_maintenance_cost_factor':'0.25','annual_minor_maint_factor':'0.03','maintenance_complexity':'High',
  'lifecycle_source_notes':'LFP battery 10-12yr cycle; panels 25yr; off-grid inverter 10yr; generator backup 5-10yr',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'7','moisture_resistance':'Medium',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0.05','accessibility_score':'7',
  'thermal_source_notes':'Net zero carbon electricity generation on site. ECBC 2017 maximum renewable credit. Negligible grid carbon.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'High electricity demand homes above 1000 units/month without oversized system',
  'compatible_with':'All structural systems',
  'requires_component':'8-10kWp PV array|20-30kWh LFP battery bank|Off-grid pure sine inverter|Diesel or petrol generator backup|Battery management system|Remote monitoring',
  'climate_restrictions':'Monsoon period (Jun-Sep) with heavy cloud cover in Kerala and Coastal Karnataka significantly reduces generation. Generator backup mandatory for 60-90 day monsoon periods.',
  'hard_block_rule':'None',
  'advisory_rule':'Diesel generator backup mandatory for monsoon periods in high-rainfall zones',
  'advisory_message':'Full off-grid systems in Kerala or Coastal Karnataka face 60-90 days of heavy cloud cover during monsoon reducing solar generation by 50-70%. A diesel or petrol generator backup sized to charge the batteries is mandatory.',
  'advisory_severity':'Strong-Warning','constraint_source_notes':'MNRE off-grid guidelines; IEC 62109; IS 16221',
  'ai_advisory_notes':'Full off-grid solar is only justified in two situations: remote sites where DISCOM connection would cost more than the solar system itself, or high-conviction eco-projects willing to pay a premium for genuine energy independence. The economics do not stack up versus grid-tied for urban and semi-urban South India because the grid is reliable enough that batteries earning export credits in net metering give better returns than doubling battery capacity for off-grid independence. The monsoon period is the critical design challenge particularly in Kerala and Coastal Karnataka where 60-90 days of heavy cloud can cut generation to 30% of rated capacity - the battery bank and generator backup must be sized for this worst case.',
  'pros':'Complete energy independence|Zero electricity bill|Ideal for remote sites|Net zero carbon lifestyle',
  'cons':'Very high upfront cost|Complex system requiring specialist maintenance|Generator mandatory for monsoon backup|Cannot be undersized - careful energy audit required',
  'tooltip_detail':'Full off-grid solar. Remote sites only or ultra-premium builds. Generator backup mandatory for monsoon in high-rainfall zones. High complexity.',
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
