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
  'component_id':'STEEL-001','category_name':'Structure','subcategory_name':'Steel Grade',
  'name':'steel_fe415','display_name':'Fe 415 TMT Steel','region':'South India',
  'description':'Fe 415 grade TMT (Thermo-Mechanically Treated) reinforcement bars per IS 1786. Older BIS standard with 415 N/mm² yield strength. Still available but largely superseded by Fe 500 in modern construction.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Basic','sort_order':'1',
  'base_cost_per_sqft_inr':'28','installation_cost_per_sqft_inr':'8','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Steel market rate South India 2024; Fe415 is rare - estimate based on Fe500 minus 5%; normalized per sqft',
  'expected_lifespan_years':'60','replacement_cost_factor':'0','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'IS 1786; embedded steel lifespan = structure lifespan if no corrosion',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'6','moisture_resistance':'Medium',
  'fire_rating':'Class A','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution as embedded reinforcement.',
  'max_floors_supported':'3','min_floors_required':'1','max_span_supported_m':'4',
  'incompatible_with':'G+3 and above without engineer review|Seismic zones III-V',
  'compatible_with':'M15 PCC|M20 RCC|Low-rise residential up to G+2',
  'requires_component':'IS 1786 BIS certification mark on bars|Mill test certificate',
  'climate_restrictions':'In coastal zones corrosion protection (epoxy-coated bars or stainless) recommended.',
  'hard_block_rule':'None',
  'advisory_rule':'Fe415 is largely obsolete - confirm availability and BIS mark before specifying',
  'advisory_message':'Fe415 has been largely phased out in favour of Fe500. Verify that BIS-certified Fe415 is available from your steel supplier before specifying it.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 1786:2008; NBC 2016',
  'ai_advisory_notes':'Fe415 is essentially legacy steel that you will struggle to find from reputable mills today. Most major producers have moved to Fe500 as their standard grade. The only reason to consider Fe415 is if you are matching existing construction in a renovation or extension project. For new construction there is no practical benefit over Fe500 - Fe500 gives you higher strength which means either stronger members for the same amount of steel or the same strength with less steel weight. If your contractor quotes you Fe415 ask him to show you the BIS certification mark on the bundle tag because there is a real risk of getting substandard steel labelled as Fe415 from small operators. Always insist on a mill test certificate from the manufacturer.',
  'pros':'Available for legacy/matching work|Lower yield stress - slightly more ductile than Fe500 in old designs',
  'cons':'Largely obsolete - hard to source certified material|Lower strength than Fe500|Requires more steel by weight for same structural performance|Not recommended for seismic zones',
  'tooltip_detail':'Fe415 is obsolete. Hard to source with BIS certification. Use Fe500 or Fe500D for all new construction.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'STEEL-002','category_name':'Structure','subcategory_name':'Steel Grade',
  'name':'steel_fe500','display_name':'Fe 500 TMT Steel','region':'South India',
  'description':'Fe 500 grade TMT reinforcement bars per IS 1786. Current BIS standard with 500 N/mm² yield strength. Most widely used grade for residential construction in South India. Good strength-to-cost ratio.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Intermediate','sort_order':'2',
  'base_cost_per_sqft_inr':'32','installation_cost_per_sqft_inr':'8','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'JSW/Tata/SAIL steel prices South India 2024; Fe500 standard grade; normalized per sqft built-up area',
  'expected_lifespan_years':'60','replacement_cost_factor':'0','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'IS 1786; embedded steel lifespan = structure lifespan if no corrosion',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'8','moisture_resistance':'Medium',
  'fire_rating':'Class A','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution as embedded reinforcement.',
  'max_floors_supported':'4','min_floors_required':'1','max_span_supported_m':'5',
  'incompatible_with':'None','compatible_with':'M20 and above concrete|All residential structural systems',
  'requires_component':'IS 1786 BIS certification mark|Mill test certificate from manufacturer',
  'climate_restrictions':'In coastal zones within 5km of sea consider epoxy-coated Fe500 or upgrade to Fe500D.',
  'hard_block_rule':'None',
  'advisory_rule':'Always check BIS certification mark on every bar bundle',
  'advisory_message':'Significant quantities of uncertified or mislabelled steel circulate in South India markets. Check the BIS certification mark and the rolling marks on the bar surface. Insist on a mill test certificate.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 1786:2008; NBC 2016',
  'ai_advisory_notes':'Fe500 is what I specify for the vast majority of residential projects and it is the right choice for G+1 to G+3 construction. The 500 N/mm2 yield strength means you need about 17 percent less steel by weight compared to Fe415 for the same structural performance which partially offsets the slightly higher per-tonne cost. The quality issue I cannot emphasise enough is the proliferation of fake or substandard steel in South India markets. I have tested bars from local dealers that failed at 350 N/mm2 while being sold as Fe500. The protection against this is simple - buy only from authorised distributors of major mills like Tata Tiscon SAIL JSW or RINL and insist on the mill test certificate. Check the BIS certification mark and the raised letters on the bar itself which encode the manufacturer and grade. Never buy steel without these marks regardless of the price advantage.',
  'pros':'Current BIS standard - widely available|Good strength for residential construction|Better value than Fe415 (less weight for same strength)|Major mill products well certified',
  'cons':'Fake/substandard steel common in market - buy from authorised dealers only|Not recommended for seismic zones III-IV (use Fe500D)|Moderate ductility compared to Fe500D',
  'tooltip_detail':'Fe500 standard grade for all residential construction. Buy from authorised dealer only - fake steel is common. Mill test certificate mandatory.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'STEEL-003','category_name':'Structure','subcategory_name':'Steel Grade',
  'name':'steel_fe500d_ductile','display_name':'Fe 500D — Ductile Grade','region':'South India',
  'description':'Fe 500D grade TMT bars per IS 1786. Same 500 N/mm² yield strength as Fe500 but with enhanced ductility (higher elongation at failure) critical for seismic performance. The D suffix denotes ductile. Recommended for all seismic zone III and IV construction.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Performance','sort_order':'3',
  'base_cost_per_sqft_inr':'35','installation_cost_per_sqft_inr':'9','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'JSW/Tata Tiscon Fe500D premium over Fe500; South India market 2024; normalized per sqft',
  'expected_lifespan_years':'60','replacement_cost_factor':'0','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'IS 1786; IS 13920 seismic ductility requirements',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'9','moisture_resistance':'Medium',
  'fire_rating':'Class A','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution as embedded reinforcement.',
  'max_floors_supported':'6','min_floors_required':'1','max_span_supported_m':'6',
  'incompatible_with':'None','compatible_with':'M20 and above concrete|All structural systems|Seismic zone III-IV construction',
  'requires_component':'IS 1786 BIS certification mark with D designation|Mill test certificate showing UTS/YS ratio and elongation',
  'climate_restrictions':'None',
  'hard_block_rule':'None',
  'advisory_rule':'Verify D grade marking on bars - plain Fe500 is sometimes supplied instead',
  'advisory_message':'Confirm the D grade designation on both the mill test certificate and the bar marking. Some suppliers substitute plain Fe500 for Fe500D. The bar rolling marks should include the D designation.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 1786:2008; IS 13920:2016; NBC 2016',
  'ai_advisory_notes':'Fe500D is my default specification for any new residential construction in South India and the cost premium over plain Fe500 is minimal - typically 3-5 percent per tonne. The reason to always choose the D grade is ductility. In an earthquake the energy is dissipated through controlled plastic deformation of the steel. Plain Fe500 can be brittle at failure whereas Fe500D has the higher elongation specified in IS 13920 which means it bends before it breaks giving occupants critical seconds to exit. Most of Karnataka is in seismic zone II to III and parts of the Western Ghats coast are zone III - this is not a theoretical risk. The practical issue is verification - always check that the mill test certificate shows the UTS/YS ratio above 1.25 and elongation above 16 percent as specified in IS 1786 for the D grade. These numbers are what make it seismically ductile.',
  'pros':'Enhanced ductility critical for seismic performance|IS 13920 compliant for earthquake zones|Same strength as Fe500 with better failure behaviour|Minimal cost premium over Fe500',
  'cons':'Slightly higher cost than plain Fe500|Must verify D grade marking - substitution risk|Not widely stocked at all small dealers',
  'tooltip_detail':'Fe500D ductile grade. Recommended for all South India construction. Verify D marking on bars and mill certificate. Small cost premium over Fe500.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'STEEL-004','category_name':'Structure','subcategory_name':'Steel Grade',
  'name':'steel_fe550','display_name':'Fe 550 — High Strength','region':'South India',
  'description':'Fe 550 grade TMT bars per IS 1786. 550 N/mm² yield strength - the highest standard grade for residential use. Allows reduction in steel quantity by approximately 10% compared to Fe500. For G+4 and above, seismic zone IV-V, and heavily loaded structures.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Premium','sort_order':'4',
  'base_cost_per_sqft_inr':'40','installation_cost_per_sqft_inr':'10','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'SAIL/RINL Fe550 market rate South India 2024; normalized per sqft',
  'expected_lifespan_years':'60','replacement_cost_factor':'0','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'IS 1786; high-strength steel performance data',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'10','moisture_resistance':'Medium',
  'fire_rating':'Class A','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution as embedded reinforcement.',
  'max_floors_supported':'10','min_floors_required':'1','max_span_supported_m':'8',
  'incompatible_with':'None','compatible_with':'M25 and above concrete|G+4 and above structures|Heavy commercial construction',
  'requires_component':'IS 1786 BIS certification mark|Structural engineer design approval|RMC M25+ concrete',
  'climate_restrictions':'None',
  'hard_block_rule':'None',
  'advisory_rule':'Only specify when structural engineer has designed for Fe550 strength - not a drop-in replacement for Fe500',
  'advisory_message':'Fe550 changes the structural design - bar diameters and quantities will be different from an Fe500 design. Only use when your structural engineer has specifically designed for this grade.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 1786:2008; NBC 2016',
  'ai_advisory_notes':'Fe550 is specified by structural engineers for tall residential buildings and heavily loaded transfer structures where the higher yield strength allows a meaningful reduction in steel quantity and therefore construction cost at scale. For a typical 30x40 or 40x60 plot G+2 or G+3 house the cost saving does not justify the reduced availability and the need for a specific structural redesign. If your structural engineer has specified Fe550 it is because the member sizes or loading genuinely benefit from the higher grade - do not ask him to downgrade to Fe500 to save a few rupees because the design will need to be reworked. The availability of genuinely certified Fe550 is more limited than Fe500 so insist on major mill supply with test certificates.',
  'pros':'Highest standard residential grade - maximum structural efficiency|Allows smaller member sizes for same load|Best for G+4+ and heavily loaded structures',
  'cons':'Must be specifically designed for - not a drop-in replacement|Less widely available than Fe500/Fe500D|Higher cost|Requires M25+ concrete to realise full benefit',
  'tooltip_detail':'Fe550 high strength for G+4+ and heavily loaded structures. Must be specifically designed for. Not a direct substitute for Fe500.',
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
