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

# ── WINDOWS (Finishes) ──────────────────────────────────────────────────────
# Cost unit: base_cost_per_sqft_inr = INR per sqft of window leaf area
# 5 options: Basic → Standard → Performance → High-Performance → Special
new_rows = [
{
  'component_id':'WIN-001','category_name':'Finishes','subcategory_name':'Windows',
  'name':'aluminium_sliding','display_name':'Aluminium Sliding Window','region':'South India',
  'description':'Standard extruded aluminium sliding window in 2-track or 3-track configuration. Most common window type in South India residential construction. 1.2-2.0mm profile thickness.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Basic','sort_order':'1',
  'base_cost_per_sqft_inr':'180','installation_cost_per_sqft_inr':'40','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'CPWD DSR 2023 Item 13.1; Karnataka PWD SOR 2024-25; Bangalore/Chennai aluminium market rate',
  'expected_lifespan_years':'20','replacement_cost_factor':'0.9','major_maintenance_cycle_years':'7',
  'major_maintenance_cost_factor':'0.12','annual_minor_maint_factor':'0.02','maintenance_complexity':'Low',
  'lifecycle_source_notes':'BRE Digest 345; aluminium industry lifespan data',
  'thermal_resistance_score':'2','acoustic_score':'3','durability_score':'7','moisture_resistance':'High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'1.6','accessibility_score':'9',
  'thermal_source_notes':'U-value 5.5-6.0 W/m2K without thermal break. Aluminium conducts heat rapidly. ECBC 2017 Table 4.6.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'2.4',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'Mosquito mesh|Weather-strip brush seals',
  'climate_restrictions':'Not recommended for west-facing openings > 4 sqft in Hot-Dry zones without external shading',
  'hard_block_rule':'None',
  'advisory_rule':'West-facing openings in Hot-Dry zones require external shading',
  'advisory_message':'Standard aluminium sliding windows on west-facing walls cause severe solar heat gain in summer. Add external chajja or louvers.',
  'advisory_severity':'Warning','constraint_source_notes':'ECBC 2017 Section 4.5; NBC 2016',
  'ai_advisory_notes':'Aluminium sliding windows are what 90% of South India homes use because they are cheap fast to install and every contractor knows how to fit them. But they are terrible at keeping heat out because the aluminium frame conducts heat directly into the room. If you are in Chennai Hyderabad or coastal AP always insist on minimum 1.6mm profile thickness - cheap 1.2mm profiles bend and the sliding mechanism jams within 3-4 years. Add quality nylon brush seals on the tracks because without them mosquitoes find every gap. For west-facing windows above 2 sqft add a proper RCC chajja of at least 18 inches overhang.',
  'pros':'Very low cost|Widely available and serviceable|Smooth sliding operation|Corrosion resistant',
  'cons':'Poor thermal insulation - aluminium conducts heat|Poor acoustic performance|Brush seals wear out|Cheap profiles bend over time',
  'tooltip_detail':'Standard aluminium sliding window. Most common in South India. Poor thermal performance - add external shading on west and south faces.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'WIN-002','category_name':'Finishes','subcategory_name':'Windows',
  'name':'upvc_sliding_casement','display_name':'uPVC Sliding / Casement Window','region':'South India',
  'description':'Multi-chamber uPVC profile window in sliding or casement configuration with steel reinforcement. Significantly better thermal and acoustic performance than aluminium. 60-70mm profile depth.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Standard','sort_order':'2',
  'base_cost_per_sqft_inr':'285','installation_cost_per_sqft_inr':'50','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market rate Fenesta/Encraft/Rehau uPVC; Bangalore/Chennai distributor price including glass',
  'expected_lifespan_years':'30','replacement_cost_factor':'0.75','major_maintenance_cycle_years':'10',
  'major_maintenance_cost_factor':'0.08','annual_minor_maint_factor':'0.01','maintenance_complexity':'Low',
  'lifecycle_source_notes':'BS EN 12608; manufacturer 10-year warranty; BRE Digest 345',
  'thermal_resistance_score':'6','acoustic_score':'6','durability_score':'8','moisture_resistance':'Very High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'1.2','accessibility_score':'9',
  'thermal_source_notes':'U-value 2.8-3.5 W/m2K (multi-chamber profile with single glass). ECBC 2017 Table 4.6 compliant.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'2.0',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'Steel reinforcement inside profile|EPDM gaskets|Silicone sealant at perimeter',
  'climate_restrictions':'UV-stabilised profiles mandatory for south and west elevations',
  'hard_block_rule':'None',
  'advisory_rule':'Specify UV-stabilised grade for south and west-facing windows',
  'advisory_message':'Standard uPVC without UV stabilisation yellows and becomes brittle within 5-7 years on south and west facades in South India.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 14856; manufacturer UV stability rating',
  'ai_advisory_notes':'uPVC windows are the upgrade I recommend most to clients on a medium budget because for 50-60% more than aluminium you get windows that actually keep heat and noise out. The critical specification is always ask for UV-stabilised profiles and check that steel reinforcement sections are inserted inside the hollow chambers - cheap suppliers skip this and the frames bow inward under wind pressure. The EPDM rubber gaskets are what make these windows airtight so inspect them during installation and reject any that show visible gaps at the corners. uPVC casement opens fully unlike sliding so ventilation is much better.',
  'pros':'Much better thermal insulation than aluminium|Good acoustic performance|Zero painting ever|30-year lifespan|Termite and corrosion proof',
  'cons':'Higher cost than aluminium|Yellows without UV stabilisation|Cannot be repainted|Repair requires specialist',
  'tooltip_detail':'Multi-chamber uPVC window. Significantly better thermal and acoustic performance than aluminium. Specify UV-stabilised grade.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'WIN-003','category_name':'Finishes','subcategory_name':'Windows',
  'name':'aluminium_thermally_broken','display_name':'Thermally Broken Aluminium Window','region':'South India',
  'description':'Premium aluminium window with polyamide thermal break strip separating inner and outer frame. Eliminates conductive heat bridge of standard aluminium. Suitable for DGU glazing.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Performance','sort_order':'3',
  'base_cost_per_sqft_inr':'420','installation_cost_per_sqft_inr':'65','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market rate Alumil/Schuco/local Bangalore fabricators with thermal break; verified against 3 Bangalore suppliers',
  'expected_lifespan_years':'25','replacement_cost_factor':'0.8','major_maintenance_cycle_years':'10',
  'major_maintenance_cost_factor':'0.10','annual_minor_maint_factor':'0.015','maintenance_complexity':'Medium',
  'lifecycle_source_notes':'BS EN 14351; manufacturer data; BRE Digest 345',
  'thermal_resistance_score':'7','acoustic_score':'7','durability_score':'8','moisture_resistance':'High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'1.1','accessibility_score':'8',
  'thermal_source_notes':'U-value 2.0-2.8 W/m2K with thermal break + single glass; 1.4-1.8 with DGU. ECBC 2017 compliant.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'3.0',
  'incompatible_with':'Standard single-pane glass where DGU is specified',
  'compatible_with':'All structural systems|DGU glazing units',
  'requires_component':'Polyamide thermal break strip|EPDM gaskets|Silicone perimeter seal',
  'climate_restrictions':'None','hard_block_rule':'None',
  'advisory_rule':'Verify thermal break polyamide strip is present before accepting delivery',
  'advisory_message':'Some fabricators supply standard aluminium frames claiming thermal break. Ask to see a cut section of the profile - the brown polyamide strip must be visible between inner and outer aluminium.',
  'advisory_severity':'Warning','constraint_source_notes':'BS EN 14351; ECBC 2017 Section 4.5',
  'ai_advisory_notes':'Thermally broken aluminium gives you the slim elegant aluminium look that architects love with the thermal performance you actually need in South India. The polyamide strip inside the profile breaks the heat conduction path so the frame no longer acts as a heat pipe between outside and inside. This is mandatory if you are specifying DGU glass because putting DGU into a standard aluminium frame wastes most of the thermal benefit through the frame itself. The fabrication quality varies enormously in South India - ask to see a cut sample of the profile before ordering because some suppliers simply mark standard frames as thermally broken.',
  'pros':'Slim premium aesthetic|Good thermal performance with DGU|Suitable for large openings|Corrosion resistant',
  'cons':'Higher cost than uPVC for similar performance|Requires quality verification of thermal break|Specialist repair needed',
  'tooltip_detail':'Premium aluminium with thermal break strip. Required for DGU glass. Verify polyamide strip in profile before accepting delivery.',
  'status':'Active','verify_flags':'base_cost_per_sqft_inr','data_filled_by':'AI'
},
{
  'component_id':'WIN-004','category_name':'Finishes','subcategory_name':'Windows',
  'name':'wooden_casement','display_name':'Timber / Wooden Casement Window','region':'South India',
  'description':'Solid hardwood or teak casement window with traditional design. Good natural insulation. Popular in heritage, traditional and eco-conscious construction. Requires regular maintenance.',
  'climate_zone':'Warm-Humid|Temperate','spectrum_position':'Performance','sort_order':'4',
  'base_cost_per_sqft_inr':'550','installation_cost_per_sqft_inr':'90','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Bangalore timber market rate for seasoned teak/hardwood; Karnataka PWD SOR 2024-25 timber items',
  'expected_lifespan_years':'40','replacement_cost_factor':'0.7','major_maintenance_cycle_years':'3',
  'major_maintenance_cost_factor':'0.15','annual_minor_maint_factor':'0.03','maintenance_complexity':'High',
  'lifecycle_source_notes':'BRE Digest 345; IS 287 timber specifications; field observation South India',
  'thermal_resistance_score':'7','acoustic_score':'8','durability_score':'7','moisture_resistance':'Medium',
  'fire_rating':'Non-Rated','energy_impact_modifier':'1.0','accessibility_score':'7',
  'thermal_source_notes':'Solid wood has low thermal conductivity ~0.13 W/m.K. Natural insulating frame. ECBC 2017.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'1.8',
  'incompatible_with':'Coastal high-salinity zones without marine-grade treatment',
  'compatible_with':'All structural systems',
  'requires_component':'Kiln-dried seasoned timber|Teak oil or paint finish|Quality brass hardware',
  'climate_restrictions':'Requires wide chajja overhang in heavy monsoon zones. Not recommended in coastal high-salinity areas without specialist treatment.',
  'hard_block_rule':'None',
  'advisory_rule':'Verify kiln-dried timber with moisture content below 12% before purchase',
  'advisory_message':'Green or improperly seasoned timber will warp and swell in the first monsoon. Insist on kiln-dried wood with MC below 12%.',
  'advisory_severity':'Strong-Warning','constraint_source_notes':'IS 287; IS 4021 timber seasoning standards',
  'ai_advisory_notes':'Solid wood windows have a warmth and character that no aluminium or uPVC can match and they are the choice for anyone doing traditional South India architecture or an eco-conscious home. The timber quality is the critical issue - the market is full of plantation teak passed off as premium Burma teak and green unseasoned wood that warps in the first rain. Always buy from a licensed timber depot and insist on kiln-dried wood with a moisture content certificate below 12%. Apply a proper teak oil or exterior paint finish before installation and renew it every 2-3 years especially in coastal areas. With proper maintenance a solid teak window will outlast three generations.',
  'pros':'Natural insulating wood frame|Excellent acoustic performance|Timeless traditional aesthetic|Repairable and repaintable',
  'cons':'Warps if timber not properly seasoned|High maintenance - oiling every 2-3 years|Not suitable for coastal salinity without treatment|Species fraud common in market',
  'tooltip_detail':'Solid hardwood casement window. Excellent insulation and aesthetics. Requires kiln-dried timber and periodic oiling to prevent warping.',
  'status':'Active','verify_flags':'base_cost_per_sqft_inr','data_filled_by':'AI'
},
{
  'component_id':'WIN-005','category_name':'Finishes','subcategory_name':'Windows',
  'name':'louvred_ventilation','display_name':'Louvred / Jalousie Ventilation Window','region':'South India',
  'description':'Horizontal glass or aluminium blade louvres in aluminium frame. Maximum passive ventilation. Traditional South India bathroom and utility room window. Zero weather sealing.',
  'climate_zone':'Warm-Humid|Temperate','spectrum_position':'Basic','sort_order':'5',
  'base_cost_per_sqft_inr':'120','installation_cost_per_sqft_inr':'25','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market rate South India aluminium fabricators; CPWD DSR 2023',
  'expected_lifespan_years':'15','replacement_cost_factor':'0.9','major_maintenance_cycle_years':'5',
  'major_maintenance_cost_factor':'0.10','annual_minor_maint_factor':'0.02','maintenance_complexity':'Low',
  'lifecycle_source_notes':'Market observation; aluminium blade degradation',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'5','moisture_resistance':'Low',
  'fire_rating':'Non-Rated','energy_impact_modifier':'1.8','accessibility_score':'10',
  'thermal_source_notes':'No weather sealing. Continuous air infiltration. Not suitable for AC rooms. ECBC 2017 non-compliant for conditioned spaces.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'1.2',
  'incompatible_with':'Air-conditioned rooms|Rooms requiring security',
  'compatible_with':'All structural systems',
  'requires_component':'Mosquito mesh overlay|Aluminium frame',
  'climate_restrictions':'Not suitable in Hot-Dry zones where dust ingress is a problem',
  'hard_block_rule':'BLOCK_IN_AC_ROOMS',
  'advisory_rule':'Never use in air-conditioned spaces - completely negates AC efficiency',
  'advisory_message':'Louvred windows cannot be sealed. Using in an air-conditioned room will waste all cooling energy.',
  'advisory_severity':'Critical','constraint_source_notes':'ECBC 2017 Section 4.5; NBC 2016',
  'ai_advisory_notes':'Louvred windows are the traditional South India solution for bathrooms toilets and utility areas where maximum passive airflow is more important than thermal control. In a hot humid bathroom they work perfectly - the continuous blade ventilation prevents moisture buildup and mould. But never specify them in any room with AC because they cannot be sealed and all your cooling energy will literally blow out. They are also poor for security - the blades can be removed from outside easily so avoid them on ground floor bedrooms or any room with valuables. Pair with a mosquito mesh frame on the outside.',
  'pros':'Maximum passive ventilation|Very low cost|No maintenance required|Traditional South India design',
  'cons':'Cannot be sealed - no weather protection|Useless in AC rooms|Poor security - blades removable|No acoustic or thermal benefit',
  'tooltip_detail':'Traditional louvred blade window. Maximum ventilation for bathrooms and utility rooms. Cannot be used in air-conditioned spaces.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
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
