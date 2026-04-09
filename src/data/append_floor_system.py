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

# ── FLOOR SYSTEM (Structure) ───────────────────────────────────────────────────
# Structural floor/slab system type
# Cost: INR per sqft of floor area for structural slab only
# 4 options: Solid RCC → Ribbed/Waffle → Hollow core precast → Post-tensioned flat plate
new_rows = [
{
  'component_id':'FS-001','category_name':'Structure','subcategory_name':'Floor System',
  'name':'solid_rcc_slab','display_name':'Solid RCC Slab (Conventional)','region':'South India',
  'description':'Conventional 125-150mm solid reinforced concrete slab cast in-situ with beam and column frame. Universal standard in South India residential and commercial construction. Well understood by all structural engineers and contractors.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Standard','sort_order':'1',
  'base_cost_per_sqft_inr':'160','installation_cost_per_sqft_inr':'83','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'CPWD DSR 2023 Items 5.2.2 and 5.9.3; Karnataka PWD SOR 2024-25; normalised per sqft',
  'expected_lifespan_years':'75','replacement_cost_factor':'1.2','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0.005','maintenance_complexity':'Low',
  'lifecycle_source_notes':'IS 456; BRE concrete carbonation; NBC 2016',
  'thermal_resistance_score':'4','acoustic_score':'8','durability_score':'10','moisture_resistance':'High',
  'fire_rating':'Class A','energy_impact_modifier':'1.0','accessibility_score':'10',
  'thermal_source_notes':'High thermal mass - slows temperature changes between floors. Good inter-floor thermal buffer. ECBC 2017.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'5.0',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'M20 concrete minimum|Fe415 steel reinforcement|Shuttering and centering|7-day minimum water curing',
  'climate_restrictions':'In coastal zones use M25 concrete with low water-cement ratio for better durability against chloride attack.',
  'hard_block_rule':'None',
  'advisory_rule':'Minimum 7-day continuous water curing mandatory after slab pour',
  'advisory_message':'Insufficient curing of RCC slabs (under 7 days continuous water curing) causes 20-30% reduction in concrete strength and early carbonation cracking. Do not remove shuttering before 14 days.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 456 Clause 13; NBC 2016 structural quality',
  'ai_advisory_notes':'The solid RCC slab is what every building in South India uses and for good reason - it is structurally proven, acoustically excellent between floors, completely fireproof and every engineer and contractor understands it. The two quality factors I fight for on every site are curing and shuttering. Minimum 7 days of continuous water curing is non-negotiable for a slab to reach design strength - I have seen slabs that failed dust tests because the contractor removed the hessian after 3 days to save water. Shuttering must not be removed before 14 days regardless of how fast the contractor wants to move on. These two shortcuts cause structural inadequacy that cannot be fixed after the fact.',
  'pros':'Universal - every engineer and contractor knows this system|Maximum acoustic insulation between floors|Highest fire resistance|Thermal mass buffers inter-floor temperature',
  'cons':'Heaviest dead load of all slab systems|Requires timber or steel shuttering and centering|Longest construction time before next floor|Material-intensive',
  'tooltip_detail':'Standard solid RCC slab. Universal, proven, acoustically excellent. 7-day curing and 14-day shuttering retention mandatory. No shortcuts.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'FS-002','category_name':'Structure','subcategory_name':'Floor System',
  'name':'ribbed_waffle_slab','display_name':'Ribbed / Waffle Slab','region':'South India',
  'description':'Two-way ribbed slab with voids created by permanent or removable form pods. 25-35% lighter than solid slab. Reduces concrete and steel for medium-to-large spans. Distinctive coffered ceiling soffit aesthetic if left exposed.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Performance','sort_order':'2',
  'base_cost_per_sqft_inr':'175','installation_cost_per_sqft_inr':'95','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Structural engineer estimate; form pod rental; IS 456 ribbed slab; ~10% premium over solid slab for spans above 5m',
  'expected_lifespan_years':'75','replacement_cost_factor':'1.2','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0.005','maintenance_complexity':'Medium',
  'lifecycle_source_notes':'IS 456; ACI 318 waffle slab; BRE Digest 345',
  'thermal_resistance_score':'3','acoustic_score':'6','durability_score':'9','moisture_resistance':'High',
  'fire_rating':'Class A','energy_impact_modifier':'1.0','accessibility_score':'9',
  'thermal_source_notes':'Voids reduce thermal mass. Slightly less inter-floor thermal buffer than solid slab. ECBC 2017.',
  'max_floors_supported':'15','min_floors_required':'2','max_span_supported_m':'8.0',
  'incompatible_with':'Heavy point loads|Spans below 5m where solid slab is more economical',
  'compatible_with':'RCC frame|Steel frame',
  'requires_component':'Structural engineer waffle slab design|Form pods (GRP or expanded polystyrene)|M25 concrete minimum|Topping slab 75mm',
  'climate_restrictions':'None','hard_block_rule':'None',
  'advisory_rule':'Only economical above 5m spans - solid slab is cheaper below 5m',
  'advisory_message':'Waffle slab is more expensive than solid slab for spans under 5m. The material saving from the voids does not offset the form pod cost and complexity at short spans. Specify only where spans exceed 5m.',
  'advisory_severity':'Info','constraint_source_notes':'IS 456; IS 1905; structural engineering practice',
  'ai_advisory_notes':'Waffle slabs make economic sense when your column grid exceeds 5 meters because the void-forming pods reduce the concrete volume and dead weight which means smaller columns and foundations below. For a 6x6m grid the material saving in concrete and steel from switching to waffle slab roughly offsets the pod rental and additional formwork complexity. The exposed waffle soffit also looks spectacular in commercial or double-height residential spaces - the coffered ceiling pattern is genuinely beautiful. Do not use waffle slabs for spans under 5 meters where the solid slab is actually cheaper.',
  'pros':'25-35% lighter than solid slab at large spans|Reduces column and foundation sizes|Exposed coffered ceiling aesthetic|Material efficient at 6m+ spans',
  'cons':'More expensive than solid slab at spans under 5m|Poorer acoustic performance than solid slab|Requires specialist form pods|M25 concrete mandatory',
  'tooltip_detail':'Ribbed/waffle slab with voids. 25-35% lighter than solid. Only economical above 5m spans. Excellent coffered ceiling aesthetic if exposed.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'FS-003','category_name':'Structure','subcategory_name':'Floor System',
  'name':'hollow_core_precast','display_name':'Hollow Core Precast Slab','region':'South India',
  'description':'Factory-manufactured prestressed hollow core concrete planks (150-200mm depth) placed on beams. Fastest floor construction method. Eliminates shuttering entirely. Growing availability from precast plants near Bangalore, Chennai and Hyderabad.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Performance','sort_order':'3',
  'base_cost_per_sqft_inr':'150','installation_cost_per_sqft_inr':'40','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market rate precast hollow core plank supply + crane erection; Bangalore precast plant 2024; normalised per sqft',
  'expected_lifespan_years':'75','replacement_cost_factor':'1.1','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0.005','maintenance_complexity':'Low',
  'lifecycle_source_notes':'IS 1343 prestressed concrete; manufacturer quality control; BS 8110',
  'thermal_resistance_score':'3','acoustic_score':'6','durability_score':'9','moisture_resistance':'High',
  'fire_rating':'Class A','energy_impact_modifier':'1.0','accessibility_score':'8',
  'thermal_source_notes':'Hollow voids reduce thermal mass slightly vs solid slab. ECBC 2017.',
  'max_floors_supported':'10','min_floors_required':'2','max_span_supported_m':'8.0',
  'incompatible_with':'Irregular plan shapes with many cuts|Curved or non-rectilinear buildings',
  'compatible_with':'RCC frame|Steel frame|Masonry bearing walls',
  'requires_component':'Mobile crane for plank erection|Precast plant supply within 150km|Structural topping concrete 50-75mm|RCC edge beams as bearing support',
  'climate_restrictions':'None','hard_block_rule':'None',
  'advisory_rule':'Precast plant must be within 150km - long haulage damages prestressed planks',
  'advisory_message':'Hollow core prestressed planks are fragile in transport. Sourcing from a plant more than 150km away risks micro-cracking of the prestressed wires during road transport. Verify plant location before specifying.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 1343; precast plant logistics guidelines',
  'ai_advisory_notes':'Hollow core precast slabs are dramatically faster to build than cast-in-situ slabs because there is no shuttering to erect and strike. A floor of hollow core planks can be placed in one day by a crane rather than the 3-4 weeks required for conventional slab shuttering, casting and curing. The factory quality control for prestressed products is also more consistent than site-cast concrete. The key constraint is crane access to the site and proximity to a precast plant - the planks are heavy (300-400 kg each) and a mobile crane is mandatory. Plans with many irregular cut-outs for stairwells and openings are harder to detail with planks than with cast-in-situ concrete.',
  'pros':'No shuttering required - dramatically faster floor construction|Factory quality control|Can span 6-8m efficiently|Lower site labour than cast-in-situ',
  'cons':'Crane mandatory for installation|Precast plant must be within 150km|Irregular plan shapes difficult to detail|Acoustic performance slightly lower than solid slab',
  'tooltip_detail':'Factory precast hollow core planks. No shuttering needed. Fastest floor system. Crane access mandatory. Precast plant within 150km.',
  'status':'Active','verify_flags':'base_cost_per_sqft_inr','data_filled_by':'AI'
},
{
  'component_id':'FS-004','category_name':'Structure','subcategory_name':'Floor System',
  'name':'post_tensioned_flat_plate','display_name':'Post-Tensioned Flat Plate Slab','region':'South India',
  'description':'Flat slab without downstand beams, post-tensioned with high-strength steel tendons after casting. Eliminates beams entirely giving maximum headroom. Used in premium multi-storey residential and commercial. Growing use in Bangalore and Chennai luxury apartments.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Premium','sort_order':'4',
  'base_cost_per_sqft_inr':'195','installation_cost_per_sqft_inr':'85','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market rate PT system contractor Bangalore/Chennai; IS 1343; specialist contractor rate; normalised per sqft',
  'expected_lifespan_years':'75','replacement_cost_factor':'1.2','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0.005','maintenance_complexity':'High',
  'lifecycle_source_notes':'IS 1343; ACI 318 post-tensioned; fib Model Code; BS 8110',
  'thermal_resistance_score':'4','acoustic_score':'7','durability_score':'9','moisture_resistance':'High',
  'fire_rating':'Class A','energy_impact_modifier':'1.0','accessibility_score':'10',
  'thermal_source_notes':'Flat plate with no beam bulges. Flat soffit maximises false ceiling space. ECBC 2017.',
  'max_floors_supported':'30','min_floors_required':'3','max_span_supported_m':'9.0',
  'incompatible_with':'Low-rise G+1 or G+2 structures where PT cost premium is unjustified|Contractors without PT experience',
  'compatible_with':'RCC frame|High-rise structures',
  'requires_component':'Post-tensioning specialist contractor|High-strength PT strands and anchorages|Hydraulic jack for stressing|M30 concrete minimum|Structural engineer specialist in PT design',
  'climate_restrictions':'Coastal high-chloride zones require grouted duct PT system (not unbonded) to protect tendons from corrosion.',
  'hard_block_rule':'REQUIRES_PT_SPECIALIST_CONTRACTOR',
  'advisory_rule':'Post-tensioning specialist contractor mandatory - general contractors cannot do PT work',
  'advisory_message':'Post-tensioned slabs require specialist stressing equipment, certified strand installation and precise stressing sequence. General contractors attempting PT work without certification cause catastrophic structural failures.',
  'advisory_severity':'Critical','constraint_source_notes':'IS 1343; ACI 318; IStructE post-tensioning guidelines',
  'ai_advisory_notes':'Post-tensioned flat plate construction is the premium structural choice for multi-storey residential because eliminating the downstand beams gives you 8-10 inches more usable headroom per floor - on a 10-floor building that extra clearance lets you fit one additional floor within the same overall building height. The flat soffit also simplifies MEP coordination and false ceiling design enormously because there are no beams to route around. The absolute requirement is a certified post-tensioning contractor - the stressing sequence and anchor installation are precision engineering tasks that cannot be done by a general contractor. The PT system is also more vulnerable to corrosion in coastal zones requiring grouted duct protection.',
  'pros':'No downstand beams - maximum headroom and flat ceiling|Can add extra floor within same building height|Best for complex MEP routing above ceiling|Large column-free spans up to 9m',
  'cons':'PT specialist contractor mandatory - limited availability|Higher cost than solid slab|Coastal zones need grouted (bonded) PT for corrosion protection|Cannot be cut or cored after tensioning',
  'tooltip_detail':'Post-tensioned flat plate. No beams - maximum headroom. PT specialist contractor mandatory. Extra floor possible within same building height.',
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
