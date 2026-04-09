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

# ── GREEN RATING TARGET (Sustainability) ───────────────────────────────────────
# Target green building certification level
# Cost: premium over baseline construction per sqft (certification + compliance cost)
# 4 options: No rating → IGBC Green Homes → GRIHA 3-star → GRIHA 5-star/Platinum
new_rows = [
{
  'component_id':'GR-001','category_name':'Sustainability','subcategory_name':'Green Rating Target',
  'name':'no_rating','display_name':'No Green Certification','region':'South India',
  'description':'Standard construction with no formal green certification target. No third-party audit. Building may incorporate sustainable features individually but without systematic compliance or rating documentation.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Baseline','sort_order':'1',
  'base_cost_per_sqft_inr':'0','installation_cost_per_sqft_inr':'0','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'No certification cost.',
  'expected_lifespan_years':'0','replacement_cost_factor':'0','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'N/A',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'5','moisture_resistance':'Medium',
  'fire_rating':'Non-Rated','energy_impact_modifier':'1.0','accessibility_score':'10',
  'thermal_source_notes':'No systematic energy performance requirement. ECBC 2017 baseline only.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'None beyond standard construction',
  'climate_restrictions':'None','hard_block_rule':'None',
  'advisory_rule':'ECBC 2017 compliance is mandatory for all new construction above 500sqm in South India regardless of green rating',
  'advisory_message':'Energy Conservation Building Code (ECBC) 2017 compliance is legally mandatory for commercial and residential buildings above 500sqm conditioned area in Karnataka, Tamil Nadu and Telangana. This is separate from voluntary green certification.',
  'advisory_severity':'Info','constraint_source_notes':'ECBC 2017; State BEE notifications; NBC 2016',
  'ai_advisory_notes':'Most South India residential construction operates without a formal green certification and that is perfectly reasonable for standard housing. The important distinction is that ECBC 2017 energy code compliance is now mandatory (not optional) for larger buildings in most South India states - this is a legal requirement, not a voluntary certification. Even without targeting a formal IGBC or GRIHA rating you should be making basic sustainability decisions - insulation, ECBC-compliant windows, efficient lighting and solar water heating. These pay back in reduced operating costs and do not require any certification fees.',
  'pros':'No certification cost or process overhead|No documentation requirements|Flexible construction choices',
  'cons':'No third-party verification of energy performance|Lower property premium vs certified buildings|ECBC compliance still legally required above 500sqm|No systematic sustainability tracking',
  'tooltip_detail':'No green certification. Standard construction. ECBC 2017 energy code still legally mandatory above 500sqm. Sustainable features can still be adopted individually.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'GR-002','category_name':'Sustainability','subcategory_name':'Green Rating Target',
  'name':'igbc_green_homes','display_name':'IGBC Green Homes Certified','region':'South India',
  'description':'Indian Green Building Council (IGBC) Green Homes certification for residential buildings. Points-based system covering site sustainability, water efficiency, energy, materials and indoor environment. Widely adopted in South India. 3-5% construction premium.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Standard','sort_order':'2',
  'base_cost_per_sqft_inr':'18','installation_cost_per_sqft_inr':'5','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'IGBC registration and certification fees + 3-5% construction premium for compliance; normalised per sqft 1500sqft house',
  'expected_lifespan_years':'5','replacement_cost_factor':'0.8','major_maintenance_cycle_years':'5',
  'major_maintenance_cost_factor':'0.10','annual_minor_maint_factor':'0.01','maintenance_complexity':'Medium',
  'lifecycle_source_notes':'IGBC Green Homes v2.0; certification valid 5 years then recertification',
  'thermal_resistance_score':'6','acoustic_score':'5','durability_score':'7','moisture_resistance':'High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0.7','accessibility_score':'8',
  'thermal_source_notes':'IGBC requires ECBC compliance and minimum energy performance standards. 20-30% energy saving over baseline. ECBC 2017.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'IGBC accredited professional (IGBC AP)|Energy simulation report|Water balance calculation|Material regional sourcing documentation|Commissioning report',
  'climate_restrictions':'None','hard_block_rule':'None',
  'advisory_rule':'Engage IGBC Accredited Professional from design stage - not at construction completion',
  'advisory_message':'IGBC Green Homes certification requires design-stage compliance planning. Attempting to certify a completed building that was not designed for IGBC is very difficult and expensive. Engage the AP at schematic design stage.',
  'advisory_severity':'Warning','constraint_source_notes':'IGBC Green Homes v2.0 rating system; IGBC guidelines',
  'ai_advisory_notes':'IGBC Green Homes is the most accessible green certification for South India residential construction and is worth pursuing if you are building a permanent home you plan to live in for 10+ years. The 3-5% construction cost premium is recovered through 20-30% lower electricity and water bills over the building lifetime. In Bangalore and Chennai IGBC certification also provides a meaningful property value premium of 5-8% at resale. The process requires an IGBC Accredited Professional who should be engaged at design stage not after construction is complete. The documentation requirements are significant but the AP guides you through them.',
  'pros':'20-30% lower electricity and water bills|5-8% property value premium at resale|Third-party verified quality|Systematic approach to sustainability',
  'cons':'3-5% construction cost premium|Documentation overhead|AP fees|Recertification every 5 years',
  'tooltip_detail':'IGBC Green Homes certification. 20-30% energy saving. 5-8% property value premium. Engage accredited professional at design stage not after completion.',
  'status':'Active','verify_flags':'base_cost_per_sqft_inr','data_filled_by':'AI'
},
{
  'component_id':'GR-003','category_name':'Sustainability','subcategory_name':'Green Rating Target',
  'name':'griha_3star','display_name':'GRIHA 3-4 Star Rating','region':'South India',
  'description':'Green Rating for Integrated Habitat Assessment (GRIHA) 3 or 4 star rating. Government of India endorsed system developed by TERI and ADaRSH. Stronger focus on passive design, climate responsiveness and embodied energy than IGBC. Mandatory for government buildings.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Performance','sort_order':'3',
  'base_cost_per_sqft_inr':'28','installation_cost_per_sqft_inr':'8','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'GRIHA registration fees + 5-8% construction premium for 3-4 star compliance; normalised per sqft',
  'expected_lifespan_years':'5','replacement_cost_factor':'0.75','major_maintenance_cycle_years':'5',
  'major_maintenance_cost_factor':'0.08','annual_minor_maint_factor':'0.01','maintenance_complexity':'High',
  'lifecycle_source_notes':'GRIHA v2019; ADaRSH certification guidelines',
  'thermal_resistance_score':'8','acoustic_score':'6','durability_score':'8','moisture_resistance':'High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0.55','accessibility_score':'7',
  'thermal_source_notes':'GRIHA requires passive design compliance, U-value performance, LPD compliance, solar water heating. 35-45% energy saving over baseline. ECBC 2017 exceeded.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'GRIHA Evaluator|Energy simulation software (eQUEST/EnergyPlus)|Daylight simulation|Material LCA data|Post-occupancy evaluation',
  'climate_restrictions':'None','hard_block_rule':'None',
  'advisory_rule':'GRIHA requires post-occupancy evaluation 1 year after occupation - plan for this in advance',
  'advisory_message':'GRIHA certification includes a mandatory post-occupancy evaluation approximately 1 year after first occupation to verify actual energy and water performance against design projections. This must be factored into the building management plan.',
  'advisory_severity':'Info','constraint_source_notes':'GRIHA v2019 rating system; ADaRSH guidelines',
  'ai_advisory_notes':'GRIHA is the more rigorous of the two major Indian green rating systems because it requires genuine passive design compliance and energy simulation - not just a checklist of features. For a committed sustainable home GRIHA 3-4 star forces the design team to make correct decisions on orientation, shading, window-to-wall ratio and insulation from the very beginning. The post-occupancy evaluation requirement is actually a strength - it verifies the building actually performs as designed. GRIHA is mandatory for all central government buildings which means GRIHA-rated private buildings are viewed as genuinely rigorous by discerning buyers.',
  'pros':'35-45% energy saving over baseline|Government endorsed - high credibility|Stronger passive design requirement than IGBC|Post-occupancy verification ensures real performance',
  'cons':'5-8% construction premium|More rigorous documentation than IGBC|Post-occupancy evaluation obligation|Fewer accredited evaluators available in South India vs IGBC',
  'tooltip_detail':'GRIHA 3-4 star. Government endorsed, more rigorous than IGBC. 35-45% energy saving. Post-occupancy evaluation required after 1 year of occupation.',
  'status':'Active','verify_flags':'base_cost_per_sqft_inr','data_filled_by':'AI'
},
{
  'component_id':'GR-004','category_name':'Sustainability','subcategory_name':'Green Rating Target',
  'name':'griha_5star_platinum','display_name':'GRIHA 5-Star / Net Zero Building','region':'South India',
  'description':'Highest green certification level targeting GRIHA 5-star or net-zero energy performance. Requires onsite renewable generation equal to or exceeding annual energy consumption. Exceptional passive design, advanced materials and comprehensive monitoring. Aspirational for residential.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Premium','sort_order':'4',
  'base_cost_per_sqft_inr':'55','installation_cost_per_sqft_inr':'15','cost_confidence':'Low',
  'cost_last_updated':'2024-Q1','cost_source_notes':'GRIHA 5-star premium estimated 10-15% over standard construction + solar system + monitoring; normalised per sqft [VERIFY]',
  'expected_lifespan_years':'5','replacement_cost_factor':'0.7','major_maintenance_cycle_years':'3',
  'major_maintenance_cost_factor':'0.10','annual_minor_maint_factor':'0.02','maintenance_complexity':'High',
  'lifecycle_source_notes':'GRIHA v2019; ADaRSH Net Zero guidelines; IEA Net Zero Buildings',
  'thermal_resistance_score':'10','acoustic_score':'7','durability_score':'8','moisture_resistance':'High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0.1','accessibility_score':'6',
  'thermal_source_notes':'Net zero energy: onsite solar generation = annual consumption. Near-zero grid draw. ECBC 2017 far exceeded.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'Sites with severe shading preventing adequate solar generation',
  'compatible_with':'All structural systems with south-facing roof area',
  'requires_component':'GRIHA Evaluator specialist|Energy simulation and commissioning|Full solar PV system sized to net zero|Energy monitoring system|High-performance envelope|Green housekeeping plan',
  'climate_restrictions':'Net zero requires sufficient solar generation potential. In Kerala coastal high-rainfall zones cloud cover may prevent net zero without larger PV array.',
  'hard_block_rule':'None',
  'advisory_rule':'Net zero target requires integrated design team from concept - not certifiable as an afterthought',
  'advisory_message':'GRIHA 5-star and net-zero buildings require an integrated design team (architect, structural, MEP, sustainability consultant) working together from concept design. Attempting to add sustainability features to a completed design is almost never successful at this level.',
  'advisory_severity':'Strong-Warning','constraint_source_notes':'GRIHA v2019; IEA Net Zero Buildings framework; ADaRSH guidelines',
  'ai_advisory_notes':'GRIHA 5-star or net-zero is an exceptional aspiration and genuinely achievable in South India which has among the best solar resources in the world. In Bangalore or Hyderabad with 5.5 kWh/m2/day solar irradiance a well-designed house can generate more electricity than it consumes annually. The requirements are demanding: super-insulated envelope, very low window-to-wall ratio with high-performance glazing, all-LED lighting, efficient HVAC, and a solar PV system sized to the entire annual load. The building must be designed as an integrated system from day one by a team that includes an energy modeller. The lifestyle payoff is exceptional - zero electricity bill and genuine environmental leadership.',
  'pros':'Near-zero electricity bill - solar generates what you consume|Highest property prestige and value|Net zero carbon lifestyle|Future-proof against any tariff increase',
  'cons':'10-15% construction premium|Requires integrated design team from concept|Strict material and system specifications|Energy monitoring system ongoing requirement',
  'tooltip_detail':'GRIHA 5-star / net-zero. Near-zero electricity bill. Requires integrated design team from day one. Best solar resource in world is in South India.',
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
