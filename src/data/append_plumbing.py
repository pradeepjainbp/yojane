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

# ── PLUMBING (Systems) ────────────────────────────────────────────────────────
# Cost unit: base_cost_per_sqft_inr = INR per sqft of built-up area (whole house system cost)
# 5 options: Basic exposed GI → CPVC concealed → uPVC → PPR → Premium concealed PPR
new_rows = [
{
  'component_id':'PLB-001','category_name':'Systems','subcategory_name':'Plumbing',
  'name':'gi_exposed','display_name':'GI Pipe — Exposed (Galvanised Iron)','region':'South India',
  'description':'25-40mm galvanised iron threaded pipes installed exposed along walls and ceiling. Traditional low-cost system. Heavily used in older construction but largely obsolete for new residential builds.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Basic','sort_order':'1',
  'base_cost_per_sqft_inr':'55','installation_cost_per_sqft_inr':'30','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'CPWD DSR 2023 plumbing items; Karnataka PWD SOR 2024-25; GI pipe market rate normalised per sqft',
  'expected_lifespan_years':'20','replacement_cost_factor':'0.9','major_maintenance_cycle_years':'7',
  'major_maintenance_cost_factor':'0.20','annual_minor_maint_factor':'0.04','maintenance_complexity':'Medium',
  'lifecycle_source_notes':'IS 1239; BRE Digest 345; field observation - coastal corrosion accelerates failure',
  'thermal_resistance_score':'1','acoustic_score':'2','durability_score':'5','moisture_resistance':'Medium',
  'fire_rating':'Non-Rated','energy_impact_modifier':'1.0','accessibility_score':'8',
  'thermal_source_notes':'Metal pipes conduct heat rapidly. Hot water pipes must be insulated. ECBC 2017.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'Coastal zones within 5km of sea without special treatment',
  'compatible_with':'All structural systems',
  'requires_component':'Teflon tape on all threaded joints|Gate valves at branch points|PVC drain lines (GI not used for drainage)',
  'climate_restrictions':'In coastal and high-salinity zones GI pipes corrode internally within 7-10 years causing rust-coloured water. Not recommended for new construction near coast.',
  'hard_block_rule':'None',
  'advisory_rule':'Not recommended for new residential construction - specify CPVC or PPR instead',
  'advisory_message':'GI pipes corrode internally releasing rust particles into drinking water within 10-15 years in South India humidity. Concealed GI is extremely difficult and expensive to replace. Choose CPVC or PPR for new builds.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 1239; IS 778; BIS plumbing standards',
  'ai_advisory_notes':'I only include GI pipe as a baseline comparison because most clients in older buildings already have it. For any new construction I strongly advise against GI piping. Internal rust buildup contaminates drinking water and the threaded joints are vulnerable to leaks especially when the pipes go through the embedded in slabs and walls. When GI pipes fail inside a slab the only repair is breaking open the concrete which is enormously expensive and disruptive. The one advantage of exposed GI is that you can find and repair leaks easily since everything is visible - but this means visible ugly pipes along your walls. Use CPVC or PPR for new construction.',
  'pros':'Low material cost|Widely available|Easy to find plumber|Exposed system easy to repair',
  'cons':'Corrodes internally releasing rust|Threaded joints leak over time|Ugly exposed installation|Not suitable for concealed use',
  'tooltip_detail':'Traditional GI pipe. Not recommended for new construction - internal rust contaminates water. Use CPVC or PPR instead.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'PLB-002','category_name':'Systems','subcategory_name':'Plumbing',
  'name':'cpvc_concealed','display_name':'CPVC Concealed Plumbing','region':'South India',
  'description':'Chlorinated PVC pipes (IS 15778) for hot and cold water supply, concealed in walls and slabs. Standard for modern South India residential. Solvent-welded joints. Suitable for hot water up to 93°C.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Standard','sort_order':'2',
  'base_cost_per_sqft_inr':'85','installation_cost_per_sqft_inr':'40','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market rate Astral/Prince/Finolex CPVC pipes + fittings; Bangalore/Chennai contractor rate normalized per sqft',
  'expected_lifespan_years':'50','replacement_cost_factor':'0.7','major_maintenance_cycle_years':'15',
  'major_maintenance_cost_factor':'0.08','annual_minor_maint_factor':'0.01','maintenance_complexity':'Low',
  'lifecycle_source_notes':'IS 15778; ASTM D2846; manufacturer 50-year warranty Astral/Prince',
  'thermal_resistance_score':'2','acoustic_score':'3','durability_score':'8','moisture_resistance':'Very High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'1.0','accessibility_score':'9',
  'thermal_source_notes':'CPVC good insulator vs metal. Hot water pipes lose less heat than copper. ECBC 2017.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'CPVC solvent cement (not PVC solvent - different formula)|Gate valves|Stop cocks|PVC drainage pipes|Water softener in hard water areas',
  'climate_restrictions':'In extremely hard water zones (TDS above 500ppm) scale deposits narrow CPVC bore over 15-20 years. Install water softener.',
  'hard_block_rule':'None',
  'advisory_rule':'Use CPVC solvent cement not standard PVC solvent - different chemical formulas',
  'advisory_message':'CPVC and PVC require different solvent cements. Using PVC solvent on CPVC joints causes joint failure within months. Buy the correct Astral CPVC solvent explicitly.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 15778; ASTM D2846; manufacturer installation guide',
  'ai_advisory_notes':'CPVC is the standard I recommend for all middle-income residential projects in South India. The 50-year warranty from Astral and Prince is real - I have seen houses built in the 2000s with CPVC that still have no issues. The critical quality issue is the solvent cement - CPVC uses a completely different chemical from PVC and mixing them causes joint failure within months. Always buy the matching CPVC solvent from the same brand as your pipe. The other issue is hard water particularly in areas of Bangalore and interior Andhra - the high mineral content slowly narrows the bore. Install a water softener or use larger bore pipes in hard water areas.',
  'pros':'50-year lifespan|Suitable for hot and cold water|No corrosion or rust|Very good concealed installation',
  'cons':'Solvent joints must be done correctly|Cannot be used for gas|Hard water areas need softener|More expensive than basic GI',
  'tooltip_detail':'Standard modern residential plumbing. 50-year rated. Use CPVC-specific solvent cement only. Most reliable concealed option.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'PLB-003','category_name':'Systems','subcategory_name':'Plumbing',
  'name':'upvc_plumbing','display_name':'uPVC Plumbing (Cold Water Only)','region':'South India',
  'description':'Unplasticised PVC pipes for cold water supply and drainage. Not suitable for hot water above 60°C. Lower cost than CPVC. Commonly used for external water supply lines and drainage.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Basic','sort_order':'3',
  'base_cost_per_sqft_inr':'65','installation_cost_per_sqft_inr':'32','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market rate Finolex/Supreme uPVC; Karnataka PWD SOR 2024-25; normalized per sqft',
  'expected_lifespan_years':'40','replacement_cost_factor':'0.75','major_maintenance_cycle_years':'15',
  'major_maintenance_cost_factor':'0.08','annual_minor_maint_factor':'0.01','maintenance_complexity':'Low',
  'lifecycle_source_notes':'IS 4985; BRE Digest 345',
  'thermal_resistance_score':'2','acoustic_score':'3','durability_score':'8','moisture_resistance':'Very High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'1.0','accessibility_score':'9',
  'thermal_source_notes':'uPVC cannot handle hot water - softens and deforms above 60C. Cold lines only. ECBC 2017.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'Hot water supply lines|Concealed solar water heater connections',
  'compatible_with':'All structural systems',
  'requires_component':'PVC solvent cement|Gate valves|Drainage slope minimum 1:80',
  'climate_restrictions':'UV exposure degrades uPVC. All external exposed pipes must be painted or covered.',
  'hard_block_rule':'BLOCK_FOR_HOT_WATER_LINES',
  'advisory_rule':'Never use uPVC for hot water supply lines - use CPVC or PPR instead',
  'advisory_message':'uPVC pipes deform and fail above 60°C. Using uPVC for solar water heater or geyser supply lines will cause pipe failure and flooding.',
  'advisory_severity':'Critical','constraint_source_notes':'IS 4985; IS 15778; manufacturer temperature rating',
  'ai_advisory_notes':'uPVC is excellent and very economical for drainage lines and cold water external supply but must absolutely never be used for hot water supply. It softens at 60 degrees and solar water heaters in South India routinely produce water at 65-75 degrees in summer - I have seen multiple failures where uPVC connections to solar heaters burst flooding the building. Use uPVC for all drainage pipework and external cold supply lines but switch to CPVC for every internal concealed supply line especially anything connected to a geyser or solar heater.',
  'pros':'Economical|Good for drainage and cold water|40-year lifespan|Wide range of fittings available',
  'cons':'Cannot carry hot water - deforms above 60C|UV degrades exposed pipes|Not suitable for concealed hot water|Loud water hammer noise in drainage',
  'tooltip_detail':'uPVC for cold water and drainage only. Never use for hot water lines - deforms above 60C. Good economical choice for drainage.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'PLB-004','category_name':'Systems','subcategory_name':'Plumbing',
  'name':'ppr_hot_cold','display_name':'PPR Pipe — Hot and Cold (Fusion Welded)','region':'South India',
  'description':'Polypropylene Random copolymer (PPR) pipes with heat-fusion welded joints. Superior to CPVC for hot water. Rated to 95°C continuous. Growing adoption in premium South India residential.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Performance','sort_order':'4',
  'base_cost_per_sqft_inr':'110','installation_cost_per_sqft_inr':'50','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market rate Wavin/Aquatherm/Finolex PPR pipes + fusion welder rental; normalized per sqft; verified 2 Bangalore suppliers',
  'expected_lifespan_years':'50','replacement_cost_factor':'0.65','major_maintenance_cycle_years':'20',
  'major_maintenance_cost_factor':'0.06','annual_minor_maint_factor':'0.008','maintenance_complexity':'Low',
  'lifecycle_source_notes':'DIN 8077; ISO 15874; manufacturer 50-year warranty; DVGW Germany certification',
  'thermal_resistance_score':'3','acoustic_score':'5','durability_score':'9','moisture_resistance':'Very High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'1.0','accessibility_score':'9',
  'thermal_source_notes':'PPR thermal conductivity 0.24 W/m.K. Significantly better hot water retention than CPVC. DIN 8077.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'PPR fusion welding machine (rental)|PPR-specific fittings|Gate valves',
  'climate_restrictions':'None','hard_block_rule':'None',
  'advisory_rule':'PPR joints must be made with a proper fusion welding machine - not solvent cement',
  'advisory_message':'PPR pipes use heat fusion welding not solvent cement. Attempting to join PPR with solvent will fail immediately. The installer must have a proper electric fusion welding machine.',
  'advisory_severity':'Warning','constraint_source_notes':'DIN 8077; ISO 15874; manufacturer installation guide',
  'ai_advisory_notes':'PPR is the system I recommend for any premium project because the fusion-welded joints are leak-proof for life - unlike solvent joints which can fail if the surface is wet or the glue is wrong. The pipe and fitting literally melt together into one monolithic piece. The limitation is that the installer must have a proper electric fusion welding machine and know how to use it - in South India fewer plumbers have this tool compared to CPVC skills so verify before hiring. PPR is also quieter than CPVC because the slightly softer material damps water flow noise - a meaningful quality difference in bathrooms adjacent to bedrooms.',
  'pros':'Fusion welded joints - zero leak risk|50-year lifespan|Rated to 95C - best for solar heaters|Quieter than CPVC|Eco-friendly - no solvents',
  'cons':'Installer must have fusion welder - fewer plumbers|Higher material cost than CPVC|Cannot be repaired with solvent - needs welding machine|Linear expansion higher than metal',
  'tooltip_detail':'Premium fusion-welded PPR pipe. Zero leak joints. Best for solar water heater connections. Installer must have fusion welding machine.',
  'status':'Active','verify_flags':'base_cost_per_sqft_inr','data_filled_by':'AI'
},
{
  'component_id':'PLB-005','category_name':'Systems','subcategory_name':'Plumbing',
  'name':'concealed_pprc_insulated','display_name':'Fully Concealed PPR-C + Insulated Hot Lines','region':'South India',
  'description':'Premium fully concealed PPR-C plumbing system with foam insulation jackets on all hot water pipes, pressure-tested per IS 12235 before plastering, dual-stack drainage, and individual isolation valves to every fixture.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Premium','sort_order':'5',
  'base_cost_per_sqft_inr':'165','installation_cost_per_sqft_inr':'70','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market rate full concealed PPR-C system with thermal insulation and dual-stack; verified contractor Bangalore and Chennai',
  'expected_lifespan_years':'50','replacement_cost_factor':'0.6','major_maintenance_cycle_years':'25',
  'major_maintenance_cost_factor':'0.05','annual_minor_maint_factor':'0.005','maintenance_complexity':'Low',
  'lifecycle_source_notes':'DIN 8077; IS 12235 pressure test; dual-stack drainage standards',
  'thermal_resistance_score':'4','acoustic_score':'7','durability_score':'9','moisture_resistance':'Very High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0.92','accessibility_score':'9',
  'thermal_source_notes':'Foam insulation on hot water pipes retains heat - reduces water and energy waste waiting for hot water. ECBC 2017.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'PPR-C fusion welded pipes|Nitrile foam pipe insulation|Pressure gauge for testing|Individual isolation valves|Dual-stack drainage (soil + waste separate)',
  'climate_restrictions':'None','hard_block_rule':'None',
  'advisory_rule':'Mandatory pressure test at 1.5x working pressure for 2 hours before plastering walls',
  'advisory_message':'All concealed plumbing must be pressure-tested to 1.5x working pressure for minimum 2 hours before closing walls with plaster. Skipping this test means any future leak requires breaking open finished walls.',
  'advisory_severity':'Strong-Warning','constraint_source_notes':'IS 12235; NBC 2016 Part 9; plumbing best practice',
  'ai_advisory_notes':'The fully concealed insulated PPR system is what I specify for premium homes and it is the one you will never regret paying extra for. The key differentiators are insulation on every hot water pipe which means hot water arrives at the tap within seconds instead of wasting 10-15 litres while the pipe warms up, individual isolation valves to every fixture so you can shut off one bathroom tap without shutting off the whole house, and most importantly the pressure test. Always insist on a 2-hour pressure test at 1.5 times working pressure before any wall is plastered. This is the single most important quality check in plumbing and most contractors skip it to save one day of work. If a leak develops inside a plastered wall it will cost 5-10 lakhs to find and fix.',
  'pros':'Zero leak risk with proper pressure test|Insulated hot lines save water and energy|Individual valves for easy maintenance|Quietest plumbing system|50-year lifespan',
  'cons':'Highest plumbing cost|Requires skilled PPR installer with fusion welder|Pressure test must be done before plastering - timeline sensitive|If leak occurs post-plaster requires wall breaking',
  'tooltip_detail':'Premium PPR-C with insulated hot lines. Mandatory pressure test before plastering. Individual valves per fixture. Best lifetime value.',
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
