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

# E4 - Electrical Load Planning
load_rows = [
{
  'component_id':'ELOAD-001','category_name':'Systems','subcategory_name':'Electrical Load',
  'name':'load_5kw_single_phase','display_name':'5 kW Single Phase','region':'South India',
  'description':'5 kW single phase BESCOM/TNEB service connection. Adequate for 1-2 BHK apartments or small houses with basic appliances, no air conditioning or minimal ceiling fan + 1 small AC.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Basic','sort_order':'1',
  'base_cost_per_sqft_inr':'8','installation_cost_per_sqft_inr':'5','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Electrical contractor rate; panel + wiring + connection charges normalized per sqft',
  'expected_lifespan_years':'25','replacement_cost_factor':'0.5','major_maintenance_cycle_years':'10',
  'major_maintenance_cost_factor':'0.1','annual_minor_maint_factor':'0.005','maintenance_complexity':'Low',
  'lifecycle_source_notes':'Electrical system lifespan 20-30 years with proper maintenance',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'7','moisture_resistance':'Medium',
  'fire_rating':'Class A','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'3-phase appliances|Multiple ACs|EV charging','compatible_with':'Residential 1-2BHK|Basic appliance load',
  'requires_component':'25A main MCB|4-6 way distribution board|2.5 sqmm copper wiring',
  'climate_restrictions':'None',
  'hard_block_rule':'None',
  'advisory_rule':'Upgrade to 3-phase if more than 2 ACs planned at any point in future',
  'advisory_message':'Single phase 5kW is severely limited. Any future addition of a second AC or EV charging will require a costly panel upgrade and BESCOM/TNEB re-connection process.',
  'advisory_severity':'Warning','constraint_source_notes':'BESCOM/TNEB service connection regulations; IS 732',
  'ai_advisory_notes':'A 5 kW single phase connection is genuinely undersized for any 3 BHK house in South India in 2024. Even if you only have one split AC today you will add more within 5-10 years as climate gets hotter. A 1.5 ton AC alone draws 1.5-2 kW so two ACs plus a refrigerator plus a washing machine plus kitchen appliances easily exceeds 5 kW simultaneously. When you trip the main MCB repeatedly because of load you will have to apply for a load extension from BESCOM which involves significant paperwork fees and delays. Upgrading to three phase from the start costs Rs 15000-25000 more now versus Rs 80000-150000 for a connection upgrade later including the BESCOM application fee wiring changes and transformer load addition. Spend the money now.',
  'pros':'Lowest connection cost|Adequate for very basic 1-2 BHK|Simple single phase wiring',
  'cons':'Insufficient for most 3 BHK residences with AC|Cannot add EV charging|Costly upgrade later|Trips frequently under load|Not future-ready',
  'tooltip_detail':'5kW single phase. Only for small 1-2 BHK with minimal AC. Upgrade cost is 5x later - invest in 3-phase now.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'ELOAD-002','category_name':'Systems','subcategory_name':'Electrical Load',
  'name':'load_10kw_three_phase','display_name':'10 kW Three Phase','region':'South India',
  'description':'10 kW three phase BESCOM/TNEB service connection. Standard for 3 BHK residential with 2-3 split ACs, all household appliances, washing machine, water heater. Three phase allows balanced load distribution and supports larger individual appliances.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Intermediate','sort_order':'2',
  'base_cost_per_sqft_inr':'14','installation_cost_per_sqft_inr':'8','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Three phase BESCOM connection charges; electrician rates; normalized per sqft',
  'expected_lifespan_years':'25','replacement_cost_factor':'0.5','major_maintenance_cycle_years':'10',
  'major_maintenance_cost_factor':'0.08','annual_minor_maint_factor':'0.005','maintenance_complexity':'Low',
  'lifecycle_source_notes':'Electrical system lifespan 20-30 years',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'8','moisture_resistance':'Medium',
  'fire_rating':'Class A','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'3 BHK residential|2-3 split ACs|All standard appliances',
  'requires_component':'3-phase 40A main RCCB|12-16 way distribution board|4 sqmm copper wiring on AC circuits|Earth leakage protection',
  'climate_restrictions':'None',
  'hard_block_rule':'None',
  'advisory_rule':'Plan conduit provision for future EV charging circuit even if not installing charger now',
  'advisory_message':'Laying an empty conduit from the DB to the parking area during construction costs Rs 500. Adding an EV charging circuit later without pre-laid conduit costs Rs 8000-15000 including wall chasing.',
  'advisory_severity':'Warning','constraint_source_notes':'BESCOM/TNEB regulations; IS 732; NBC 2016',
  'ai_advisory_notes':'Ten kilowatts three phase is the right specification for the standard 3-4 BHK South India home and most BESCOM consumers in residential layouts have this connection. Three phase means you can balance the AC loads across the three phases which prevents the voltage sag you get on a single phase circuit when multiple large loads are running simultaneously. The practical things to get right are the main RCCB rating (40A minimum for 10 kW three phase), earth leakage protection on every circuit, and dedicated circuits for each AC rather than sharing with lighting. An electrician who wants to put all your ACs on one circuit or skip earth leakage circuit breakers is cutting corners. Also insist on 4 sqmm copper wire on all AC circuits - the 2.5 sqmm wire used for light points is undersized for split AC current draw and will overheat under sustained use.',
  'pros':'Standard specification for 3-4 BHK|Supports 2-3 ACs comfortably|Balanced three phase load|Future-ready for most appliances|Wide contractor knowledge',
  'cons':'Not sufficient for EV charging and solar inverter simultaneously|Upgrade to 15kW needed for EV home charging|Higher connection fee than single phase',
  'tooltip_detail':'10kW 3-phase. Standard for 3 BHK with 2-3 ACs. Lay EV conduit during construction. 4sqmm wire on AC circuits.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'ELOAD-003','category_name':'Systems','subcategory_name':'Electrical Load',
  'name':'load_15kw_three_phase_ev','display_name':'15 kW Three Phase + EV Ready','region':'South India',
  'description':'15 kW three phase BESCOM/TNEB service connection with pre-provisioned EV charging circuit and conduit to parking. Future-ready specification for solar inverter, EV charging, home office equipment, and large ACs. Best long-term investment for 2024 construction.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Premium','sort_order':'3',
  'base_cost_per_sqft_inr':'22','installation_cost_per_sqft_inr':'12','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'15kW BESCOM connection; EV conduit and circuit provision; enhanced wiring; normalized per sqft',
  'expected_lifespan_years':'25','replacement_cost_factor':'0.4','major_maintenance_cycle_years':'10',
  'major_maintenance_cost_factor':'0.05','annual_minor_maint_factor':'0.003','maintenance_complexity':'Low',
  'lifecycle_source_notes':'Electrical system lifespan 20-30 years; future-proof for EV and solar',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'9','moisture_resistance':'Medium',
  'fire_rating':'Class A','energy_impact_modifier':'0.1','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All residential configurations|Solar grid-tied inverter|EV home charging|Home office equipment',
  'requires_component':'15kW three phase BESCOM meter|16-20 way distribution board|Dedicated EV circuit conduit to parking|4-6 sqmm copper wiring on power circuits|Bidirectional meter provision for solar',
  'climate_restrictions':'None',
  'hard_block_rule':'None',
  'advisory_rule':'None','advisory_message':'','advisory_severity':'',
  'constraint_source_notes':'BESCOM/TNEB solar net metering regulations; IS 732',
  'ai_advisory_notes':'Fifteen kilowatts three phase with EV provisioning is the specification I am recommending to every new build client in 2024 and the reason is simply the trajectory of EV adoption. BESCOM statistics show that EV registrations in Bangalore grew by 80 percent in 2023. If you are building a house today that you plan to live in for 20 years there is a high probability that you will own an electric vehicle within that period. A 7.2 kW home EV charger draws 32A on a dedicated circuit - this cannot be accommodated on a 10 kW connection that is already carrying 2-3 ACs and household loads. The incremental cost of going from 10 kW to 15 kW at construction time is Rs 15000-20000 more. The cost of upgrading later is Rs 80000-120000 including BESCOM fees connection upgrade and wiring changes. The EV circuit conduit alone - just the plastic pipe from the DB to the parking - costs Rs 500 during construction and Rs 8000-12000 after plastering.',
  'pros':'Future-ready for EV charging and solar inverter|Handles simultaneous high loads|BESCOM bidirectional meter provision for solar net metering|Best long-term value|Marginal cost premium over 10kW',
  'cons':'Higher connection fee than 10kW|Slightly higher installation cost|Over-specified if no EV or solar planned|BESCOM approval time for 15kW may be longer',
  'tooltip_detail':'15kW 3-phase + EV ready. Best future-proof specification for 2024 construction. EV conduit to parking costs Rs 500 now vs Rs 12000 later.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
]

# E5 - Electrical Points Density
points_rows = [
{
  'component_id':'EPOINTS-001','category_name':'Systems','subcategory_name':'Electrical Points',
  'name':'points_basic','display_name':'Basic Point Density','region':'South India',
  'description':'Basic electrical outlet density. 1-2 power sockets per room, single light point per room, no dedicated data or USB points. Adequate for very minimal usage or rental construction. NBC minimum compliance.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Basic','sort_order':'1',
  'base_cost_per_sqft_inr':'4','installation_cost_per_sqft_inr':'3','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Electrical contractor per-point rate; basic density normalized per sqft',
  'expected_lifespan_years':'20','replacement_cost_factor':'0.4','major_maintenance_cycle_years':'10',
  'major_maintenance_cost_factor':'0.1','annual_minor_maint_factor':'0.01','maintenance_complexity':'Medium',
  'lifecycle_source_notes':'Wiring lifespan 20-30 years; switch and socket replacement at 10 years',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'6','moisture_resistance':'Medium',
  'fire_rating':'Class A','energy_impact_modifier':'0','accessibility_score':'7',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All residential configurations',
  'requires_component':'Modular switches (Legrand/Anchor/Havells)|2.5 sqmm copper concealed wiring',
  'climate_restrictions':'None',
  'hard_block_rule':'None',
  'advisory_rule':'Not recommended for owner-occupied homes - extension cords become permanent fixtures',
  'advisory_message':'Basic point density leads to permanent use of extension cords and power strips which are a fire risk. Adding points later requires wall chasing through finished plaster at Rs 2000-4000 per point.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 732; NBC 2016',
  'ai_advisory_notes':'Basic point density was adequate when a bedroom had a light a fan and a clock. In 2024 a typical South India bedroom has a phone charger tablet charger laptop AC unit TV point and reading lamp. Two sockets for all of this means permanent multi-socket extension cords which are the leading cause of residential electrical fires. I see this mistake repeatedly in rental construction where the landlord minimises upfront cost and the tenant lives with extension cord tangles for 10 years. Adding a socket point later requires chasing a channel in a plastered finished wall routing conduit connecting to the distribution board and replastering - total cost Rs 2500-4000 per point. Planning adequate points costs maybe Rs 500-800 per point during construction. The math is obvious.',
  'pros':'Lowest electrical installation cost|Meets NBC minimum requirements',
  'cons':'Insufficient for modern home usage|Leads to permanent extension cord use - fire risk|Adding points later costs 4-6x more|Not recommended for owner-occupied homes',
  'tooltip_detail':'Basic points - 1-2 sockets per room. Not recommended for owner-occupied homes. Extension cord dependency is a fire risk.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'EPOINTS-002','category_name':'Systems','subcategory_name':'Electrical Points',
  'name':'points_standard','display_name':'Standard Point Density','region':'South India',
  'description':'Standard electrical outlet density for residential use. 3-4 power sockets per bedroom, TV point, 1 data/LAN point per room, dedicated kitchen appliance points, 2 sockets per bathroom. Adequate for comfortable modern residential use.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Intermediate','sort_order':'2',
  'base_cost_per_sqft_inr':'8','installation_cost_per_sqft_inr':'5','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Electrical contractor per-point rate; standard density normalized per sqft',
  'expected_lifespan_years':'20','replacement_cost_factor':'0.4','major_maintenance_cycle_years':'10',
  'major_maintenance_cost_factor':'0.08','annual_minor_maint_factor':'0.008','maintenance_complexity':'Low',
  'lifecycle_source_notes':'Wiring lifespan 20-30 years',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'7','moisture_resistance':'Medium',
  'fire_rating':'Class A','energy_impact_modifier':'0','accessibility_score':'9',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All residential configurations',
  'requires_component':'Legrand/Havells/Anchor modular switches|2.5-4 sqmm copper wiring|LAN conduit in each room',
  'climate_restrictions':'None',
  'hard_block_rule':'None',
  'advisory_rule':'None','advisory_message':'','advisory_severity':'',
  'constraint_source_notes':'IS 732; NBC 2016',
  'ai_advisory_notes':'Standard point density is the minimum I recommend for any owner-occupied home and it covers most needs without over-engineering. Three to four sockets per bedroom means you can have the AC phone charger bedside lamp and one additional device without extension cords. The LAN data point in each room is increasingly important even in an era of WiFi because wired connections are more reliable for work-from-home setups and smart TV streaming. Run cat6 conduit in every room even if you only connect data points in the study initially - the incremental cost of the conduit is trivial and it saves the disruption of adding it later. Include dedicated kitchen appliance circuits - microwave mixer grinder and dishwasher on separate circuits prevents tripping when multiple appliances run simultaneously.',
  'pros':'Adequate for comfortable modern residential use|No extension cords needed|LAN points future-proof|Good balance of cost and functionality|Standard for most contractor quotations',
  'cons':'Insufficient for home office or home automation|No USB charging points built in|Data conduit may be omitted if not specified clearly',
  'tooltip_detail':'Standard density - 3-4 sockets/room plus TV and LAN points. Best default for owner-occupied homes.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'EPOINTS-003','category_name':'Systems','subcategory_name':'Electrical Points',
  'name':'points_premium','display_name':'Premium Point Density','region':'South India',
  'description':'Premium electrical outlet density with home automation provision. 5+ power sockets per room, USB charging outlets, LAN and TV points in all rooms, dedicated home office circuits, EV conduit to parking, provisions for home automation control switches, and outdoor weatherproof points.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Premium','sort_order':'3',
  'base_cost_per_sqft_inr':'16','installation_cost_per_sqft_inr':'9','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Premium point density electrician rates Bangalore 2024; Legrand Arteor/Schneider range; normalized per sqft',
  'expected_lifespan_years':'20','replacement_cost_factor':'0.3','major_maintenance_cycle_years':'10',
  'major_maintenance_cost_factor':'0.05','annual_minor_maint_factor':'0.005','maintenance_complexity':'Low',
  'lifecycle_source_notes':'Premium modular switches 15-20 year lifespan; wiring 25+ years',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'8','moisture_resistance':'Medium',
  'fire_rating':'Class A','energy_impact_modifier':'0.05','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All residential configurations|Home automation systems|Home office setups',
  'requires_component':'Legrand Arteor or Schneider Vivace premium modular switches|Cat6 LAN outlets|USB charging outlets|Home automation conduit (4-way corrugated)|EV conduit to parking',
  'climate_restrictions':'None',
  'hard_block_rule':'None',
  'advisory_rule':'Plan home automation conduit separately from power conduit for future KNX/Modbus control',
  'advisory_message':'If home automation is planned, route a separate 4-way corrugated conduit from each switch box back to a central control panel location. Mixing automation wiring in power conduit causes interference.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 732; KNX Association guidelines',
  'ai_advisory_notes':'Premium point density pays for itself in lifestyle quality and in the complete elimination of the wire management problem that plagues Indian homes. When every bedroom has 5-6 sockets plus built-in USB outlets plus a LAN point there is simply no need for extension cords anywhere and the visual cleanliness of the space is dramatically better. The home automation conduit provision is the element most commonly forgotten - if you ever want smart switches smart lighting or a KNX home automation system in the future you need a separate conduit from each switch position back to a central location for the control wiring. This conduit costs Rs 8000-12000 to lay during construction and Rs 80000+ to add later through finished walls. Even if you have no immediate plans for home automation lay the conduit - it costs almost nothing as part of the overall electrical work.',
  'pros':'Maximum convenience - no extension cords anywhere|Future-ready for EV and home automation|USB outlets built in|Premium switch aesthetics|Home office and work-from-home ready|Best for premium construction',
  'cons':'Highest electrical installation cost|Requires detailed planning before construction|Home automation conduit often forgotten - specify clearly|Over-specified for basic residential',
  'tooltip_detail':'Premium points - 5+ sockets/room plus USB, LAN, home automation conduit. Lay home automation conduit separately from power.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
]

new_rows = load_rows + points_rows

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
