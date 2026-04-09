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

# ── LIGHTING STRATEGY (Systems) ───────────────────────────────────────────────
# Cost unit: base_cost_per_sqft_inr = INR per sqft of built-up area (whole house system)
# 5 options: Basic batten → Standard LED downlights → Layered design → Smart dimmable → Passive + solar tubes
new_rows = [
{
  'component_id':'LGT-001','category_name':'Systems','subcategory_name':'Lighting Strategy',
  'name':'basic_tube_batten','display_name':'Basic Tube Light / Batten Fitting','region':'South India',
  'description':'Surface-mounted fluorescent or LED batten fittings. Single circuit per room. No dimming or zoning. Minimum functional lighting. Common in budget residential and rental construction.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Basic','sort_order':'1',
  'base_cost_per_sqft_inr':'18','installation_cost_per_sqft_inr':'10','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'CPWD DSR 2023 electrical items; market rate Havells/Wipro LED batten 4ft; normalized per sqft 1500sqft house',
  'expected_lifespan_years':'5','replacement_cost_factor':'0.95','major_maintenance_cycle_years':'3',
  'major_maintenance_cost_factor':'0.30','annual_minor_maint_factor':'0.05','maintenance_complexity':'Low',
  'lifecycle_source_notes':'LED batten driver lifespan 15000-25000 hours; BEE India',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'5','moisture_resistance':'Low',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0.5','accessibility_score':'10',
  'thermal_source_notes':'LED battens produce minimal heat vs fluorescent. ECBC 2017 LPD 3.0 W/sqm baseline.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'False ceiling design|Recessed lighting plan',
  'compatible_with':'All structural systems',
  'requires_component':'Single-phase wiring|5A power point per fitting|Ceiling hook or batten plate',
  'climate_restrictions':'None','hard_block_rule':'None',
  'advisory_rule':'Use LED battens - not fluorescent tubes - to meet ECBC 2017 LPD requirements',
  'advisory_message':'Fluorescent tube fittings exceed ECBC 2017 Lighting Power Density limits. Specify LED batten equivalents which consume 50% less power.',
  'advisory_severity':'Info','constraint_source_notes':'ECBC 2017 Section 4.7; BEE India LPD norms',
  'ai_advisory_notes':'Basic tube light fittings are fine for a rental property or a utility space where aesthetics do not matter but they look institutional in a home. The one thing I insist on even at this budget level is LED over fluorescent - the energy saving is 50% and the LED driver lasts 3-4 times longer than a fluorescent ballast. Specify Havells or Wipro branded LED battens with at least 2-year warranty. The driver is the failure point so the warranty matters. For any room you want to feel comfortable in the long term plan at least one additional circuit for task lighting near work surfaces.',
  'pros':'Lowest cost lighting system|No electrician needed to replace lamp|Universally serviceable|LED versions very energy efficient',
  'cons':'Institutional appearance|Single harsh top-down light source|No dimming or ambience control|Driver failures frequent in cheap brands',
  'tooltip_detail':'Basic LED batten fittings. Functional and economical. Fine for rental or utility spaces. Use LED not fluorescent for ECBC compliance.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'LGT-002','category_name':'Systems','subcategory_name':'Lighting Strategy',
  'name':'led_downlights_standard','display_name':'Standard LED Downlights + Ceiling Fans','region':'South India',
  'description':'Recessed LED downlights (7-12W) in false ceiling grid with fan provision in every room. Two lighting circuits per room: general downlights and perimeter/task. Most common mid-range residential lighting in South India.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Standard','sort_order':'2',
  'base_cost_per_sqft_inr':'45','installation_cost_per_sqft_inr':'18','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market rate Philips/Wipro/Havells LED downlights + wiring; normalized per sqft including 2-circuit layout',
  'expected_lifespan_years':'8','replacement_cost_factor':'0.85','major_maintenance_cycle_years':'5',
  'major_maintenance_cost_factor':'0.20','annual_minor_maint_factor':'0.03','maintenance_complexity':'Low',
  'lifecycle_source_notes':'LED driver lifespan 25000-30000 hours; Philips warranty 3yr',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'6','moisture_resistance':'Low',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0.4','accessibility_score':'9',
  'thermal_source_notes':'Recessed LEDs produce minimal heat. ECBC 2017 LPD 2.5 W/sqm achievable.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'Rooms without false ceiling',
  'compatible_with':'All structural systems with false ceiling',
  'requires_component':'False ceiling (min 4-inch recess depth)|2 circuits per room|Fan hook sleeve in slab|ISI LED driver rated fittings',
  'climate_restrictions':'IP44 rated downlights mandatory in bathrooms and outdoor covered areas.',
  'hard_block_rule':'REQUIRES_FALSE_CEILING',
  'advisory_rule':'Use IP44-rated downlights in bathrooms - standard downlights are not moisture-safe',
  'advisory_message':'Standard open-back LED downlights installed in bathroom false ceilings create an electrocution risk from steam and condensation. IP44 moisture-rated fittings are mandatory.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 10322; NBC 2016 Part 8; ECBC 2017',
  'ai_advisory_notes':'LED downlights in a false ceiling is the standard I recommend for most South India homes because it gives a clean modern look with good light distribution. The key decisions are color temperature and placement. Warm white 2700-3000K feels comfortable in bedrooms and living areas while cool white 4000-4500K works better in kitchens and study areas. Space downlights at 1.5 to 2 times the ceiling height from walls so the light covers the walls evenly. A very common mistake is placing all downlights in a central grid which creates a brightly lit centre and dark gloomy corners. Always have a separate circuit for perimeter or feature lighting that you can switch independently for evening ambience.',
  'pros':'Clean modern look|Good light distribution with correct placement|Energy efficient LEDs|Easy lamp replacement',
  'cons':'Requires false ceiling|Creates holes that reduce acoustic and thermal performance|Single colour temperature per fitting|No dimming without additional investment',
  'tooltip_detail':'Standard LED downlights in false ceiling. Space at 1.5x ceiling height from walls. IP44 in bathrooms. Separate circuit for perimeter lighting.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'LGT-003','category_name':'Systems','subcategory_name':'Lighting Strategy',
  'name':'layered_lighting_design','display_name':'Layered Lighting Design (Ambient + Task + Accent)','region':'South India',
  'description':'Three-layer lighting design: ambient (downlights/cove), task (under-cabinet, reading, workdesk), and accent (feature wall, art, landscape). Separate switching circuits for each layer. Designed by lighting consultant or architect.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Performance','sort_order':'3',
  'base_cost_per_sqft_inr':'90','installation_cost_per_sqft_inr':'35','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market rate including cove LED strips + downlights + task fittings + 3-circuit wiring per room; Bangalore premium contractor',
  'expected_lifespan_years':'10','replacement_cost_factor':'0.80','major_maintenance_cycle_years':'5',
  'major_maintenance_cost_factor':'0.20','annual_minor_maint_factor':'0.03','maintenance_complexity':'Medium',
  'lifecycle_source_notes':'LED strip lifespan 20000-35000 hours; downlight driver 25000h',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'6','moisture_resistance':'Low',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0.35','accessibility_score':'8',
  'thermal_source_notes':'Lower wattage distributed lighting reduces heat gain vs single high-wattage sources. ECBC 2017 LPD 2.0 W/sqm achievable.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'Rooms without false ceiling (cove lighting not possible)',
  'compatible_with':'All structural systems with false ceiling',
  'requires_component':'False ceiling with cove recess detail|3 independent circuits per room|LED strip channels for cove|Under-cabinet LED fittings|Separate DB circuits',
  'climate_restrictions':'LED strip drivers must be rated for 45C ambient in Hot-Dry zones - South India summer temps stress drivers in enclosed cove spaces.',
  'hard_block_rule':'REQUIRES_FALSE_CEILING',
  'advisory_rule':'LED strip driver must be accessible for replacement - do not enclose in sealed cove',
  'advisory_message':'LED strip drivers fail before the strip itself. If the driver is sealed inside an inaccessible cove the entire strip assembly must be demolished and reinstalled. Design the cove with an access panel.',
  'advisory_severity':'Warning','constraint_source_notes':'LED manufacturer installation guide; IS 10322',
  'ai_advisory_notes':'Layered lighting transforms a house from a functional space into a home that feels genuinely comfortable at any time of day or evening. The concept is simple: ambient light for general visibility, task light exactly where you need to see detail like the kitchen counter or the reading chair, and accent light to highlight architectural features or artwork. The wiring change from standard is minimal - just run 3 circuits instead of 1 to each room. Plan the cove detail in the false ceiling drawings before the ceiling is built because retrofitting a cove is expensive. The LED driver location is the most common oversight - put them in an accessible location like inside a wardrobe or behind an access panel not buried in concrete.',
  'pros':'Transforms room atmosphere dramatically|Lower total energy than single bright source|Hides harsh point sources|Supports different moods for different activities',
  'cons':'Requires careful planning before construction|LED strip drivers need accessible location|Higher design and wiring cost|Cove detail adds to false ceiling complexity',
  'tooltip_detail':'Three-layer ambient + task + accent lighting. Plan cove and wiring before false ceiling is built. Driver must be accessible for replacement.',
  'status':'Active','verify_flags':'base_cost_per_sqft_inr','data_filled_by':'AI'
},
{
  'component_id':'LGT-004','category_name':'Systems','subcategory_name':'Lighting Strategy',
  'name':'smart_dimmable_lighting','display_name':'Smart Dimmable LED System','region':'South India',
  'description':'Full dimmable LED system with smart switches or DALI/Zigbee-controlled drivers. App, voice and scene control. Occupancy sensor auto-off. Energy metering per circuit. Integrates with home automation.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'High-Performance','sort_order':'4',
  'base_cost_per_sqft_inr':'145','installation_cost_per_sqft_inr':'50','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market rate Legrand/Philips Hue/Lutron Caedra dimmable system + occupancy sensors; Bangalore smart home installer',
  'expected_lifespan_years':'10','replacement_cost_factor':'0.75','major_maintenance_cycle_years':'5',
  'major_maintenance_cost_factor':'0.25','annual_minor_maint_factor':'0.04','maintenance_complexity':'High',
  'lifecycle_source_notes':'Smart driver and sensor replacement cycle 7-10 years; IS 10322',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'6','moisture_resistance':'Low',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0.25','accessibility_score':'10',
  'thermal_source_notes':'Dimming reduces wattage proportionally - 50% dim = ~50% energy. Occupancy auto-off eliminates standby waste. ECBC 2017 LPD 1.5 W/sqm achievable.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems with false ceiling',
  'requires_component':'Neutral wire at every switch point|Dimmable LED drivers (not standard)|Zigbee or WiFi smart switches|Stable WiFi or mesh network|Home automation hub optional',
  'climate_restrictions':'None','hard_block_rule':'None',
  'advisory_rule':'All LED fittings must use dimmable drivers - standard LED drivers buzz or flicker when dimmed',
  'advisory_message':'Standard (non-dimmable) LED drivers buzz loudly and flicker when connected to a dimmer switch. Specify dimmable-compatible drivers explicitly for every fitting.',
  'advisory_severity':'Warning','constraint_source_notes':'Philips/Legrand compatibility guide; IS 10322',
  'ai_advisory_notes':'Smart dimmable lighting is the highest quality lighting upgrade and genuinely changes daily life. Waking up to a gradually brightening light, movie mode where all lights dim to 10%, occupancy sensors that turn off the corridor light you always forget - these are real daily benefits. The technical prerequisite that catches most people is the neutral wire at switch points which standard Indian wiring omits, and the dimmable driver specification for every fitting. A regular LED driver connected to a dimmer switch will buzz irritatingly. Specify dimmable-rated drivers from Philips or Havells for every single downlight and strip driver in the system.',
  'pros':'30-50% energy saving through dimming and auto-off|Voice and app scene control|Gradual wake-up and sunset scenes|Occupancy auto-off eliminates waste',
  'cons':'Highest lighting system cost|All drivers must be dimmable-rated - easy to get wrong|Neutral wire required at switch points|Smart devices obsolete in 8-10 years',
  'tooltip_detail':'Smart dimmable LEDs with occupancy sensors. All drivers must be dimmable-rated. Neutral wire at switch points mandatory. 30-50% energy saving.',
  'status':'Active','verify_flags':'base_cost_per_sqft_inr','data_filled_by':'AI'
},
{
  'component_id':'LGT-005','category_name':'Systems','subcategory_name':'Lighting Strategy',
  'name':'passive_daylighting_solar_tubes','display_name':'Passive Daylighting + Solar Tubes','region':'South India',
  'description':'Architectural daylighting strategy: sun-path optimised window placement, light shelves, and tubular daylighting devices (solar tubes) to bring natural light into interior rooms. Reduces artificial lighting need by 40-70% in daytime.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'High-Performance','sort_order':'5',
  'base_cost_per_sqft_inr':'35','installation_cost_per_sqft_inr':'25','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market rate Solatube/Velux solar tubes + light shelf design premium; averaged over floor area',
  'expected_lifespan_years':'25','replacement_cost_factor':'0.6','major_maintenance_cycle_years':'10',
  'major_maintenance_cost_factor':'0.08','annual_minor_maint_factor':'0.01','maintenance_complexity':'Low',
  'lifecycle_source_notes':'Solatube 10-year warranty; roof dome 20-25 year lifespan; BRE Digest 345',
  'thermal_resistance_score':'3','acoustic_score':'1','durability_score':'8','moisture_resistance':'High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0.0','accessibility_score':'9',
  'thermal_source_notes':'Solar tubes admit daylight not direct solar heat - diffuser dome filters IR. ECBC 2017 daylight credit applicable. No heat addition to space.',
  'max_floors_supported':'2','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'Underground or basement rooms|Apartments not on top floor',
  'compatible_with':'Ground floor and top floor of all structural systems with accessible roof',
  'requires_component':'Roof access for dome installation|350-550mm diameter roof penetration|Flashing and weatherproofing at penetration|Reflective tube from roof to ceiling diffuser',
  'climate_restrictions':'In high-rainfall coastal zones ensure roof penetration flashing is watertight. Solar tubes must be installed by certified installer to prevent roof leaks.',
  'hard_block_rule':'BLOCK_IN_APARTMENTS_BELOW_TOP_FLOOR',
  'advisory_rule':'Roof penetration must be flashed and waterproofed by certified installer',
  'advisory_message':'Solar tube roof penetrations that are not properly flashed and sealed will leak during monsoon. Use only certified Solatube or Velux installers.',
  'advisory_severity':'Warning','constraint_source_notes':'ECBC 2017 daylighting credits; NBC 2016; Solatube installation guide',
  'ai_advisory_notes':'Passive daylighting is the most underused strategy in South India residential construction. Simply orienting the main living areas to face north and east gives beautiful soft diffuse light all day without glare or heat gain while west-facing rooms get the brutal afternoon sun. Solar tubes are brilliant for dark interior bathrooms and corridors that otherwise need artificial lighting all day - a 350mm tube brings in as much light as three 100-watt bulbs at zero ongoing electricity cost. The roof penetration must be done by a certified installer because a badly flashed solar tube is a guaranteed roof leak. Works best on ground floor rooms and the top floor - middle floors of multi-storey cannot use them.',
  'pros':'Zero electricity cost for daytime lighting|Natural light quality incomparable to artificial|25-year lifespan|Reduces AC load - no heat from artificial lights',
  'cons':'Only works on top floor or ground floor|Cannot be used in multi-storey middle floors|Requires roof penetration - leak risk if poorly done|Cannot replace night lighting',
  'tooltip_detail':'Solar tubes bring natural daylight into dark interior rooms. Zero running cost. Top floor and ground floor only. Certified installer for leak-free installation.',
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
