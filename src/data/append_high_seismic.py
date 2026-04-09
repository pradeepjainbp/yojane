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

# ── HIGH-SEISMIC DESIGN (Special) ─────────────────────────────────────────────
# Seismic zone design compliance level
# South India: most of KA, TN, KL = Zone II (low); AP coast, Andaman = Zone III; some areas Zone IV/V
# Cost: premium over standard construction per sqft
# 4 options: Zone II baseline → Zone III → Zone IV → Zone V (high seismic)
new_rows = [
{
  'component_id':'SZ-001','category_name':'Special','subcategory_name':'High-Seismic',
  'name':'seismic_zone_ii','display_name':'Seismic Zone II (Standard South India)','region':'South India',
  'description':'Standard IS 1893 Seismic Zone II design. Applicable to most of Karnataka (except Bidar), Tamil Nadu, Kerala and interior Andhra Pradesh. Minimum ductile detailing as per IS 13920. Standard structural design for low seismic risk.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Standard','sort_order':'1',
  'base_cost_per_sqft_inr':'0','installation_cost_per_sqft_inr':'0','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'No premium - baseline seismic design included in standard structural cost.',
  'expected_lifespan_years':'75','replacement_cost_factor':'1.2','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'IS 1893 Part 1; IS 13920; NBC 2016 seismic provisions',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'8','moisture_resistance':'High',
  'fire_rating':'Class A','energy_impact_modifier':'1.0','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'IS 1893 Zone II structural design|IS 13920 ductile detailing at beam-column joints|Structural engineer certification',
  'climate_restrictions':'None',
  'hard_block_rule':'None',
  'advisory_rule':'Confirm your district seismic zone from IS 1893 Part 1 Annexure before finalising structural design',
  'advisory_message':'Seismic zone boundaries in South India are not always intuitive. Verify your specific district zone from IS 1893 Part 1 Annexure B before confirming Zone II design. Some coastal AP districts are Zone III.',
  'advisory_severity':'Info','constraint_source_notes':'IS 1893 Part 1 2016; IS 13920 2016; NBC 2016',
  'ai_advisory_notes':'Zone II seismic design is what the vast majority of South India residential construction follows and it is adequate for the geological risk in most of Karnataka, Tamil Nadu and Kerala. The key requirement that most small residential contractors neglect is IS 13920 ductile detailing at beam-column joints - the special closed stirrups with 135-degree hooks that prevent the joint from failing during an earthquake. This is routinely skipped on residential sites to save time and steel. It is not optional - it is the difference between a building that survives a moderate earthquake and one that collapses.',
  'pros':'Baseline seismic design - no cost premium|Appropriate for most South India locations|Well understood by structural engineers',
  'cons':'IS 13920 ductile detailing routinely skipped by contractors - must be enforced|Not adequate for coastal AP or Andaman districts which are Zone III/IV',
  'tooltip_detail':'Standard Zone II seismic design for most South India. IS 13920 ductile joint detailing mandatory - routinely skipped by contractors, must be enforced.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'SZ-002','category_name':'Special','subcategory_name':'High-Seismic',
  'name':'seismic_zone_iii','display_name':'Seismic Zone III (Coastal AP / North Karnataka)','region':'South India',
  'description':'Enhanced IS 1893 Seismic Zone III design. Applicable to coastal Andhra Pradesh, Vizag region, North Karnataka (Bidar, Gulbarga) and parts of Telangana. Requires enhanced ductile detailing, shear walls for buildings above G+3, and higher steel ratios.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Performance','sort_order':'2',
  'base_cost_per_sqft_inr':'15','installation_cost_per_sqft_inr':'8','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Structural engineer estimate Zone III premium; additional steel and shear wall cost; normalised per sqft',
  'expected_lifespan_years':'75','replacement_cost_factor':'1.2','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'IS 1893 Part 1 2016; IS 13920 2016; NBC 2016',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'9','moisture_resistance':'High',
  'fire_rating':'Class A','energy_impact_modifier':'1.0','accessibility_score':'9',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'15','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'IS 1893 Zone III structural design|Enhanced IS 13920 ductile detailing|Shear walls for G+3 and above|Higher minimum steel ratios|Structural engineer IS 1893 certified',
  'climate_restrictions':'None','hard_block_rule':'None',
  'advisory_rule':'Shear walls mandatory for buildings above G+3 in Zone III',
  'advisory_message':'Zone III buildings above G+3 floors require RCC shear walls in both principal directions as per IS 1893. Frame-only design without shear walls is inadequate for Zone III multi-storey.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 1893 Part 1 2016; IS 13920 2016',
  'ai_advisory_notes':'Zone III seismic design is required in coastal Andhra Pradesh around Vizag and Nellore, North Karnataka around Bidar and Gulbarga, and parts of Telangana. The structural cost premium is real but modest - approximately 8-12% higher steel consumption and the requirement for shear walls in taller buildings. The most important practical change from Zone II is that beam-column joint detailing becomes even more critical and must be inspected by a structural engineer during construction, not just checked on paper.',
  'pros':'Appropriate structural safety for Zone III locations|Shear walls provide excellent lateral rigidity|Enhanced detailing also improves building quality generally',
  'cons':'10-15% structural cost premium over Zone II|Shear wall locations restrict plan flexibility|Requires Zone III certified structural engineer',
  'tooltip_detail':'Zone III for coastal AP, North Karnataka, Telangana. 10-15% structural premium. Shear walls mandatory above G+3. Verify your district zone from IS 1893.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'SZ-003','category_name':'Special','subcategory_name':'High-Seismic',
  'name':'seismic_zone_iv','display_name':'Seismic Zone IV (High Seismic Risk)','region':'South India',
  'description':'High seismic risk design per IS 1893 Zone IV. Applies to Andaman and Nicobar Islands and some border areas. Requires moment-resisting frames, shear walls, base isolation consideration for critical structures, and higher response spectrum design forces.',
  'climate_zone':'Warm-Humid|Temperate','spectrum_position':'High-Performance','sort_order':'3',
  'base_cost_per_sqft_inr':'30','installation_cost_per_sqft_inr':'15','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Structural engineer estimate Zone IV; SMRF design premium; normalised per sqft',
  'expected_lifespan_years':'75','replacement_cost_factor':'1.2','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'IS 1893 Part 1 2016; IS 13920 2016; IS 13935 seismic strengthening',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'9','moisture_resistance':'High',
  'fire_rating':'Class A','energy_impact_modifier':'1.0','accessibility_score':'8',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'12','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'IS 1893 Zone IV dynamic analysis|Special Moment Resisting Frame (SMRF)|Shear walls both directions|Response spectrum analysis by structural engineer|Quality control concrete testing mandatory',
  'climate_restrictions':'None','hard_block_rule':'REQUIRES_SPECIALIST_STRUCTURAL_ENGINEER',
  'advisory_rule':'Response spectrum dynamic analysis mandatory - equivalent static method insufficient for Zone IV above G+2',
  'advisory_message':'Zone IV design above G+2 floors requires dynamic response spectrum analysis. The simpler equivalent static method used for Zone II is not adequate for Zone IV multi-storey buildings.',
  'advisory_severity':'Critical','constraint_source_notes':'IS 1893 Part 1 2016; IS 13920',
  'ai_advisory_notes':'Zone IV seismic design applies primarily to the Andaman and Nicobar Islands and very limited mainland areas. At this zone level the structural design is genuinely specialist engineering - dynamic response spectrum analysis, special moment-resisting frames with very precise reinforcement detailing, and mandatory concrete cube testing to verify material quality. The design fees for Zone IV are significantly higher than standard because the structural analysis complexity is much greater. This is not a design that can be done by a general residential structural engineer.',
  'pros':'Provides genuine earthquake survival safety in high-risk zones|SMRF design also improves robustness against all lateral loads including wind',
  'cons':'20-25% structural cost premium|Dynamic analysis mandatory for multi-storey|Specialist structural engineer required|Concrete quality control must be formally documented',
  'tooltip_detail':'Zone IV for Andaman and Nicobar. Dynamic response spectrum analysis mandatory. SMRF design. Specialist structural engineer - general engineers cannot do this.',
  'status':'Active','verify_flags':'base_cost_per_sqft_inr','data_filled_by':'AI'
},
{
  'component_id':'SZ-004','category_name':'Special','subcategory_name':'High-Seismic',
  'name':'seismic_retrofitting','display_name':'Seismic Retrofitting (Existing Structure)','region':'South India',
  'description':'Structural retrofitting of existing buildings to improve seismic resistance. Methods include jacketing of columns, addition of shear walls, base isolation insertion, and FRP wrapping of critical joints. Applicable to pre-1984 structures designed without seismic provisions.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Premium','sort_order':'4',
  'base_cost_per_sqft_inr':'45','installation_cost_per_sqft_inr':'35','cost_confidence':'Low',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market estimate; varies enormously by existing structure condition and method; [VERIFY]',
  'expected_lifespan_years':'30','replacement_cost_factor':'0.8','major_maintenance_cycle_years':'15',
  'major_maintenance_cost_factor':'0.10','annual_minor_maint_factor':'0.005','maintenance_complexity':'High',
  'lifecycle_source_notes':'IS 13935 seismic repair; CPWD retrofitting guidelines; NDMA guidelines',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'8','moisture_resistance':'High',
  'fire_rating':'Class A','energy_impact_modifier':'1.0','accessibility_score':'5',
  'thermal_source_notes':'No thermal contribution. Column jacketing adds to wall thickness reducing carpet area.',
  'max_floors_supported':'10','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'Severely damaged structures|Structures with foundation failure|Unreinforced masonry beyond repair',
  'compatible_with':'RCC frame structures|Reinforced masonry',
  'requires_component':'Structural assessment and vulnerability analysis first|IS 13935 specialist engineer|Non-destructive testing (rebound hammer, UPV) of existing concrete|Jacketing formwork|High-strength micro-concrete for jacketing',
  'climate_restrictions':'None','hard_block_rule':'REQUIRES_STRUCTURAL_ASSESSMENT_FIRST',
  'advisory_rule':'Structural vulnerability assessment mandatory before any retrofitting work begins',
  'advisory_message':'Seismic retrofitting must begin with a formal structural vulnerability assessment by a qualified engineer. Retrofitting based on visual inspection alone is inadequate and can miss critical weaknesses.',
  'advisory_severity':'Critical','constraint_source_notes':'IS 13935 2009; NDMA seismic vulnerability guidelines; CPWD retrofitting manual',
  'ai_advisory_notes':'Seismic retrofitting is relevant for the large number of South India buildings constructed before 1984 when IS 1893 seismic provisions became mandatory. Pre-1984 construction in Zone III areas like Vizag and Bidar is particularly vulnerable. The most common and cost-effective retrofit method for residential buildings is column jacketing - adding a reinforced concrete shell around each existing column to increase its strength and ductility. FRP (fibre-reinforced polymer) wrapping of columns is a newer faster method that is excellent for improving ductility without adding much weight. A structural vulnerability assessment is mandatory first because some buildings are too damaged to be economically retrofitted and are better demolished.',
  'pros':'Improves safety of existing structures significantly|Column jacketing is relatively low disruption|FRP wrapping is fast and lightweight|Much cheaper than demolition and rebuild',
  'cons':'Very high cost variability - depends entirely on existing structure|Occupants typically need to vacate during work|Column jacketing reduces room sizes|Structural assessment mandatory before cost can be estimated',
  'tooltip_detail':'Seismic retrofit of existing buildings. Column jacketing or FRP wrapping. Structural vulnerability assessment mandatory first. Pre-1984 buildings in Zone III priority.',
  'status':'Active','verify_flags':'base_cost_per_sqft_inr|installation_cost_per_sqft_inr','data_filled_by':'AI'
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
