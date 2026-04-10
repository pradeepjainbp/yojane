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
  'component_id':'MORT-001','category_name':'Structure','subcategory_name':'Mortar Type',
  'name':'mortar_cement_1_6','display_name':'Cement Mortar 1:6','region':'South India',
  'description':'Standard cement mortar in 1:6 ratio (1 part cement to 6 parts sand). Most common masonry mortar for residential construction. Adequate strength for non-load-bearing walls and general brick/block laying.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Basic','sort_order':'1',
  'base_cost_per_sqft_inr':'4','installation_cost_per_sqft_inr':'3','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Karnataka PWD SOR 2024-25 masonry mortar rates; normalized per sqft of wall area',
  'expected_lifespan_years':'40','replacement_cost_factor':'0.3','major_maintenance_cycle_years':'20',
  'major_maintenance_cost_factor':'0.1','annual_minor_maint_factor':'0.005','maintenance_complexity':'Low',
  'lifecycle_source_notes':'IS 2250; mortar joint lifespan in protected masonry 30-50 years',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'6','moisture_resistance':'Medium',
  'fire_rating':'Class A','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'No significant thermal contribution beyond wall material.',
  'max_floors_supported':'6','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'AAC block walls (use thin-bed mortar instead)','compatible_with':'Clay brick|Fly ash brick|Hollow concrete block|Stone masonry',
  'requires_component':'OPC 43 or 53 cement|Clean river sand or M-sand|Water measured by ratio',
  'climate_restrictions':'In coastal zones add waterproofing admixture to mortar to reduce salt penetration.',
  'hard_block_rule':'None',
  'advisory_rule':'Do not use 1:6 mortar for AAC blocks - use thin-bed mortar for AAC',
  'advisory_message':'AAC (Autoclaved Aerated Concrete) blocks require thin-bed mortar of 3-5mm thickness, not standard 1:6 cement mortar. Using thick mortar with AAC defeats the thermal advantage of the block.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 2250; IS 6452',
  'ai_advisory_notes':'Cement mortar 1:6 is the backbone of South India construction and most masons know how to prepare and use it correctly. The key quality control issue is the sand. River sand with excessive silt or clay weakens the mortar significantly - test by making a ball of wet sand and squeezing it: if it crumbles cleanly it is good quality, if it leaves mud it has too much clay. The other issue is water-cement ratio: adding extra water to make the mortar flow easily reduces strength. Mix it to a stiff consistency that holds its shape on the trowel. For AAC block walls you must switch to thin-bed adhesive mortar instead of this mix - the standard 1:6 mortar bed at 10-15mm thickness creates thermal bridges across the fine-cell AAC structure and eliminates most of the thermal benefit.',
  'pros':'Most economical mortar|Widest contractor familiarity|Adequate for all common masonry units except AAC|Good workability',
  'cons':'Not suitable for AAC blocks|Weaker than 1:4 mix|Quality depends on sand quality|Degrades faster in high-moisture conditions',
  'tooltip_detail':'Standard 1:6 mortar. Use for all masonry except AAC blocks. Sand quality critical - reject silty sand.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'MORT-002','category_name':'Structure','subcategory_name':'Mortar Type',
  'name':'mortar_cement_1_4','display_name':'Cement Mortar 1:4 (Stronger Mix)','region':'South India',
  'description':'Stronger cement mortar in 1:4 ratio (1 part cement to 4 parts sand). Used for load-bearing walls, exposed locations, parapet walls, and areas subject to water or structural stress. Higher cement content improves strength and durability.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Intermediate','sort_order':'2',
  'base_cost_per_sqft_inr':'5','installation_cost_per_sqft_inr':'3','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Karnataka PWD SOR 2024-25 masonry rates; 1:4 mix cement premium; normalized per sqft',
  'expected_lifespan_years':'50','replacement_cost_factor':'0.3','major_maintenance_cycle_years':'25',
  'major_maintenance_cost_factor':'0.08','annual_minor_maint_factor':'0.003','maintenance_complexity':'Low',
  'lifecycle_source_notes':'IS 2250; stronger mortar lifespan data',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'7','moisture_resistance':'Medium',
  'fire_rating':'Class A','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'No significant thermal contribution beyond wall material.',
  'max_floors_supported':'6','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'AAC block walls','compatible_with':'Load-bearing brick masonry|Exposed parapet walls|Water tank masonry|Retaining walls',
  'requires_component':'OPC 53 grade cement preferred|Clean sand|Measured water',
  'climate_restrictions':'Use in all coastal and high-rainfall areas for exterior wall courses.',
  'hard_block_rule':'None',
  'advisory_rule':'None','advisory_message':'','advisory_severity':'',
  'constraint_source_notes':'IS 2250; IS 1905 load-bearing masonry',
  'ai_advisory_notes':'The 1:4 mortar is my specification for all load-bearing courses, parapet walls, and any masonry that is exposed to weathering or structural load. The additional cement content meaningfully improves compressive strength and reduces water permeability. At the site level the practical difference is visible - 1:4 mortar is stiffer and harder to work with which is why masons often try to use 1:6 everywhere to make their job easier. For load-bearing walls specify 1:4 and check that the contractor is actually making the correct ratio by watching the batching. A simple check is measuring the proportions by volume using a standard gauge box. The additional cost is trivial compared to the structural importance.',
  'pros':'Higher strength for load-bearing applications|Better durability and moisture resistance than 1:6|Appropriate for exposed locations and parapet walls|Modest cost premium',
  'cons':'Stiffer mix - slightly harder to work|Higher cement cost than 1:6|Not needed for non-load-bearing interior walls|Still not suitable for AAC blocks',
  'tooltip_detail':'1:4 stronger mortar for load-bearing walls and exposed locations. Use OPC 53 cement. Check contractor is batching correctly.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'MORT-003','category_name':'Structure','subcategory_name':'Mortar Type',
  'name':'mortar_thin_bed_aac','display_name':'Thin-Bed Mortar (for AAC Blocks)','region':'South India',
  'description':'Specialist thin-bed adhesive mortar for AAC (Autoclaved Aerated Concrete) block laying. Applied 3-5mm thick versus 10-15mm for standard mortar. Reduces thermal bridging across block joints, key to realising AAC thermal performance. Brands: Ytong Multipor, Weber, Ultratech.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Performance','sort_order':'3',
  'base_cost_per_sqft_inr':'9','installation_cost_per_sqft_inr':'4','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Ytong/Weber thin-bed mortar market rate South India 2024; normalized per sqft of AAC wall area',
  'expected_lifespan_years':'50','replacement_cost_factor':'0.2','major_maintenance_cycle_years':'30',
  'major_maintenance_cost_factor':'0.05','annual_minor_maint_factor':'0.002','maintenance_complexity':'Low',
  'lifecycle_source_notes':'DIN 18550; AAC thin-bed mortar performance data',
  'thermal_resistance_score':'7','acoustic_score':'6','durability_score':'8','moisture_resistance':'Medium',
  'fire_rating':'Class A','energy_impact_modifier':'0.1','accessibility_score':'10',
  'thermal_source_notes':'3-5mm bed reduces thermal bridging at joints by 60-70% versus standard mortar. Key to AAC thermal performance.',
  'max_floors_supported':'6','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'Clay brick|Fly ash brick|Hollow concrete block|Any non-AAC masonry unit',
  'compatible_with':'AAC block (Ytong|Aerocon|Magicrete|Ultratech)',
  'requires_component':'Notched trowel for uniform bed thickness|AAC block system from same manufacturer|Water measured per bag instructions',
  'climate_restrictions':'None',
  'hard_block_rule':'Only use with AAC blocks. Do not use on clay brick or other masonry - bond will fail.',
  'advisory_rule':'None','advisory_message':'','advisory_severity':'',
  'constraint_source_notes':'AAC manufacturer installation guidelines; DIN 18550',
  'ai_advisory_notes':'Thin-bed mortar is non-negotiable if you choose AAC blocks. The entire thermal performance advantage of AAC - the lightweight aerated concrete that acts as a natural insulator - is dramatically reduced if you use standard 10-15mm cement mortar at the joints because the mortar has a much higher conductivity than the AAC block and creates a thermal bypass path at every course. Thin-bed adhesive mortar at 3-5mm thickness reduces this joint thermal bridging by 60-70 percent. Buy the mortar from the same manufacturer as your AAC blocks because the adhesive is formulated for the specific block porosity and surface texture. Use the manufacturer-supplied notched trowel to ensure consistent 3-5mm bed thickness. The cost is higher per bag than cement mortar but you use far less material because of the thin application.',
  'pros':'Essential for AAC thermal performance - eliminates joint thermal bridging|Faster laying than standard mortar|Precise 3-5mm joint reduces material consumption|Manufacturer system warranty when used correctly',
  'cons':'More expensive per sqft than cement mortar|Only works with AAC - wrong choice for other masonry|Requires notched trowel and trained mason|AAC first course levelling critical before thin-bed can be used',
  'tooltip_detail':'Thin-bed mortar for AAC blocks only. 3-5mm joint essential for AAC thermal performance. Buy from same manufacturer as blocks.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'MORT-004','category_name':'Structure','subcategory_name':'Mortar Type',
  'name':'mortar_polymer_modified','display_name':'Polymer-Modified Mortar','region':'South India',
  'description':'Cement mortar with polymer additive (SBR latex or acrylic polymer) mixed in. Better adhesion, flexibility, and water resistance than plain cement mortar. Used for stone cladding, exterior exposed masonry, and areas subject to movement or severe weather.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Premium','sort_order':'4',
  'base_cost_per_sqft_inr':'14','installation_cost_per_sqft_inr':'5','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'SBR latex polymer additive cost; Fosroc/Pidilite/STP market rate 2024; normalized per sqft',
  'expected_lifespan_years':'50','replacement_cost_factor':'0.2','major_maintenance_cycle_years':'25',
  'major_maintenance_cost_factor':'0.05','annual_minor_maint_factor':'0.002','maintenance_complexity':'Low',
  'lifecycle_source_notes':'BS EN 998-2; polymer mortar performance data',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'9','moisture_resistance':'High',
  'fire_rating':'Class A','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'No significant thermal contribution beyond wall material.',
  'max_floors_supported':'6','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'Stone cladding|Exterior exposed masonry|High-movement joints|Coastal construction',
  'requires_component':'SBR latex or acrylic polymer (Fosroc Renderoc|Pidilite Dr Fixit)|OPC cement|Clean sand',
  'climate_restrictions':'Recommended for all coastal construction and high-rainfall zones above 2000mm annual.',
  'hard_block_rule':'None',
  'advisory_rule':'Mix polymer additive at manufacturer-specified ratio - do not reduce to save cost',
  'advisory_message':'Polymer-modified mortar only achieves its performance benefit at the correct polymer-to-cement ratio specified by the manufacturer. Reducing the polymer dose to save cost produces ordinary mortar with higher cost.',
  'advisory_severity':'Warning','constraint_source_notes':'BS EN 998-2; manufacturer product data sheets',
  'ai_advisory_notes':'Polymer-modified mortar is the specification for stone cladding jobs and any exterior masonry in coastal zones where the combination of salt moisture and thermal cycling requires greater adhesion and flexibility than standard cement mortar can provide. The polymer additive improves tensile bond strength by 50-100 percent over plain mortar and adds flexibility that prevents cracking at movement joints. The critical quality control issue is the polymer dosage - the temptation to reduce the additive quantity to save money is real and the result is a mortar with slightly better than ordinary performance at significantly higher cost, which defeats the purpose. I measure the polymer quantity by bucket and add it before the mixing water so both I and the contractor can see the correct dose has been used.',
  'pros':'Best adhesion for stone cladding and exposed masonry|Flexible - resists cracking at movement|Higher moisture resistance|Essential for coastal construction|Long service life',
  'cons':'Highest mortar cost|Polymer dosage must be correctly maintained|Not needed for interior protected masonry|Requires correct mixing sequence',
  'tooltip_detail':'Polymer-modified mortar for stone cladding and coastal exposed masonry. Maintain correct polymer dosage - do not reduce to save cost.',
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
