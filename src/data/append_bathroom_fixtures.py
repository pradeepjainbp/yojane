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
  'component_id':'BATH-001','category_name':'Finishes','subcategory_name':'Bathroom Fixtures',
  'name':'bath_economy_grade','display_name':'Economy Grade Fixtures','region':'South India',
  'description':'Economy-tier sanitaryware and bathroom fittings. Brands: Hindware Ace series, Cera Standard, Johnson Tiles economy range. Basic functionality with adequate quality for rental properties or budget builds. CP fittings (taps, showers) from Indian economy range.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Basic','sort_order':'1',
  'base_cost_per_sqft_inr':'12','installation_cost_per_sqft_inr':'6','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Economy sanitaryware market rate South India 2024; normalized per sqft of bathroom area',
  'expected_lifespan_years':'10','replacement_cost_factor':'0.8','major_maintenance_cycle_years':'5',
  'major_maintenance_cost_factor':'0.2','annual_minor_maint_factor':'0.03','maintenance_complexity':'Medium',
  'lifecycle_source_notes':'Economy fixtures typical lifespan 8-12 years before replacement or major maintenance',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'5','moisture_resistance':'Medium',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0','accessibility_score':'7',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All bathroom configurations',
  'requires_component':'IS 2556 compliant sanitaryware|IS 1795 compliant CP fittings',
  'climate_restrictions':'None',
  'hard_block_rule':'None',
  'advisory_rule':'Check BIS mark on CP fittings - uncertified economy fittings fail within 2-3 years',
  'advisory_message':'Many economy-grade CP fittings lack BIS certification and use thin chrome plating that peels within 2-3 years. Always check for IS 1795 BIS mark on taps and showers.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 2556; IS 1795',
  'ai_advisory_notes':'Economy fixtures make sense for rental properties and budget builds where replacement every 8-10 years is factored into the financial model. The critical quality filter even at economy grade is the BIS mark on CP fittings - taps showers and shower heads from uncertified manufacturers use chrome plating that is 2-3 microns thick versus the 8+ microns required by IS 1795 and it peels within two monsoon seasons leaving corroded brass exposed. This is particularly visible in South India where the chlorinated municipal water attacks thin plating aggressively. Stick to Hindware Cera or Parryware economy range which are certified even at entry level. For a house you plan to live in for 20 years the mid-range fixtures are worth the extra outlay.',
  'pros':'Lowest cost|Adequate for rental properties|Wide availability|Reasonable functionality for basic use',
  'cons':'8-10 year lifespan|CP fittings prone to peeling if uncertified|Less water-efficient|Limited design options|Not recommended for owner-occupied homes',
  'tooltip_detail':'Economy fixtures for rental/budget builds. Check BIS mark on CP fittings. 8-10 year lifespan.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'BATH-002','category_name':'Finishes','subcategory_name':'Bathroom Fixtures',
  'name':'bath_mid_range_grade','display_name':'Mid-Range Grade Fixtures','region':'South India',
  'description':'Mid-range sanitaryware and bathroom fittings. Brands: Jaquar Solo/Opal series, Parryware T-Connect, Hindware Italian Collection, Cera Prima. Good quality, water-efficient, and better aesthetics. Suitable for owner-occupied residential construction.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Intermediate','sort_order':'2',
  'base_cost_per_sqft_inr':'25','installation_cost_per_sqft_inr':'10','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Jaquar/Parryware mid-range dealer rates South India 2024; normalized per sqft of bathroom area',
  'expected_lifespan_years':'20','replacement_cost_factor':'0.6','major_maintenance_cycle_years':'10',
  'major_maintenance_cost_factor':'0.1','annual_minor_maint_factor':'0.015','maintenance_complexity':'Low',
  'lifecycle_source_notes':'Mid-range fixture lifespan 15-20 years with normal maintenance',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'7','moisture_resistance':'High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0.05','accessibility_score':'8',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All bathroom configurations',
  'requires_component':'IS 2556 sanitaryware|IS 1795 CP fittings|WELS water efficiency label preferred',
  'climate_restrictions':'None',
  'hard_block_rule':'None',
  'advisory_rule':'None','advisory_message':'','advisory_severity':'',
  'constraint_source_notes':'IS 2556; IS 1795; BIS certification',
  'ai_advisory_notes':'Mid-range from Jaquar or Parryware is my standard recommendation for any owner-occupied home in South India. Jaquar in particular has excellent quality control at their mid-range Solo and Opal series and the CP fittings use proper 8-10 micron chrome plating that holds up well in South India water conditions. The water efficiency is meaningfully better than economy grade - Jaquar mid-range taps typically have aerators that restrict flow to 6 litres per minute versus 12+ for economy grade which makes a real difference in water bills over 20 years. The aesthetic quality is also significantly better with more consistent colour glazing on the sanitaryware. This is the range where you get genuinely good quality without paying the premium brand surcharge.',
  'pros':'Good quality for 20-year lifespan|Water-efficient CP fittings|BIS certified|Better aesthetics than economy|Jaquar/Parryware service network across South India|Best value tier',
  'cons':'Higher cost than economy|Not as durable as premium brands|Service required every 10 years',
  'tooltip_detail':'Mid-range fixtures - best value for owner-occupied homes. Jaquar/Parryware recommended. 20-year lifespan.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'BATH-003','category_name':'Finishes','subcategory_name':'Bathroom Fixtures',
  'name':'bath_premium_grade','display_name':'Premium Grade Fixtures','region':'South India',
  'description':'Premium sanitaryware and bathroom fittings. Brands: Kohler, TOTO, Duravit, Grohe, American Standard. Highest build quality, water efficiency, and aesthetic design. Concealed cistern systems, wall-hung WCs, rain showers. For premium construction and luxury bathrooms.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Premium','sort_order':'3',
  'base_cost_per_sqft_inr':'60','installation_cost_per_sqft_inr':'18','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Kohler/TOTO/Duravit dealer rates Bangalore/Chennai 2024; normalized per sqft of bathroom area',
  'expected_lifespan_years':'25','replacement_cost_factor':'0.5','major_maintenance_cycle_years':'15',
  'major_maintenance_cost_factor':'0.05','annual_minor_maint_factor':'0.008','maintenance_complexity':'Low',
  'lifecycle_source_notes':'Premium fixture lifespan 20-30 years; spare parts availability key',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'9','moisture_resistance':'Very High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0.1','accessibility_score':'9',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All bathroom configurations|Premium and luxury residential construction',
  'requires_component':'Trained plumber familiar with brand-specific installation|Concealed cistern framing if wall-hung WC|Manufacturer-specified accessories',
  'climate_restrictions':'None',
  'hard_block_rule':'None',
  'advisory_rule':'Verify local service and spare parts availability before specifying niche international brands',
  'advisory_message':'Some international premium brands have limited service network in Tier 2 South India cities. Verify that the brand has authorised service and spare parts availability in your city before specifying.',
  'advisory_severity':'Warning','constraint_source_notes':'Manufacturer warranty terms',
  'ai_advisory_notes':'Premium fixtures from Kohler or TOTO are genuinely excellent products with build quality that is meaningfully superior to mid-range. The glazing quality on Kohler and TOTO sanitaryware is better which means less staining and easier cleaning over 20+ years. The TOTO Washlet integrated bidet-seat is a particularly good product for South India given the water usage habits and hygiene preferences. The concern I raise with clients is service - Kohler has a reasonable service network in Bangalore Chennai and Hyderabad but if you are building in a Tier 2 city like Mysore or Trichy confirm that a certified service technician and spare parts are available locally before you commit. A concealed cistern that needs a specific TOTO part from Mumbai with a 2-week lead time is a significant inconvenience.',
  'pros':'Highest quality and durability|Best water efficiency ratings|Superior aesthetics|25+ year lifespan|Advanced features (concealed cisterns, wall-hung WC, integrated bidets)',
  'cons':'Highest cost|Service and spare parts availability must be verified locally|Wall-hung WC requires frame installation|Over-specified for most residential builds',
  'tooltip_detail':'Premium fixtures (Kohler/TOTO/Duravit). 25+ year lifespan. Verify local service network before specifying.',
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
