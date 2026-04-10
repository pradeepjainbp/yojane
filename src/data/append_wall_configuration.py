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
  'component_id':'WCFG-001','category_name':'Envelope','subcategory_name':'Wall Configuration',
  'name':'wall_single_wythe','display_name':'Single Wythe Wall','region':'South India',
  'description':'Standard single thickness wall construction. One layer of masonry units (brick, AAC, or block) bonded with mortar. The most common wall configuration in South India residential construction. Economical and adequate for inland locations with moderate thermal requirements.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Basic','sort_order':'1',
  'base_cost_per_sqft_inr':'0','installation_cost_per_sqft_inr':'0','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Configuration modifier - base cost in wall material selection',
  'expected_lifespan_years':'50','replacement_cost_factor':'1','major_maintenance_cycle_years':'20',
  'major_maintenance_cost_factor':'0.05','annual_minor_maint_factor':'0.005','maintenance_complexity':'Low',
  'lifecycle_source_notes':'Wall configuration lifespan equals wall material lifespan',
  'thermal_resistance_score':'4','acoustic_score':'5','durability_score':'7','moisture_resistance':'Medium',
  'fire_rating':'Class A','energy_impact_modifier':'-0.05','accessibility_score':'10',
  'thermal_source_notes':'Single masonry layer. Moderate thermal mass. Higher heat transmission than cavity configurations.',
  'max_floors_supported':'6','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All masonry wall materials|RCC frame structures',
  'requires_component':'Wall material (B2 selection)|Appropriate mortar (B4 selection)',
  'climate_restrictions':'Not recommended for coastal zones within 5km of sea without additional waterproofing.',
  'hard_block_rule':'None',
  'advisory_rule':'None','advisory_message':'','advisory_severity':'',
  'constraint_source_notes':'NBC 2016; ECBC 2017',
  'ai_advisory_notes':'Single wythe is the standard for the vast majority of residential buildings across South India and it is the correct choice for most situations. The thermal performance depends almost entirely on the wall material chosen in B2 - an AAC block single wythe performs significantly better than a solid clay brick single wythe. Where single wythe walls become inadequate is in very hot coastal zones like Chennai south or Andhra coast where the combination of high temperatures and salt-laden humid air drives serious heat gain through thin walls. For those locations cavity or insulated configurations make a real difference. For typical Bangalore or Mysore residential construction single wythe is the right call.',
  'pros':'Most economical configuration|Widest contractor familiarity|Standard for most South India conditions|Adequate thermal performance with modern wall materials',
  'cons':'Lower thermal performance than cavity configurations|Not suitable for high-heat coastal zones|Less acoustic performance than cavity walls',
  'tooltip_detail':'Standard single wythe wall. Correct for most South India inland residential. Performance depends on wall material choice.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'WCFG-002','category_name':'Envelope','subcategory_name':'Wall Configuration',
  'name':'wall_cavity','display_name':'Cavity Wall (Air Gap)','region':'South India',
  'description':'Double-leaf wall construction with an air gap (50-75mm) between two masonry wythes tied with wall ties. The trapped air significantly reduces heat transmission and provides a moisture break. Recommended for coastal zones, high-humidity regions, and premium thermal performance.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Performance','sort_order':'2',
  'base_cost_per_sqft_inr':'15','installation_cost_per_sqft_inr':'8','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Additional masonry and wall tie cost over single wythe; Karnataka PWD SOR 2024-25 reference; normalized per sqft',
  'expected_lifespan_years':'50','replacement_cost_factor':'1','major_maintenance_cycle_years':'20',
  'major_maintenance_cost_factor':'0.05','annual_minor_maint_factor':'0.005','maintenance_complexity':'Medium',
  'lifecycle_source_notes':'Cavity wall lifespan equals wall material lifespan; cavity must remain clear',
  'thermal_resistance_score':'7','acoustic_score':'7','durability_score':'8','moisture_resistance':'High',
  'fire_rating':'Class A','energy_impact_modifier':'0.15','accessibility_score':'10',
  'thermal_source_notes':'Air cavity significantly reduces heat transmission. U-value reduction 25-35% vs single wythe. ECBC 2017.',
  'max_floors_supported':'4','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'Brick masonry|AAC block|RCC frame structures',
  'requires_component':'Stainless steel or galvanised wall ties at 900mm centres|Cavity fill weep holes at base|Cavity clear of mortar droppings',
  'climate_restrictions':'Strongly recommended for coastal zones within 20km of sea. High value in Warm-Humid and Hot-Dry climates.',
  'hard_block_rule':'None',
  'advisory_rule':'Cavity must be kept clean of mortar droppings during construction to maintain air gap function',
  'advisory_message':'The cavity air gap loses its thermal benefit if filled with mortar droppings during construction. A clean cavity board or cover must be used during each masonry course and removed to clean the cavity. Inspect cavity with endoscope before closing the wall.',
  'advisory_severity':'Warning','constraint_source_notes':'NBC 2016; IS 1905; ECBC 2017',
  'ai_advisory_notes':'Cavity walls are standard practice in the UK and Singapore for good reasons and I strongly recommend them for any construction within 20 kilometres of the South India coast or in zones with high humidity and heat gain. The 50-75mm air gap reduces heat transmission through the wall by 25-35 percent compared to single wythe which translates directly into lower air conditioning loads. The other benefit in coastal areas is the moisture break - salt moisture that penetrates the outer leaf cannot cross the air gap to the inner leaf preventing efflorescence and spalling on internal surfaces. The contractor must use a clean cavity board at each course and pull it up clean to remove mortar droppings. If mortar droppings fill the cavity you get thermal bridging through the solid mortar path and the benefit is lost. This is not difficult to do properly but many contractors are not familiar with the technique and need supervision.',
  'pros':'25-35% reduction in heat gain vs single wythe|Moisture break for coastal areas|Better acoustic performance|Reduced AC loads over building life',
  'cons':'Higher cost than single wythe|Thicker wall reduces internal floor area|Cavity must be kept clean during construction - supervision needed|Wall tie corrosion over time',
  'tooltip_detail':'Cavity wall with air gap. Best for coastal zones and high-humidity areas. Keep cavity clean of mortar droppings during construction.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'WCFG-003','category_name':'Envelope','subcategory_name':'Wall Configuration',
  'name':'wall_insulated_cavity','display_name':'Insulated Cavity Wall','region':'South India',
  'description':'Cavity wall with the air gap partially or fully filled with rigid insulation board (EPS, XPS or Glasswool). Provides maximum thermal resistance. Premium configuration for passive cooling and energy-efficient construction targeting ECBC or IGBC compliance.',
  'climate_zone':'Hot-Dry|Warm-Humid','spectrum_position':'Premium','sort_order':'3',
  'base_cost_per_sqft_inr':'28','installation_cost_per_sqft_inr':'12','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Cavity wall cost plus EPS/XPS board fill; Bangalore insulation contractor rates 2024; normalized per sqft',
  'expected_lifespan_years':'40','replacement_cost_factor':'0.8','major_maintenance_cycle_years':'25',
  'major_maintenance_cost_factor':'0.1','annual_minor_maint_factor':'0.005','maintenance_complexity':'Medium',
  'lifecycle_source_notes':'Insulation material lifespan 25-40 years embedded in cavity; outer masonry lifespan 50 years',
  'thermal_resistance_score':'9','acoustic_score':'8','durability_score':'8','moisture_resistance':'High',
  'fire_rating':'Class B','energy_impact_modifier':'0.25','accessibility_score':'10',
  'thermal_source_notes':'Insulated cavity reduces wall U-value to ECBC compliant levels. 40-50% heat gain reduction vs single wythe.',
  'max_floors_supported':'4','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'Brick masonry|RCC frame structures|IGBC Green Homes compliance',
  'requires_component':'EPS or XPS rigid insulation boards (50mm)|Stainless steel wall ties|Vapour barrier where required|Specialist insulation contractor',
  'climate_restrictions':'Highest value in Hot-Dry zones (Andhra, Telangana, interior Tamil Nadu). Good value in Warm-Humid coastal zones.',
  'hard_block_rule':'None',
  'advisory_rule':'Use closed-cell insulation (XPS or EPS) not open-cell in humid climates',
  'advisory_message':'In Warm-Humid zones only use closed-cell insulation (XPS or EPS) in the cavity. Open-cell materials like Glasswool can absorb moisture in humid conditions reducing effectiveness and creating mould risk.',
  'advisory_severity':'Warning','constraint_source_notes':'ECBC 2017; IS 3792; IS 4671',
  'ai_advisory_notes':'Insulated cavity walls are the specification I recommend for premium energy-efficient homes targeting IGBC Green Homes rating or ECBC compliance because they genuinely deliver passive cooling performance. The combination of the outer masonry thermal mass with the insulation core and the inner masonry leaf produces a wall assembly that keeps indoor temperatures significantly more stable through the day. In a hot-dry zone like Hyderabad or interior Tamil Nadu this can reduce air conditioning run hours by 15-20 percent annually. The installation requires care with the insulation board placement and vapour barrier depending on the climate zone. Use XPS or EPS boards in humid zones - never Glasswool in the cavity because it absorbs moisture and loses its insulating value. This configuration is most cost-effective for houses above 2500 sqft where the AC savings over the building life justify the premium.',
  'pros':'Highest thermal performance - 40-50% heat gain reduction|ECBC and IGBC compliance pathway|Significant AC cost savings over building life|Best acoustic performance',
  'cons':'Highest cost wall configuration|Thicker wall reduces floor area|Requires specialist installation|Insulation material replacement after 25-40 years|Fire rating slightly reduced',
  'tooltip_detail':'Insulated cavity wall. Premium thermal performance. Use XPS/EPS boards only in humid zones - not Glasswool. Best for IGBC/ECBC compliance.',
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
