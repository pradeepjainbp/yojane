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

# ── ELECTRICAL (Systems) ──────────────────────────────────────────────────────
# Cost unit: base_cost_per_sqft_inr = INR per sqft of built-up area (whole house system cost)
# 4 options: Basic → Standard → Performance → Premium (Solar-ready)
new_rows = [
{
  'component_id':'ELEC-001','category_name':'Systems','subcategory_name':'Electrical',
  'name':'basic_concealed_wiring','display_name':'Basic Concealed Wiring (ISI PVC)','region':'South India',
  'description':'Standard concealed copper wiring in PVC conduit with ISI-marked single-core cables. Provides essential circuits: lights, fans, power points and AC provisions. Minimum code-compliant installation per IE Rules and IS 732.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Basic','sort_order':'1',
  'base_cost_per_sqft_inr':'75','installation_cost_per_sqft_inr':'35','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'CPWD DSR 2023 electrical items; Karnataka PWD SOR 2024-25; Bangalore/Chennai contractor rate for 1500 sqft house normalized per sqft',
  'expected_lifespan_years':'25','replacement_cost_factor':'0.9','major_maintenance_cycle_years':'10',
  'major_maintenance_cost_factor':'0.15','annual_minor_maint_factor':'0.01','maintenance_complexity':'Low',
  'lifecycle_source_notes':'IS 732; IE Rules 1956; BEE India electrical standards',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'6','moisture_resistance':'Medium',
  'fire_rating':'Class B','energy_impact_modifier':'1.0','accessibility_score':'9',
  'thermal_source_notes':'No thermal contribution. Standard copper conductors. ECBC 2017 Section 4 lighting power density baseline.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'ISI marked FRLS copper cables|PVC rigid conduit|MCB distribution board|Earthing electrode',
  'climate_restrictions':'In coastal areas all MS conduit must be replaced with PVC - moisture causes rapid rust of metal conduit.',
  'hard_block_rule':'None',
  'advisory_rule':'Use only ISI-marked FRLS (flame-retardant low-smoke) cables - not bare PVC',
  'advisory_message':'Non-ISI cables and bare PVC (non-FRLS) are a fire risk. IS 694 FRLS cables are mandatory for all concealed wiring.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 732; IS 694; IE Rules 1956; NBC 2016 Part 8',
  'ai_advisory_notes':'Basic concealed wiring is what every house gets and most people never think about it until something goes wrong. The quality of cable is everything - I cannot stress this enough. Use only ISI-marked FRLS copper cables from companies like Havells Finolex or Polycab. Never let your electrician use cheap unbranded wire because it will fail in 5-7 years and you cannot repair concealed wiring without breaking walls. Specify 2.5 sqmm copper for all power points and AC points - contractors often downgrade to 1.5 sqmm to save money which overheats with modern high-wattage appliances. Earthing is safety critical - insist on three separate earth points going to a proper copper earth electrode.',
  'pros':'Lowest cost electrical system|Code compliant|Easy to get maintenance|Universal contractor availability',
  'cons':'Minimum specification - no future-proofing|Cannot easily add circuits later|Basic switch plates only|No energy monitoring',
  'tooltip_detail':'Standard concealed copper wiring meeting IE Rules minimum. Use ISI-marked FRLS cables only. Upgrade conduit sizing for future-proofing.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'ELEC-002','category_name':'Systems','subcategory_name':'Electrical',
  'name':'modular_switches_upgraded','display_name':'Upgraded Wiring + Modular Switches','region':'South India',
  'description':'Concealed copper wiring with larger conduit (25mm vs 20mm), heavier gauge cables, RCCB protection per circuit, and branded modular switch plates (Legrand/Schneider/Anchor Roma). Enhanced safety and aesthetics over basic.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Standard','sort_order':'2',
  'base_cost_per_sqft_inr':'120','installation_cost_per_sqft_inr':'45','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market rate including Legrand Myrius or Schneider Acti9 MCBs + RCCB; Havells/Finolex cables; normalized per sqft',
  'expected_lifespan_years':'30','replacement_cost_factor':'0.85','major_maintenance_cycle_years':'10',
  'major_maintenance_cost_factor':'0.12','annual_minor_maint_factor':'0.01','maintenance_complexity':'Low',
  'lifecycle_source_notes':'IS 732; manufacturer data; IE Rules',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'7','moisture_resistance':'Medium',
  'fire_rating':'Class B','energy_impact_modifier':'1.0','accessibility_score':'9',
  'thermal_source_notes':'No thermal contribution. Higher gauge conductors run cooler under load. ECBC 2017.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'ISI FRLS 4sqmm copper cables for power|25mm PVC conduit|RCCB per circuit|Modular switch plates|MCB+ELCB main DB',
  'climate_restrictions':'In coastal zones use marine-grade switch plates and seal conduit entry points with silicone.',
  'hard_block_rule':'None',
  'advisory_rule':'Install RCCB (30mA) on every wet area circuit - bathrooms kitchen and outdoor points',
  'advisory_message':'An RCCB (Residual Current Circuit Breaker) on bathroom circuits can prevent fatal electrocution. This is non-negotiable for any house with children.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 12640; IE Rules Rule 41; NBC 2016 Part 8',
  'ai_advisory_notes':'The upgrade from basic wiring to modular switches costs only 30-40% more but transforms both safety and aesthetics. The key upgrades are RCCB (residual current breaker) protection on bathroom and outdoor circuits which is critical for safety - I have personally seen two instances of electrocution in bathrooms that RCCBs would have prevented. Use Legrand Myrius or Schneider Acti9 for the MCBs in the distribution board because local brands trip unreliably. Specify 25mm conduit instead of 20mm even for lighting circuits so you can pull additional wires later without breaking walls.',
  'pros':'RCCB protection dramatically improves safety|Better aesthetics with modular plates|Larger conduit allows future circuit addition|30-year cable lifespan',
  'cons':'Higher cost than basic|Modular switches slightly more complex to replace locally|Still no remote control or energy monitoring',
  'tooltip_detail':'Enhanced wiring with RCCB protection, larger conduit and modular switch plates. RCCB on all wet area circuits is a safety essential.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'ELEC-003','category_name':'Systems','subcategory_name':'Electrical',
  'name':'home_automation_partial','display_name':'Partial Home Automation (Smart Switches)','region':'South India',
  'description':'Standard concealed wiring backbone upgraded with WiFi-enabled smart switch modules for lights and fans. App and voice control (Alexa/Google Home). Energy monitoring dashboard. No structural change required.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Performance','sort_order':'3',
  'base_cost_per_sqft_inr':'185','installation_cost_per_sqft_inr':'55','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market rate Legrand BTicino/Orvibo/Wipro Smart switches + wiring upgrade; normalized per sqft for 2000 sqft house',
  'expected_lifespan_years':'15','replacement_cost_factor':'0.8','major_maintenance_cycle_years':'5',
  'major_maintenance_cost_factor':'0.20','annual_minor_maint_factor':'0.03','maintenance_complexity':'High',
  'lifecycle_source_notes':'Smart device replacement cycle 5-8 years; wiring backbone 25 years; IS 732',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'6','moisture_resistance':'Medium',
  'fire_rating':'Class B','energy_impact_modifier':'0.85','accessibility_score':'10',
  'thermal_source_notes':'Smart controls reduce energy use by 15-20% through schedules and occupancy detection. ECBC 2017 LPD compliance improved.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'Neutral wire at every switch point (mandatory for smart switches)|Stable WiFi throughout house|Smart home hub or direct cloud|RCCB protection',
  'climate_restrictions':'None','hard_block_rule':'None',
  'advisory_rule':'Neutral wire at switch point is mandatory for smart switches - plan this in wiring layout',
  'advisory_message':'Standard Indian wiring often omits the neutral wire at switch boxes. Smart switches require neutral at the switch point. This must be specified to the electrician before wiring starts - retrofitting is very expensive.',
  'advisory_severity':'Strong-Warning','constraint_source_notes':'Smart switch manufacturer wiring requirements; IS 732',
  'ai_advisory_notes':'Smart home systems are genuinely useful in South India because you can schedule lights and fans to cut electricity bills and control everything when you are away from home. The single most important thing to plan before your electrician starts is to specify that every switch point must have a neutral wire brought to it. Standard Indian practice omits the neutral at the switch box and most smart switches require it. Retrofitting neutral wires to existing wiring means breaking open concealed conduit which is very expensive. Also run solid stable WiFi through the house before commissioning smart switches - intermittent WiFi makes smart switches unreliable and frustrating.',
  'pros':'App and voice control from anywhere|Energy monitoring reduces electricity bills|Scenes and schedules|Accessible for elderly',
  'cons':'Requires neutral at every switch point - must plan from start|WiFi reliability critical|Smart devices obsolete in 7-10 years|Expensive repair if one module fails',
  'tooltip_detail':'WiFi smart switches on standard wiring backbone. Must specify neutral wire at switch points before wiring starts. Good for energy saving.',
  'status':'Active','verify_flags':'base_cost_per_sqft_inr','data_filled_by':'AI'
},
{
  'component_id':'ELEC-004','category_name':'Systems','subcategory_name':'Electrical',
  'name':'solar_ready_wiring','display_name':'Solar-Ready Wiring + Full Automation','region':'South India',
  'description':'Premium full electrical system designed for rooftop solar integration: dedicated solar DB panel, string inverter mounting provisions, bi-directional net-metering capable meter, heavy gauge cables, full home automation, and 3-phase supply.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Premium','sort_order':'4',
  'base_cost_per_sqft_inr':'280','installation_cost_per_sqft_inr':'75','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market rate for full solar-ready electrical layout + 3-phase metering + automation; MNRE approved installer rates South India',
  'expected_lifespan_years':'25','replacement_cost_factor':'0.8','major_maintenance_cycle_years':'8',
  'major_maintenance_cost_factor':'0.15','annual_minor_maint_factor':'0.02','maintenance_complexity':'High',
  'lifecycle_source_notes':'IS 732; MNRE solar installation guidelines; solar panel warranty 25 years; inverter 10 years',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'7','moisture_resistance':'Medium',
  'fire_rating':'Class B','energy_impact_modifier':'0.5','accessibility_score':'9',
  'thermal_source_notes':'Solar generation offsets grid draw by 30-80% depending on panel area. ECBC 2017 energy performance compliance significantly improved.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems with flat or low-slope roof',
  'requires_component':'3-phase DISCOM meter connection|Dedicated solar distribution board|DC cable trays from roof to inverter|MNRE-approved bi-directional meter|Earthing and lightning protection',
  'climate_restrictions':'Solar panels require south-facing roof area (minimum 100 sqft per kWp). Coastal areas need marine-grade connectors and mounting hardware.',
  'hard_block_rule':'None',
  'advisory_rule':'Register for net-metering with DISCOM before solar installation - approval takes 2-6 months',
  'advisory_message':'Net-metering approval from TANGEDCO/BESCOM/KSEB must be obtained before energising the solar system. Applications typically take 2-6 months in South India. Start the process during construction.',
  'advisory_severity':'Warning','constraint_source_notes':'MNRE Net Metering Regulations; TANGEDCO/BESCOM/KSEB utility guidelines',
  'ai_advisory_notes':'Designing your electrical system as solar-ready from day one costs only 15-20% more than standard but saves you a major retrofit when you add solar panels later. The provisions needed are: a dedicated DC cable tray from rooftop to inverter location, an additional distribution board for the solar circuits, and a 3-phase connection request to your DISCOM at the construction stage. South India has among the highest solar irradiance in the country - Hyderabad Chennai Bangalore and coastal AP all get 5.0-5.8 kWh/m2/day. A 3 kWp system on a 1500 sqft house typically covers 60-80% of electricity consumption. File for net-metering with BESCOM or TANGEDCO as soon as construction begins because approvals take 3-6 months.',
  'pros':'Solar offsets 60-80% of electricity bill|Net-metering earns export credits|Future-proofed for battery storage|3-phase enables EV charging and heavy equipment',
  'cons':'Highest upfront electrical cost|DISCOM net-metering approval takes months|Requires south-facing roof area|Inverter replacement cost after 10 years',
  'tooltip_detail':'Premium solar-integrated electrical system. File net-metering application with DISCOM during construction. Saves 60-80% electricity costs.',
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
