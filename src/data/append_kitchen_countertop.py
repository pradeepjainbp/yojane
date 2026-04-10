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
  'component_id':'CTOP-001','category_name':'Finishes','subcategory_name':'Kitchen Countertop',
  'name':'countertop_ceramic_tile','display_name':'Ceramic Tile Countertop','region':'South India',
  'description':'Kitchen countertop finished with ceramic or vitrified tiles on a masonry or concrete base. Economical option with wide variety of colours and patterns. Grout joints require regular maintenance to prevent staining and bacterial growth.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Basic','sort_order':'1',
  'base_cost_per_sqft_inr':'25','installation_cost_per_sqft_inr':'10','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Tile + masonry base + epoxy grout contractor rates Bangalore 2024; normalized per sqft of countertop area',
  'expected_lifespan_years':'15','replacement_cost_factor':'0.7','major_maintenance_cycle_years':'5',
  'major_maintenance_cost_factor':'0.15','annual_minor_maint_factor':'0.02','maintenance_complexity':'Medium',
  'lifecycle_source_notes':'Tile countertop lifespan limited by grout staining and tile edge chipping',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'5','moisture_resistance':'Medium',
  'fire_rating':'Class A','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All kitchen configurations',
  'requires_component':'Vitrified tiles (anti-bacterial glaze preferred)|Epoxy grout (not regular cement grout)|Masonry or concrete base|Edge tiles or trim',
  'climate_restrictions':'None',
  'hard_block_rule':'None',
  'advisory_rule':'Use epoxy grout not cement grout - cement grout stains permanently within 1-2 years',
  'advisory_message':'Standard cement grout on kitchen countertop joints absorbs oil and food stains permanently within one to two years. Use only epoxy grout for kitchen countertop tile joints.',
  'advisory_severity':'Warning','constraint_source_notes':'Tile manufacturer guidelines',
  'ai_advisory_notes':'Tile countertops are the economy option and they come with the caveat that grout maintenance is an ongoing commitment. The most critical choice is the grout - if the contractor uses standard cement grout on your kitchen counter it will be permanently stained with oil and turmeric within one monsoon season. Insist on epoxy grout which is more expensive but is stain-proof and non-porous. The other issue is edge tiles which chip over time especially at corners. A preferable detail is a bull-nose edge tile or a stainless steel edge trim that protects the vulnerable tile corner. For a rental property or a budget build where replacement is planned within 15 years the tile counter is a pragmatic choice. For your own home I would push towards granite.',
  'pros':'Lowest cost|Wide colour and pattern range|Easy local repair of damaged tiles|Adequate for rental or budget builds',
  'cons':'Grout joints stain and harbour bacteria|Tile edges chip at corners|Shorter lifespan than stone or quartz|Cement grout must be replaced with epoxy grout|Not ideal for high-use kitchens',
  'tooltip_detail':'Tile countertop. Use epoxy grout only - cement grout stains permanently. Vitrified tile preferred over ceramic.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'CTOP-002','category_name':'Finishes','subcategory_name':'Kitchen Countertop',
  'name':'countertop_granite','display_name':'Granite Countertop','region':'South India',
  'description':'Natural granite stone slab countertop, typically 18-20mm thick. Most popular premium kitchen countertop in South India. Extremely durable, heat-resistant, and hygienic when sealed. Available in a wide range of South Indian granite varieties at competitive prices.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Intermediate','sort_order':'2',
  'base_cost_per_sqft_inr':'55','installation_cost_per_sqft_inr':'18','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'South India granite market rate 2024; Indian granite varieties; polished 18mm slab; normalized per sqft',
  'expected_lifespan_years':'30','replacement_cost_factor':'0.6','major_maintenance_cycle_years':'10',
  'major_maintenance_cost_factor':'0.05','annual_minor_maint_factor':'0.005','maintenance_complexity':'Low',
  'lifecycle_source_notes':'Granite countertop lasts 25-30+ years with proper sealing; sealing required every 2-3 years',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'9','moisture_resistance':'High',
  'fire_rating':'Class A','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'High thermal mass - stays cool. Good for South India kitchens.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All kitchen configurations',
  'requires_component':'Granite sealer (applied before and after installation)|Stainless steel sink cutout|Silicone sealant at wall joint|RCC or masonry counter base',
  'climate_restrictions':'None',
  'hard_block_rule':'None',
  'advisory_rule':'Seal granite before installation and after installation - unsealed granite absorbs oil stains',
  'advisory_message':'Unsealed granite absorbs oil and turmeric stains readily. Apply stone sealer before installation and after installation when dry. Reseal every 2-3 years.',
  'advisory_severity':'Warning','constraint_source_notes':'Natural Stone Institute sealing guidelines',
  'ai_advisory_notes':'Granite is my recommendation for the vast majority of South India kitchen countertops and the reason is simple - it is extremely hard wearing heat resistant and the price of good quality Indian granite is very competitive because we quarry it right here in Karnataka Tamil Nadu and Andhra. A Krishna White or Steel Grey or Tan Brown granite counter will last 25-30 years with minimal maintenance. The important detail is sealing - all granite must be sealed before it goes in and again after installation because unsealed granite will absorb turmeric and cooking oil stains. Apply the sealer let it penetrate and wipe off the excess. Reseal every 2-3 years. The other thing to insist on is that the underside of the granite is properly supported - unsupported granite over sink cutouts more than 400mm wide can crack. Your fabricator should provide stainless steel or granite support bars.',
  'pros':'Best durability for South India use - 30 year lifespan|Heat resistant|Competitive price for Indian granite varieties|Hygienic when sealed|Wide range of South India granite patterns|Adds property value',
  'cons':'Requires sealing every 2-3 years|Heavy - counter structure must be adequate|Cracks if unsupported over large cutouts|Porous if unsealed',
  'tooltip_detail':'Granite countertop. Best value for South India. Seal before and after installation. Reseal every 2-3 years.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'CTOP-003','category_name':'Finishes','subcategory_name':'Kitchen Countertop',
  'name':'countertop_solid_surface','display_name':'Solid Surface (Corian/HI-MACS)','region':'South India',
  'description':'Homogeneous acrylic or polyester solid surface material (Corian, HI-MACS, Staron). Non-porous, seamless at joints, and surface scratches can be sanded out. Good for island countertops and modern aesthetic. Moderate heat resistance - requires trivets.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Performance','sort_order':'3',
  'base_cost_per_sqft_inr':'90','installation_cost_per_sqft_inr':'22','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Corian/HI-MACS dealer rates Bangalore/Chennai 2024; thermoforming + install; normalized per sqft',
  'expected_lifespan_years':'20','replacement_cost_factor':'0.7','major_maintenance_cycle_years':'10',
  'major_maintenance_cost_factor':'0.1','annual_minor_maint_factor':'0.01','maintenance_complexity':'Medium',
  'lifecycle_source_notes':'Solid surface lifespan 15-25 years; surface renewal possible by sanding',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'7','moisture_resistance':'Very High',
  'fire_rating':'Class B','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All kitchen configurations|Island countertops|Modern minimalist kitchens',
  'requires_component':'Certified solid surface fabricator|Trivet policy for hot pans|Special adhesive for seams',
  'climate_restrictions':'None',
  'hard_block_rule':'None',
  'advisory_rule':'Always use trivets for hot pans - solid surface has lower heat resistance than granite',
  'advisory_message':'Solid surface materials have a maximum continuous heat exposure of around 175°C. Direct contact with hot cookware can cause whitening or warping. Always use trivets or hot pads.',
  'advisory_severity':'Warning','constraint_source_notes':'Corian/HI-MACS product technical data',
  'ai_advisory_notes':'Solid surface is the right choice when you want a seamless countertop particularly for island kitchens where an integrated undermount sink without a joint is aesthetically important and hygienic. The non-porous nature means zero maintenance for stains - just wipe down. The limitation that most clients do not realise until they have it installed is the heat sensitivity. In a South India kitchen where you are handling a pressure cooker or kadai you must always use a trivet. A single contact with a hot stainless steel vessel can cause permanent whitening of the surface. The surface scratch renewal feature is real - a certified fabricator can sand out surface marks with an orbital sander and bring it back to new condition which is genuinely useful after 8-10 years of use.',
  'pros':'Seamless non-porous surface - no staining|Integrated sink possible with no visible joint|Surface scratches sandable - renewable|Modern minimal aesthetic|Easy to clean',
  'cons':'Lower heat resistance than granite - trivets mandatory|Higher cost than granite|Certified fabricator required for good seams|Shorter lifespan than granite|Repair requires specialist',
  'tooltip_detail':'Solid surface countertop. Non-porous and seamless. Always use trivets - lower heat resistance than granite.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'CTOP-004','category_name':'Finishes','subcategory_name':'Kitchen Countertop',
  'name':'countertop_engineered_quartz','display_name':'Engineered Quartz (Silestone/Caesarstone)','region':'South India',
  'description':'Engineered stone countertop made from 90-95% quartz crystals bound with polymer resin. Non-porous, consistent colour, extremely hard, and does not require sealing. Premium choice combining stone durability with consistent aesthetics.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Premium','sort_order':'4',
  'base_cost_per_sqft_inr':'120','installation_cost_per_sqft_inr':'28','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Silestone/Caesarstone/Quantra dealer rates South India 2024; normalized per sqft',
  'expected_lifespan_years':'25','replacement_cost_factor':'0.6','major_maintenance_cycle_years':'15',
  'major_maintenance_cost_factor':'0.03','annual_minor_maint_factor':'0.003','maintenance_complexity':'Low',
  'lifecycle_source_notes':'Quartz countertop manufacturer lifespan data; 20-25 year typical lifespan',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'10','moisture_resistance':'Very High',
  'fire_rating':'Class B','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All kitchen configurations|Modern premium kitchens',
  'requires_component':'Certified fabricator with water-jet cutter|Trivet policy for hot pans|Silicone at wall joint',
  'climate_restrictions':'None',
  'hard_block_rule':'None',
  'advisory_rule':'Trivets required - engineered quartz is heat sensitive despite high hardness',
  'advisory_message':'Despite being harder than granite engineered quartz is sensitive to high heat due to the polymer resin binder. Thermal shock from hot cookware can cause cracking or discolouration. Always use trivets.',
  'advisory_severity':'Warning','constraint_source_notes':'Quartz manufacturer technical data',
  'ai_advisory_notes':'Engineered quartz is the premium choice I recommend when the client wants zero maintenance and consistent aesthetics because unlike natural granite it requires no sealing and has completely consistent colour and pattern without the natural variation of stone. The 90+ percent quartz content makes it the hardest countertop material available and it is completely non-porous so there is literally nothing to maintain beyond wiping it down. The limitation shared with solid surface is heat sensitivity - the polymer resin that binds the quartz crystals can crack or discolour under thermal shock from a hot kadai. This is a significant limitation in a South Indian kitchen where high-temperature cooking is standard. Always use trivets. The price premium over granite is substantial but for a client who wants a showpiece kitchen that remains pristine with zero maintenance effort it is justified.',
  'pros':'Hardest countertop material available|Zero maintenance - no sealing required|Completely non-porous|Consistent colour and pattern|Best stain resistance|25-year lifespan',
  'cons':'Highest cost|Heat sensitive - trivets mandatory|Not suitable for direct contact with Indian high-heat cooking|Certified fabricator required|Heavier than solid surface',
  'tooltip_detail':'Engineered quartz. Hardest and lowest maintenance. Heat sensitive - trivets mandatory for Indian cooking. Premium cost.',
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
