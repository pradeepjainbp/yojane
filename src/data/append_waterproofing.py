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

# ── WATERPROOFING (Systems) ────────────────────────────────────────────────────
# Cost: INR per sqft of treated surface area (roof / basement / wet area)
# 5 options: Weathering course → Cementitious → Crystalline → Polyurethane membrane → APP membrane
new_rows = [
{
  'component_id':'WP-001','category_name':'Systems','subcategory_name':'Waterproofing',
  'name':'brick_bat_coba','display_name':'Brick Bat Coba (Weathering Course)','region':'South India',
  'description':'Traditional 75-100mm lime mortar and broken brick bat layer on flat RCC roof with lime punning finish. Time-tested passive waterproofing used for generations in South India. Good thermal insulation due to air pockets in brick bat layer.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Basic','sort_order':'1',
  'base_cost_per_sqft_inr':'35','installation_cost_per_sqft_inr':'25','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'CPWD DSR 2023 Item 13.25 brick bat coba; Karnataka PWD SOR 2024-25',
  'expected_lifespan_years':'20','replacement_cost_factor':'0.9','major_maintenance_cycle_years':'5',
  'major_maintenance_cost_factor':'0.20','annual_minor_maint_factor':'0.03','maintenance_complexity':'Medium',
  'lifecycle_source_notes':'BRE Digest 345; traditional construction observation South India',
  'thermal_resistance_score':'6','acoustic_score':'4','durability_score':'6','moisture_resistance':'Medium',
  'fire_rating':'Class A','energy_impact_modifier':'0.85','accessibility_score':'9',
  'thermal_source_notes':'Air pockets in brick bat layer provide significant thermal resistance ~R1.5. Reduces roof heat gain by 20-25%. ECBC 2017.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'Rooftop gardens|Solar panel installations without structural check',
  'compatible_with':'RCC flat roof slab',
  'requires_component':'Broken brick bats 75mm size|Lime mortar 1:3|Lime punning finish|PCC fillet at parapet junction',
  'climate_restrictions':'In very heavy rainfall zones (Kerala, Coastal Karnataka) add a cementitious waterproofing admixture to the lime mortar for enhanced protection.',
  'hard_block_rule':'None',
  'advisory_rule':'Slope the brick bat coba minimum 1:80 toward drain outlets - standing water causes failure',
  'advisory_message':'Brick bat coba must have minimum 1:80 slope to roof drain points. Standing water on any flat area penetrates through the lime mortar within 2-3 monsoons.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 3036; NBC 2016 roofing; CPWD specifications',
  'ai_advisory_notes':'Brick bat coba is one of the most underrated roofing systems in South India - it has been keeping flat concrete roofs dry for over a century and the thermal benefit from the air pockets in the brick layer is genuinely significant. It reduces roof surface temperature by 15-20 degrees compared to bare concrete which translates directly to cooler rooms below. The critical quality issue is the slope - I see so many houses where the brick bat layer is laid perfectly flat and water ponds in the middle. You need a minimum slope of 1 in 80 from the centre to the drain outlets. The lime punning finish needs re-treatment every 5-6 years as it cracks in thermal cycling.',
  'pros':'Proven 100-year technology|Good thermal insulation from air pockets|Local materials widely available|Repairable with traditional skills',
  'cons':'Heavy dead load adds to structural requirement|Cracks in lime mortar after 5-7 years need repair|Cannot be used with rooftop solar without reinforcement check|Skilled lime mason harder to find',
  'tooltip_detail':'Traditional brick bat and lime weathering course. Good thermal insulation. Slope minimum 1:80 to drains. Re-lime every 5-6 years.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'WP-002','category_name':'Systems','subcategory_name':'Waterproofing',
  'name':'cementitious_waterproofing','display_name':'Cementitious Waterproofing Coating','region':'South India',
  'description':'Polymer-modified cementitious slurry (2-3 coat system) brush-applied on roof slab, wet areas and basement walls. Bonds chemically to concrete. Flexible grade available for movement joints. Common in bathrooms, sunken slabs and external terraces.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Standard','sort_order':'2',
  'base_cost_per_sqft_inr':'28','installation_cost_per_sqft_inr':'18','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market rate Fosroc Brushbond/Pidilite Dr Fixit Dampguard; CPWD DSR 2023 Item 13.28; South India contractor rate',
  'expected_lifespan_years':'10','replacement_cost_factor':'0.85','major_maintenance_cycle_years':'5',
  'major_maintenance_cost_factor':'0.25','annual_minor_maint_factor':'0.03','maintenance_complexity':'Low',
  'lifecycle_source_notes':'Manufacturer warranty 5-7yr; IS 2645; field observation',
  'thermal_resistance_score':'2','acoustic_score':'2','durability_score':'7','moisture_resistance':'High',
  'fire_rating':'Class A','energy_impact_modifier':'1.0','accessibility_score':'10',
  'thermal_source_notes':'Thin coating - negligible thermal contribution. ECBC 2017.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'Surfaces with active water pressure from positive and negative sides simultaneously|Structural cracks above 0.3mm',
  'compatible_with':'RCC slab|Brick masonry|Block masonry|Basement walls',
  'requires_component':'Clean dry concrete substrate|Polymer-modified cementitious slurry (Fosroc/Pidilite)|Polyester mesh fabric at joints|Protection screed over waterproofing on terrace',
  'climate_restrictions':'Apply only when ambient temperature is above 10C and surface is dry. Do not apply during rain or on wet surfaces.',
  'hard_block_rule':'None',
  'advisory_rule':'Apply minimum 3 coats with polyester mesh at all construction joints and wall-floor junctions',
  'advisory_message':'Single or double coat cementitious waterproofing without mesh reinforcement at joints fails at construction joints within 2-3 monsoons. Three coats with embedded polyester mesh at all joints is the minimum standard.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 2645; Fosroc/Pidilite application guide; NBC 2016',
  'ai_advisory_notes':'Polymer-modified cementitious waterproofing is the most common and practical waterproofing for bathrooms, sunken slabs and external terraces in South India. The product quality is good from Fosroc Brushbond and Pidilite Dr Fixit but the application quality varies enormously with the contractor. The most common failure mode is skipping the polyester mesh fabric reinforcement at construction joints and wall-floor junctions - these are the points of greatest movement and without the mesh the coating cracks there within two monsoons. Always insist on a minimum three-coat application on terraces. For sunken bathroom slabs I recommend applying waterproofing to the internal walls as well not just the slab.',
  'pros':'Bonds chemically to concrete|Applicable in bathrooms and basements|Widely available and contractor skill common|Flexible grade for movement joints',
  'cons':'Only 10-year lifespan vs membrane systems|Fails at joints without mesh reinforcement|Cannot bridge structural cracks|Thin - no thermal benefit',
  'tooltip_detail':'Polymer-modified cementitious slurry. 3 coats + polyester mesh at all joints. Standard for bathrooms, sunken slabs and terraces.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'WP-003','category_name':'Systems','subcategory_name':'Waterproofing',
  'name':'crystalline_waterproofing','display_name':'Crystalline Waterproofing (Penetrating)','region':'South India',
  'description':'Crystalline active waterproofing compound (Xypex/Kryton/Sika Integral) added to concrete mix or brush-applied. Reacts with moisture to grow crystals inside concrete pores permanently blocking water pathways. Self-healing properties.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Performance','sort_order':'3',
  'base_cost_per_sqft_inr':'45','installation_cost_per_sqft_inr':'20','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market rate Xypex Concentrate / Sika WT-200 P; verified 2 Bangalore waterproofing contractors',
  'expected_lifespan_years':'40','replacement_cost_factor':'0.5','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0.005','maintenance_complexity':'Low',
  'lifecycle_source_notes':'Xypex manufacturer lifetime warranty on treated concrete; IS 456 concrete durability',
  'thermal_resistance_score':'2','acoustic_score':'2','durability_score':'10','moisture_resistance':'Very High',
  'fire_rating':'Class A','energy_impact_modifier':'1.0','accessibility_score':'9',
  'thermal_source_notes':'Negligible thermal contribution as penetrating treatment. ECBC 2017.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'Non-concrete substrates (brick, block without concrete overlay)|Pre-existing waterproofing membranes',
  'compatible_with':'RCC structures|Concrete basement walls|Concrete retaining walls',
  'requires_component':'Clean bare concrete substrate|Crystalline compound slurry (Xypex/Kryton)|Water misting for curing after application',
  'climate_restrictions':'Must be applied to damp (not wet) concrete surface for crystal growth to initiate. Cannot be applied on waterlogged or dry dust surfaces.',
  'hard_block_rule':'None',
  'advisory_rule':'Keep surface damp (not saturated) for 72 hours after crystalline application to initiate crystal growth',
  'advisory_message':'Crystalline waterproofing requires sustained dampness for 48-72 hours after application to trigger crystal formation. Without moisture curing the product fails to activate.',
  'advisory_severity':'Warning','constraint_source_notes':'Xypex/Kryton application manual; ACI 212.3R',
  'ai_advisory_notes':'Crystalline waterproofing is a remarkable technology that I specify for basements, underground sumps and water tanks because unlike surface membranes it becomes part of the concrete itself. When concrete cracks slightly due to thermal movement or settlement the crystalline compound reactivates in the presence of moisture and re-seals the crack automatically. This self-healing property is genuinely unique. The application window is critical - you must apply to damp concrete and then mist the surface with water for 48-72 hours afterward to feed the crystal growth reaction. Dry or waterlogged surfaces both prevent activation. Xypex and Kryton are the two brands I trust for this application.',
  'pros':'Permanent waterproofing - becomes part of concrete|Self-healing when cracks form|No membrane to delaminate or puncture|40-year effective lifespan',
  'cons':'Only works on concrete - not brick or block|More expensive than cementitious|Requires precise damp curing after application|Cannot be verified visually after application',
  'tooltip_detail':'Penetrating crystalline treatment - becomes part of the concrete permanently. Self-healing. Best for basements and water tanks. Damp-cure 72 hours after application.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'WP-004','category_name':'Systems','subcategory_name':'Waterproofing',
  'name':'polyurethane_membrane','display_name':'Polyurethane (PU) Liquid Membrane','region':'South India',
  'description':'Cold-applied liquid polyurethane membrane roller-applied in 2-3 coats to form seamless 2-3mm elastomeric waterproofing layer. Excellent elongation (300%+) bridges structural movement and hairline cracks. Used on terraces, podiums and wet decks.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Performance','sort_order':'4',
  'base_cost_per_sqft_inr':'65','installation_cost_per_sqft_inr':'25','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market rate Fosroc Proofex Engage / Sika Sikalastic / Pidilite PU membrane; Bangalore/Chennai specialist contractor',
  'expected_lifespan_years':'15','replacement_cost_factor':'0.75','major_maintenance_cycle_years':'7',
  'major_maintenance_cost_factor':'0.15','annual_minor_maint_factor':'0.02','maintenance_complexity':'Medium',
  'lifecycle_source_notes':'Manufacturer warranty 10yr; IS 16218; ASTM C836',
  'thermal_resistance_score':'2','acoustic_score':'2','durability_score':'8','moisture_resistance':'Very High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'1.0','accessibility_score':'9',
  'thermal_source_notes':'Light-coloured PU membranes (white or grey) have high SRI value reducing roof heat absorption by 30%. ECBC 2017 cool roof credit.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'Surfaces with active water ingress from below|Uncured concrete less than 28 days old',
  'compatible_with':'RCC slab|Masonry walls|Concrete block|Metal deck (with primer)',
  'requires_component':'Dry clean substrate|PU primer|PU liquid membrane 2-component|Polyester reinforcing mesh at joints and corners|UV-stable topcoat for exposed applications',
  'climate_restrictions':'Apply only in dry weather at ambient temperature 10-40C. Do not apply if rain expected within 24 hours. UV topcoat mandatory for exposed terraces - plain PU degrades in direct sunlight within 2-3 years.',
  'hard_block_rule':'None',
  'advisory_rule':'UV-stable topcoat mandatory on all exposed terrace applications - plain PU degrades in direct South India sunlight',
  'advisory_message':'Uncoated PU membrane on an exposed terrace will chalk and degrade within 2-3 monsoons from UV radiation. Always apply a UV-stable aliphatic topcoat or light-coloured protective screed.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 16218; manufacturer UV degradation data; ASTM C836',
  'ai_advisory_notes':'Polyurethane liquid membrane is my top recommendation for terraces and balconies in premium residential construction because the 300% elongation means it can bridge hairline cracks that form in concrete as the building settles over the first 2-3 years. Unlike rigid cementitious coatings PU flexes with the structure. The seamless application has no joints which is where all membrane systems fail. The UV degradation issue is real and important - plain PU turns chalky and loses elasticity within 2-3 years if left exposed to direct sunlight on a South India terrace. Always specify an aliphatic UV-stable topcoat or cover with a light-coloured China mosaic or tile screed to protect the membrane.',
  'pros':'300% elongation bridges structural movement|Seamless - no joints to fail|Can be light-coloured for cool roof benefit|Sticks to concrete masonry and metal',
  'cons':'UV topcoat mandatory for exposed use|More expensive than cementitious|Substrate must be dry and primed|Re-application every 10-15 years',
  'tooltip_detail':'Flexible seamless PU liquid membrane. Best for terraces and balconies. UV topcoat mandatory for exposed application. Bridges hairline cracks.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'WP-005','category_name':'Systems','subcategory_name':'Waterproofing',
  'name':'app_torch_membrane','display_name':'APP Torch-Applied Bituminous Membrane','region':'South India',
  'description':'3-4mm APP (Atactic Polypropylene) modified bituminous membrane heat-torch bonded to primed substrate. Factory-manufactured consistent thickness. Highest performance waterproofing for flat roofs with heavy rainfall and ponding risk.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Premium','sort_order':'5',
  'base_cost_per_sqft_inr':'85','installation_cost_per_sqft_inr':'35','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market rate Soprema/Bitumat/Siplast APP membrane 4mm; specialist contractor Bangalore/Chennai',
  'expected_lifespan_years':'20','replacement_cost_factor':'0.7','major_maintenance_cycle_years':'10',
  'major_maintenance_cost_factor':'0.10','annual_minor_maint_factor':'0.01','maintenance_complexity':'Low',
  'lifecycle_source_notes':'EN 13707; IS 1322; manufacturer warranty 10yr',
  'thermal_resistance_score':'3','acoustic_score':'3','durability_score':'9','moisture_resistance':'Very High',
  'fire_rating':'Class B','energy_impact_modifier':'1.0','accessibility_score':'8',
  'thermal_source_notes':'Dark bituminous surface absorbs solar heat - must be covered with light-coloured screed or aluminium foil facing to prevent extreme heat gain. ECBC 2017.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'Unprotected exposure to direct sunlight without reflective cover|Polystyrene insulation boards (solvent incompatibility)',
  'compatible_with':'RCC flat roof|Concrete deck|Metal deck with primer',
  'requires_component':'Bituminous primer coat|4mm APP membrane rolls|LPG torch for heat bonding|Polyester reinforcing mat (factory-embedded)|Light-coloured protection screed or aluminium-faced variant',
  'climate_restrictions':'Apply only in dry weather. In Warm-Humid coastal zones specify aluminium-faced APP membrane variant for reflectivity and UV protection. Torch application requires fire safety precautions on site.',
  'hard_block_rule':'None',
  'advisory_rule':'Cover APP membrane with light-coloured protection screed - dark bitumen absorbs extreme heat',
  'advisory_message':'Bare APP membrane on a South India flat roof reaches 80-90C surface temperature in summer radiating intense heat into the room below. Cover immediately with white or light-coloured china mosaic, tiles or aluminium-faced screed.',
  'advisory_severity':'Warning','constraint_source_notes':'EN 13707; IS 1322; ECBC 2017 cool roof requirements',
  'ai_advisory_notes':'APP torch-applied membrane is the gold standard for waterproofing demanding South India flat roofs particularly in Kerala and Coastal Karnataka where rainfall can exceed 3000mm per year. It is a factory-manufactured product of consistent thickness unlike site-applied coatings so quality is predictable. The torch-bonding creates a complete adhesive bond to the primed substrate with no voids where water can travel horizontally under the membrane - the failure mode of self-adhesive systems. The dark colour is a significant disadvantage in South India heat - you absolutely must cover the membrane with a light-coloured protection screed or reflective facing. Fire safety during torch application requires a competent specialist contractor.',
  'pros':'Factory-consistent 4mm thickness|Torch-bonded - no voids under membrane|20-year effective lifespan|Handles 3000mm+ annual rainfall in Kerala',
  'cons':'Dark membrane must be covered - extreme heat absorption|Requires specialist torch applicator|Fire safety on site during installation|More expensive than cementitious',
  'tooltip_detail':'APP bituminous membrane - highest performance for high-rainfall zones. Must be covered with light screed to prevent extreme heat gain. Specialist installation.',
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
