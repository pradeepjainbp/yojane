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
  'component_id':'CONC-001','category_name':'Structure','subcategory_name':'Concrete Mix',
  'name':'concrete_m15_pcc','display_name':'M15 — Plain Cement Concrete (PCC)','region':'South India',
  'description':'M15 grade concrete (1:2:4 nominal mix, 15 N/mm² characteristic strength). Used exclusively for PCC applications - levelling courses, walkways, and lean concrete below foundations. NOT suitable for reinforced structural elements.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Basic','sort_order':'1',
  'base_cost_per_sqft_inr':'40','installation_cost_per_sqft_inr':'20','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'CPWD DSR 2023 concrete items; Karnataka PWD SOR 2024-25; normalized per sqft of built-up area',
  'expected_lifespan_years':'50','replacement_cost_factor':'1','major_maintenance_cycle_years':'25',
  'major_maintenance_cost_factor':'0.3','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'IS 456; BIS concrete durability data',
  'thermal_resistance_score':'5','acoustic_score':'8','durability_score':'5','moisture_resistance':'Medium',
  'fire_rating':'Class A','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'High thermal mass - stores and releases heat. Requires insulation for comfort.',
  'max_floors_supported':'1','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'RCC structural elements|Beams|Columns|Slabs with reinforcement',
  'compatible_with':'Lean concrete below foundations|Flooring base course|Walkways|Plinth protection',
  'requires_component':'None',
  'climate_restrictions':'None',
  'hard_block_rule':'NOT for use in reinforced structural elements - beams columns or slabs. PCC use only.',
  'advisory_rule':'None','advisory_message':'','advisory_severity':'',
  'constraint_source_notes':'IS 456:2000; NBC 2016 Part 6',
  'ai_advisory_notes':'M15 is a PCC mix and using it for any reinforced element is a serious structural error that I see happen when clients try to save money on concrete grade. The nominal mix 1:2:4 gives 15 N/mm2 characteristic strength which is simply not enough for the steel to bond to properly and the element will fail under load. M15 has its place - it is the correct choice for the lean concrete layer you pour below your foundations to create a clean working surface and for non-structural walkways and plinth protection aprons. For anything that has steel in it you need M20 minimum. The other common mistake is using tap water mixed with river sand that has too much clay - always use measured water and check your sand quality. In coastal zones even M15 PCC needs proper curing for 14 days minimum or it will be porous and absorb moisture.',
  'pros':'Lowest concrete cost|Adequate for non-structural PCC applications|Wide contractor familiarity',
  'cons':'NOT suitable for RCC elements - structural failure risk|Lower durability than higher grades|Not suitable for exposed or aggressive environments',
  'tooltip_detail':'M15 PCC only. Never use for reinforced beams, columns or slabs. For lean concrete and non-structural uses only.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'CONC-002','category_name':'Structure','subcategory_name':'Concrete Mix',
  'name':'concrete_m20_standard_rcc','display_name':'M20 — Standard RCC','region':'South India',
  'description':'M20 grade concrete (1:1.5:3 nominal mix, 20 N/mm² characteristic strength). Standard grade for all RCC elements in residential construction up to G+2. Most common choice for foundations, slabs, beams and columns in South India.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Intermediate','sort_order':'2',
  'base_cost_per_sqft_inr':'52','installation_cost_per_sqft_inr':'25','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'CPWD DSR 2023; Karnataka PWD SOR 2024-25 RCC items; Bangalore market rate 2024',
  'expected_lifespan_years':'60','replacement_cost_factor':'1','major_maintenance_cycle_years':'30',
  'major_maintenance_cost_factor':'0.2','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'IS 456; BIS concrete durability for moderate exposure',
  'thermal_resistance_score':'5','acoustic_score':'8','durability_score':'7','moisture_resistance':'Medium',
  'fire_rating':'Class A','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'High thermal mass. Roof slab at M20 requires weathering course or insulation.',
  'max_floors_supported':'3','min_floors_required':'1','max_span_supported_m':'4.5',
  'incompatible_with':'G+3 and above without structural engineer approval|Seismic Zone IV-V without upgrade',
  'compatible_with':'Strip foundation|Isolated footing|RCC roof slab|Beams|Columns up to G+2',
  'requires_component':'Fe500 or Fe500D TMT steel|Vibrator for compaction|14-day curing',
  'climate_restrictions':'In coastal zones (Mangalore, Chennai, Kochi) upgrade to M25 for better chloride resistance.',
  'hard_block_rule':'None',
  'advisory_rule':'Use M25 in coastal zones or seismic zones III-IV for better durability',
  'advisory_message':'M20 in coastal areas has reduced durability due to chloride ingress. Consider M25 for any plot within 10km of the sea or in seismic zones III-IV.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 456:2000; ECBC 2017; NBC 2016',
  'ai_advisory_notes':'M20 is the workhorse of South India residential construction and for a G+1 or G+2 house on a normal plot it is the correct and adequate choice. The most important thing about M20 is not the grade itself but how it is made and cured on site. I have seen beautifully designed structures fail because the contractor added extra water to the mix to make it flow easier - every additional litre of water per bag of cement reduces the final strength by about 15 percent. Always insist on a fixed water-cement ratio and use a vibrator for compaction. The second most important thing is curing - M20 needs a minimum of 14 days of continuous wet curing. Covering with jute bags and keeping them wet morning and evening is not optional. A poorly cured M20 slab will have strength closer to M12 and will crack within two monsoons.',
  'pros':'Standard grade for all residential RCC up to G+2|Wide contractor knowledge|Good durability for most South India conditions|Economical',
  'cons':'Insufficient for G+3 and above without engineer review|Reduced chloride resistance in coastal zones|Quality highly dependent on site mixing discipline',
  'tooltip_detail':'M20 standard RCC for G+1-G+2. Most common residential grade. Curing for 14 days mandatory. Consider M25 for coastal plots.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'CONC-003','category_name':'Structure','subcategory_name':'Concrete Mix',
  'name':'concrete_m25_high_strength','display_name':'M25 — High Strength RCC','region':'South India',
  'description':'M25 grade concrete (design mix, 25 N/mm² characteristic strength). Required for G+3 and above residential construction and for all structural elements in seismic zones III and IV. Better durability and chloride resistance than M20.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Performance','sort_order':'3',
  'base_cost_per_sqft_inr':'62','installation_cost_per_sqft_inr':'28','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'CPWD DSR 2023; Karnataka PWD SOR 2024-25; design mix premium over M20',
  'expected_lifespan_years':'70','replacement_cost_factor':'1','major_maintenance_cycle_years':'35',
  'major_maintenance_cost_factor':'0.15','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'IS 456; BIS concrete durability for severe exposure',
  'thermal_resistance_score':'5','acoustic_score':'8','durability_score':'8','moisture_resistance':'High',
  'fire_rating':'Class A','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'Higher density than M20 - slightly better thermal mass performance.',
  'max_floors_supported':'6','min_floors_required':'1','max_span_supported_m':'6',
  'incompatible_with':'None','compatible_with':'All structural systems|Seismic Zone III-IV construction',
  'requires_component':'Design mix from RMC plant or certified batching|Fe500D TMT steel|Vibrator|21-day curing',
  'climate_restrictions':'Recommended for all coastal construction within 10km of sea. Mandatory for seismic zones III-IV.',
  'hard_block_rule':'None',
  'advisory_rule':'Design mix from RMC plant strongly recommended over site batching for M25',
  'advisory_message':'M25 should ideally be supplied as Ready Mix Concrete (RMC) with a delivery challan showing the mix design. Site batching of M25 is unreliable without proper equipment and calibrated measures.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 456:2000; IS 10262; NBC 2016',
  'ai_advisory_notes':'M25 is where I draw the line for G+3 construction and coastal plots. The strength increase from M20 to M25 costs roughly 15-20 percent more but gives you significantly better protection against the two biggest concrete problems in South India - carbonation and chloride ingress from sea air and coastal humidity. The important thing about M25 is that it really should come from a Ready Mix Concrete plant because site batching at this grade without calibrated equipment and a proper mix design is unreliable. A poorly batched M25 can actually be weaker than a well-batched M20. Get the RMC delivery challan showing the mix design and slump value and insist on a vibrator for every pour. In seismic zones III and IV M25 with Fe500D steel is the minimum I will put my name on.',
  'pros':'Required grade for G+3 and above|Better durability in coastal and humid conditions|IS recommended for seismic zones III-IV|Higher strength allows smaller member sizes',
  'cons':'Higher cost than M20|Site batching unreliable - RMC plant recommended|Requires design mix not nominal mix',
  'tooltip_detail':'M25 for G+3+, coastal plots, and seismic zones III-IV. Use RMC plant supply for reliable quality.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'CONC-004','category_name':'Structure','subcategory_name':'Concrete Mix',
  'name':'concrete_m30_structural_premium','display_name':'M30 — Structural Premium','region':'South India',
  'description':'M30 grade concrete (design mix, 30 N/mm² characteristic strength). Required for G+4 and above, heavily loaded transfer structures, prestressed elements, and construction in seismic zone V. Exclusively from RMC plant supply.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Premium','sort_order':'4',
  'base_cost_per_sqft_inr':'75','installation_cost_per_sqft_inr':'32','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'RMC plant rates Bangalore/Hyderabad/Chennai 2024; M30 premium over M25; normalized per sqft',
  'expected_lifespan_years':'75','replacement_cost_factor':'1','major_maintenance_cycle_years':'40',
  'major_maintenance_cost_factor':'0.1','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'IS 456; high-strength concrete durability data',
  'thermal_resistance_score':'5','acoustic_score':'8','durability_score':'10','moisture_resistance':'Very High',
  'fire_rating':'Class A','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'Dense concrete - very high thermal mass.',
  'max_floors_supported':'10','min_floors_required':'1','max_span_supported_m':'8',
  'incompatible_with':'None','compatible_with':'All structural systems|Prestressed elements|Heavy commercial construction',
  'requires_component':'Certified RMC plant with IS 4926 compliance|Fe500D or Fe550 TMT steel|Pump delivery for upper floors|28-day curing',
  'climate_restrictions':'None',
  'hard_block_rule':'None',
  'advisory_rule':'RMC plant supply mandatory - site batching not acceptable for M30',
  'advisory_message':'M30 cannot be reliably produced by site batching. A certified RMC plant with a validated mix design is mandatory. Request the mix design report and delivery challan for every truck.',
  'advisory_severity':'Strong-Warning','constraint_source_notes':'IS 456:2000; IS 10262; IS 4926',
  'ai_advisory_notes':'M30 is the grade I specify for G+4 residential buildings heavy transfer slabs over commercial spaces and seismic zone V construction. For most private residential construction on a plot in Bangalore or Chennai G+3 on M25 is sufficient and M30 is overkill that adds unnecessary cost. But if your structural engineer has specified M30 there is a reason - do not ask him to reduce the grade to save money. The absolute rule with M30 is that it must come from an RMC plant. There is no practical way to batch M30 reliably on site without a weigh batcher and calibrated equipment. Always request the mix design report from the RMC plant and check that the delivery challan matches the specified slump and water-cement ratio.',
  'pros':'Maximum strength for tall structures|Seismic zone V compliance|Best durability and longevity|Smallest structural member sizes',
  'cons':'Highest concrete cost|RMC plant supply mandatory|Requires pump placement for upper floors|Not needed for typical residential construction',
  'tooltip_detail':'M30 for G+4+, seismic zone V, heavy loads. RMC plant supply mandatory. Not needed for typical residential construction.',
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
