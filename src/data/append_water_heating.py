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
  'component_id':'WH-001','category_name':'Systems','subcategory_name':'Water Heating',
  'name':'water_heating_electric_geyser','display_name':'Electric Storage Geyser','region':'South India',
  'description':'Electric resistance water heater (storage geyser) of 15-25 litre capacity per bathroom. Most common water heating solution in India. Low upfront cost, high running cost. Energy efficiency depends on BEE star rating.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Basic','sort_order':'1',
  'base_cost_per_sqft_inr':'3','installation_cost_per_sqft_inr':'2','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Racold/Havells/AO Smith geyser market rate 2024; normalized per sqft built-up area',
  'expected_lifespan_years':'8','replacement_cost_factor':'0.9','major_maintenance_cycle_years':'3',
  'major_maintenance_cost_factor':'0.15','annual_minor_maint_factor':'0.02','maintenance_complexity':'Low',
  'lifecycle_source_notes':'Geyser heating element lifespan 6-10 years; tank lifespan 10-15 years',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'5','moisture_resistance':'Medium',
  'fire_rating':'Non-Rated','energy_impact_modifier':'-0.2','accessibility_score':'10',
  'thermal_source_notes':'2-3 kWh electricity per day per bathroom. Highest energy consumption of all heating options.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All bathroom configurations',
  'requires_component':'15A socket with ISI mark|Separate MCB for each geyser|Earth leakage protection (ELCB/RCCB)',
  'climate_restrictions':'None',
  'hard_block_rule':'None',
  'advisory_rule':'Mandatory ELCB (Earth Leakage Circuit Breaker) for all bathroom geyser circuits',
  'advisory_message':'Geyser without ELCB protection is a serious electrical safety risk in wet bathroom conditions. Every geyser circuit must have ELCB/RCCB protection. This is a legal requirement under NBC.',
  'advisory_severity':'Strong-Warning','constraint_source_notes':'NBC 2016; IS 8884; BEE star rating',
  'ai_advisory_notes':'Electric geysers are the default because they are cheapest upfront and every electrician and plumber knows how to install them but the running cost story is poor. A 15-litre geyser draws 2 kW and takes 15-20 minutes to heat a tank - that is 0.5 kWh per hot bath. For a family of 4 taking daily hot baths that is 2 kWh per day or roughly Rs 12-16 per day at BESCOM rates totalling Rs 4500-5500 per year just for water heating. Over 20 years that is Rs 90000-110000 in electricity costs. A solar water heater at Rs 25000 upfront pays back in 4-5 years and then provides effectively free hot water for 20+ years. The only advantage of the electric geyser in South India is that it is the backup for cloudy monsoon periods. I recommend electric geysers only as backup to solar or heat pump systems not as the primary water heating choice.',
  'pros':'Lowest upfront cost|Simple installation|Wide availability and service|No weather dependency|Instant hot water after heat-up period',
  'cons':'Highest running cost of all options|2 kW power draw per unit|Safety risk without ELCB protection|8-10 year lifespan|Not suitable as primary heater for South India',
  'tooltip_detail':'Electric geyser. Lowest upfront cost, highest running cost. ELCB mandatory. Use as backup to solar, not primary heating.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'WH-002','category_name':'Systems','subcategory_name':'Water Heating',
  'name':'water_heating_gas_geyser','display_name':'Gas Geyser (LPG/PNG)','region':'South India',
  'description':'Instantaneous gas water heater using LPG or Piped Natural Gas (PNG). Provides continuous hot water without storage. Lower running cost than electric geyser. Suitable where PNG connection is available (expanding in Bangalore and Chennai).',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Intermediate','sort_order':'2',
  'base_cost_per_sqft_inr':'5','installation_cost_per_sqft_inr':'3','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Gas geyser market rate 2024; normalized per sqft',
  'expected_lifespan_years':'12','replacement_cost_factor':'0.8','major_maintenance_cycle_years':'5',
  'major_maintenance_cost_factor':'0.1','annual_minor_maint_factor':'0.01','maintenance_complexity':'Medium',
  'lifecycle_source_notes':'Gas geyser heat exchanger lifespan 10-15 years',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'6','moisture_resistance':'Medium',
  'fire_rating':'Non-Rated','energy_impact_modifier':'-0.1','accessibility_score':'9',
  'thermal_source_notes':'Lower carbon emission per unit heat than electric geyser where grid is coal-powered.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All bathroom configurations|PNG or LPG connection',
  'requires_component':'PNG connection (preferred) or LPG cylinder|Gas pipe with ball valve|Flue vent to outside|CO detector',
  'climate_restrictions':'None',
  'hard_block_rule':'None',
  'advisory_rule':'Gas geyser must be installed with external flue and never in an enclosed bathroom without ventilation',
  'advisory_message':'Gas geysers produce combustion gases including CO. Installation in an enclosed bathroom without proper external flue ventilation is a fatal risk. External wall installation with flue mandatory.',
  'advisory_severity':'Strong-Warning','constraint_source_notes':'IS 6993; BIS gas appliance safety; NBC 2016',
  'ai_advisory_notes':'Gas geysers make sense in areas where Piped Natural Gas connection is available and the running cost advantage over electric is real - PNG at current rates gives hot water at roughly 40-50 percent the cost of electric heating. The PNG network is expanding in Bangalore through GAIL and in Chennai through IGL. The safety requirement that cannot be compromised is the external flue - gas combustion produces carbon monoxide and a gas geyser in an enclosed bathroom without a proper outside flue has killed people. The geyser must be mounted on an external wall with the flue pipe going directly outside. Never install in a bathroom with no external wall. Install a CO detector as well. For LPG operation the running cost advantage narrows considerably because LPG is significantly more expensive than PNG.',
  'pros':'Lower running cost than electric (PNG)|Instant continuous hot water - no storage needed|No electricity dependency|Better than electric for large families|Faster flow rate',
  'cons':'PNG connection required for cost advantage|Safety risk without external flue - fatal if incorrectly installed|CO detector mandatory|LPG variant loses cost advantage|Not suitable for enclosed bathrooms',
  'tooltip_detail':'Gas geyser. Lower cost with PNG. External flue and CO detector mandatory. Never install in enclosed bathroom.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'WH-003','category_name':'Systems','subcategory_name':'Water Heating',
  'name':'water_heating_solar','display_name':'Solar Water Heater','region':'South India',
  'description':'Flat plate or evacuated tube solar water heater system. 100-200 litre capacity on rooftop. Best suited for South India where annual solar radiation is very high (5.5-6.5 kWh/sqm/day). 4-5 year payback, effective for 20+ years.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate','spectrum_position':'Performance','sort_order':'3',
  'base_cost_per_sqft_inr':'12','installation_cost_per_sqft_inr':'6','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Racold/AO Smith/V-Guard solar system market rate Bangalore/Chennai 2024; 150L ETC system; normalized per sqft',
  'expected_lifespan_years':'20','replacement_cost_factor':'0.6','major_maintenance_cycle_years':'5',
  'major_maintenance_cost_factor':'0.1','annual_minor_maint_factor':'0.005','maintenance_complexity':'Low',
  'lifecycle_source_notes':'MNRE solar water heater performance data; 20-25 year system lifespan; collector 15 years',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'8','moisture_resistance':'High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0.2','accessibility_score':'9',
  'thermal_source_notes':'Provides 70-80% of annual water heating from solar. Backup geyser needed for monsoon months only.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All bathroom configurations|Backup electric geyser',
  'requires_component':'Rooftop space (2-3 sqm per 100L)|Insulated storage tank|Backup electric element for monsoon|MNRE approved system',
  'climate_restrictions':'Best performance in Hot-Dry and Warm-Humid zones. Evacuated tube collector performs better in cloudy conditions than flat plate.',
  'hard_block_rule':'None',
  'advisory_rule':'Use evacuated tube collector (ETC) not flat plate in high-humidity zones for better monsoon performance',
  'advisory_message':'In high-humidity zones like coastal Karnataka and Kerala evacuated tube collectors perform significantly better on partly cloudy days than flat plate collectors. Specify ETC type for coastal and high-rainfall locations.',
  'advisory_severity':'Warning','constraint_source_notes':'MNRE JNNSM guidelines; IS 12933',
  'ai_advisory_notes':'Solar water heating is the best financial decision you can make for water heating in South India. Bangalore gets 300+ sunny days a year and solar radiation is excellent even in the so-called rainy season because it is rarely fully overcast for more than 2-3 consecutive days. A 150 litre ETC solar water heater system from Racold or AO Smith costs around Rs 18000-22000 installed and eliminates 70-80 percent of your water heating electricity bill. The payback is 4-5 years and then you have free hot water for 15-20 more years. The only maintenance needed is an annual cleaning of the collector tubes which takes 30 minutes. The backup electric element in the tank handles the monsoon cloudy periods. Get an MNRE approved system to be eligible for the BESCOM solar subsidy. Install it before your roof is finished because routing the pipes is much easier before the false ceiling is done.',
  'pros':'4-5 year payback then free hot water|Best for South India solar radiation|20 year system lifespan|70-80% energy saving|MNRE subsidy eligible|ECBC compliance pathway',
  'cons':'Requires rooftop space and structural capacity|Performance reduced in cloudy monsoon periods (backup needed)|Roof plumbing must be planned early|Slightly less effective in very high rainfall zones',
  'tooltip_detail':'Solar water heater. Best choice for South India. 4-5 year payback. Use ETC type. Install before roof finishing.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'WH-004','category_name':'Systems','subcategory_name':'Water Heating',
  'name':'water_heating_heat_pump','display_name':'Heat Pump Water Heater','region':'South India',
  'description':'Heat pump water heater using ambient air as heat source. COP (Coefficient of Performance) of 3-4 meaning 3-4 kWh of heat for every 1 kWh of electricity. 60-70% energy saving versus electric geyser. Premium upfront cost with 5-7 year payback.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Premium','sort_order':'4',
  'base_cost_per_sqft_inr':'20','installation_cost_per_sqft_inr':'10','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Daikin/Racold heat pump market rate South India 2024; normalized per sqft',
  'expected_lifespan_years':'15','replacement_cost_factor':'0.7','major_maintenance_cycle_years':'3',
  'major_maintenance_cost_factor':'0.12','annual_minor_maint_factor':'0.01','maintenance_complexity':'Medium',
  'lifecycle_source_notes':'Heat pump compressor lifespan 12-18 years; tank 15-20 years',
  'thermal_resistance_score':'5','acoustic_score':'4','durability_score':'7','moisture_resistance':'Medium',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0.3','accessibility_score':'9',
  'thermal_source_notes':'COP 3-4: delivers 3-4 kWh heat per kWh electricity consumed. 60-70% saving vs resistive geyser.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All bathroom configurations',
  'requires_component':'Outdoor unit location with good air circulation|Condensate drain|15A dedicated circuit|Annual refrigerant check service',
  'climate_restrictions':'Performance reduces below 10°C ambient - not an issue for most South India locations. Best in warm humid conditions.',
  'hard_block_rule':'None',
  'advisory_rule':'Install in location with good air circulation - enclosed spaces reduce performance significantly',
  'advisory_message':'Heat pump water heaters need good ambient air flow around the unit. Installing in an enclosed utility room or store restricts airflow and significantly reduces efficiency. Place in a ventilated external location.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 15195; heat pump manufacturer installation guidelines',
  'ai_advisory_notes':'Heat pump water heaters are the premium technology choice and they make particularly good sense in South India because the warm ambient temperatures year-round give the heat pump excellent operating conditions. A heat pump extracts heat from the ambient air and transfers it to water rather than generating heat from electricity directly - this gives a COP of 3 to 4 meaning you get 3 to 4 kilowatts of heat for every kilowatt of electricity. Compared to a 2 kW resistive geyser a heat pump does the same job using 500-700 watts. Over 20 years this difference pays back the premium cost approximately 5 times. The downside is that it requires annual maintenance of the refrigerant circuit - you need a trained HVAC technician similar to what you use for a split AC. Also the unit makes a sound similar to a small AC outdoor unit so it cannot be placed directly outside a bedroom window. For premium construction where energy efficiency is a priority and the owner wants to reduce both electricity bills and carbon footprint the heat pump is the clear choice.',
  'pros':'60-70% energy saving versus electric geyser|Best for warm South India ambient conditions|Works at all hours unlike solar|Premium eco-friendly choice|Long lifespan|ECBC compliance pathway',
  'cons':'Highest upfront cost|Annual refrigerant maintenance needed|Makes noise like AC outdoor unit|Enclosed installation reduces performance|5-7 year payback longer than solar',
  'tooltip_detail':'Heat pump water heater. 60-70% energy saving. Place in ventilated location. Annual refrigerant service needed. 5-7 year payback.',
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
