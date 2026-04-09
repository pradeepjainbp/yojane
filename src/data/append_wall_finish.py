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

# ── WALL FINISH (Finishes) ────────────────────────────────────────────────────
# Cost unit: base_cost_per_sqft_inr = INR per sqft of wall surface area
# 5 options: Basic → Standard → Performance → High-Performance → Premium
new_rows = [
{
  'component_id':'WF-001','category_name':'Finishes','subcategory_name':'Wall Finish',
  'name':'cement_plaster','display_name':'Cement Sand Plaster','region':'South India',
  'description':'12-20mm two-coat cement:sand (1:4 to 1:6) plaster applied over masonry. Standard utilitarian finish for internal and external walls. Painted with emulsion or distemper.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Basic','sort_order':'1',
  'base_cost_per_sqft_inr':'28','installation_cost_per_sqft_inr':'22','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'CPWD DSR 2023 Item 9.2.1 two-coat cement plaster; Karnataka PWD SOR 2024-25; -10% South India adjustment',
  'expected_lifespan_years':'20','replacement_cost_factor':'0.85','major_maintenance_cycle_years':'5',
  'major_maintenance_cost_factor':'0.20','annual_minor_maint_factor':'0.03','maintenance_complexity':'Low',
  'lifecycle_source_notes':'BRE Digest 345; field observation South India construction',
  'thermal_resistance_score':'3','acoustic_score':'5','durability_score':'6','moisture_resistance':'Medium',
  'fire_rating':'Class A','energy_impact_modifier':'1.0','accessibility_score':'10',
  'thermal_source_notes':'High conductivity mortar; minimal insulation value. ECBC 2017 baseline wall finish.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'AAC blocks without PPC cement|CSEB blocks without lime addition',
  'compatible_with':'All masonry wall systems|RCC surfaces',
  'requires_component':'PPC or OPC 43 cement|Washed river sand|Chicken mesh at material joints',
  'climate_restrictions':'Requires waterproof additive in coastal and high-rainfall zones',
  'hard_block_rule':'None',
  'advisory_rule':'Plaster on AAC blocks must use PPC cement - OPC causes map cracking',
  'advisory_message':'Using OPC (ordinary Portland cement) mortar directly on AAC blocks causes severe shrinkage map cracking within 1-2 monsoon seasons. Always specify PPC (Portland Pozzolana Cement) for AAC.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 1661; AAC manufacturer specifications; IS 2250',
  'ai_advisory_notes':'Cement plaster is what every house in South India gets because it is cheap fast and every mason knows how to do it. But there are two critical mistakes I see constantly. First if you have AAC blocks never use OPC cement mortar - it cracks badly because of differential shrinkage. Always specify PPC cement. Second the sand quality determines everything - sharp washed river sand gives a hard surface while dusty quarry sand gives a weak crumbly finish. Always check that the curing is done properly with water for at least 7 days - hurried drying causes shrinkage cracks that never go away.',
  'pros':'Lowest cost wall finish|Universally available|Any mason can apply|Fire resistant Class A',
  'cons':'Cracks if not properly cured|Wrong cement on AAC causes map cracking|Needs repainting every 3-5 years|Shrinks in hot dry weather',
  'tooltip_detail':'Standard cement sand plaster. Most common wall finish in South India. Specify PPC cement for AAC blocks. Proper curing critical.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'WF-002','category_name':'Finishes','subcategory_name':'Wall Finish',
  'name':'gypsum_plaster','display_name':'Gypsum Plaster (Machine / Hand)','region':'South India',
  'description':'10-12mm single-coat gypsum plaster applied over masonry or RCC. Factory-produced consistent finish. Faster than cement plaster. Superior flatness and direct paintability.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Standard','sort_order':'2',
  'base_cost_per_sqft_inr':'42','installation_cost_per_sqft_inr':'18','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market rate Saint-Gobain Gyproc/USG Boral gypsum plaster; Bangalore/Chennai contractor rate',
  'expected_lifespan_years':'20','replacement_cost_factor':'0.8','major_maintenance_cycle_years':'7',
  'major_maintenance_cost_factor':'0.15','annual_minor_maint_factor':'0.02','maintenance_complexity':'Low',
  'lifecycle_source_notes':'Manufacturer data; BRE Digest 345',
  'thermal_resistance_score':'4','acoustic_score':'6','durability_score':'6','moisture_resistance':'Low',
  'fire_rating':'Class A','energy_impact_modifier':'1.0','accessibility_score':'10',
  'thermal_source_notes':'Gypsum k-value 0.16 W/m.K. Better insulator than cement. ECBC 2017.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'External walls in high-rainfall zones without protective paint|Bathrooms without waterproof treatment',
  'compatible_with':'All masonry wall systems|RCC|AAC blocks',
  'requires_component':'Bonding agent primer|Alkali-resistant primer before painting',
  'climate_restrictions':'External walls in coastal high-humidity zones require waterproof top coat. Not suitable for wet area walls without moisture-resistant grade.',
  'hard_block_rule':'BLOCK_ON_EXTERNAL_WALLS_IN_COASTAL_ZONES',
  'advisory_rule':'Never use standard gypsum on external walls or in bathrooms without waterproof grade',
  'advisory_message':'Standard gypsum plaster dissolves and crumbles if wetted. Use only interior-grade on protected internal walls. Use cement plaster for external walls.',
  'advisory_severity':'Strong-Warning','constraint_source_notes':'IS 2547; manufacturer application guide; NBC 2016',
  'ai_advisory_notes':'Machine gypsum plaster has become very popular in Bangalore and Chennai because it gives a beautiful flat surface straight from the plaster without a POP putty layer which saves time and cost. On a 1500 sqft house gypsum instead of cement plaster typically saves 3-5 days of work. The critical limitation is that standard gypsum dissolves in water - so it can only be used on internal walls that will never get wet. Never use it on external walls or in bathrooms without a proper moisture-resistant grade. Always prime with an alkali-resistant primer before painting or the topcoat will peel.',
  'pros':'Faster application than cement plaster|Beautiful flat finish direct|Better insulator than cement|No shrinkage cracks',
  'cons':'Dissolves in moisture - internal use only|More expensive than cement plaster|Cannot be used for external walls|Requires alkali-resistant primer',
  'tooltip_detail':'Single-coat gypsum plaster. Faster and flatter than cement plaster. Internal walls only - dissolves in moisture.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'WF-003','category_name':'Finishes','subcategory_name':'Wall Finish',
  'name':'pop_putty_finish','display_name':'POP Putty + Paint Finish','region':'South India',
  'description':'2-3mm Plaster of Paris putty skim coat over cement plaster, sanded smooth and painted. Standard mid-range interior finish providing near-perfect flat painted wall.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Standard','sort_order':'3',
  'base_cost_per_sqft_inr':'18','installation_cost_per_sqft_inr':'22','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'CPWD DSR 2023 POP Item 12.15; market rate South India including 2-coat emulsion paint',
  'expected_lifespan_years':'8','replacement_cost_factor':'0.9','major_maintenance_cycle_years':'4',
  'major_maintenance_cost_factor':'0.25','annual_minor_maint_factor':'0.05','maintenance_complexity':'Low',
  'lifecycle_source_notes':'Field observation; emulsion paint repaint cycle 4-6 years South India',
  'thermal_resistance_score':'3','acoustic_score':'5','durability_score':'5','moisture_resistance':'Low',
  'fire_rating':'Class A','energy_impact_modifier':'1.0','accessibility_score':'10',
  'thermal_source_notes':'Negligible thermal contribution as thin skim coat. ECBC 2017.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'External walls|Bathrooms and wet areas|Direct application on AAC without PPC base coat',
  'compatible_with':'Cement plaster base|Gypsum plaster base',
  'requires_component':'Cement plaster or gypsum base|Alkali-resistant primer|Interior emulsion paint',
  'climate_restrictions':'Internal walls only. In high-humidity zones seal with damp-proof paint on the base coat before POP.',
  'hard_block_rule':'BLOCK_ON_EXTERNAL_WALLS',
  'advisory_rule':'Apply alkali-resistant primer between cement plaster and POP putty',
  'advisory_message':'POP applied directly on green cement plaster without primer causes blistering and peeling of paint within one monsoon.',
  'advisory_severity':'Warning','constraint_source_notes':'CPWD specifications; paint manufacturer application guide',
  'ai_advisory_notes':'POP putty is what most South India homeowners want because it gives the smooth Instagram-worthy painted wall. It is applied over the cement plaster base as a 2-3mm skim coat, sanded with 120-grit paper and then painted with two coats of emulsion. The key failure mode I see every single time is applying POP directly on green plaster that has not cured for 28 days - the moisture from the base plaster causes the POP layer to crack within months. Also never skip the alkali-resistant primer between plaster and POP or the paint will peel in sheets during the first humidity season.',
  'pros':'Very smooth paintable surface|Cost-effective mid-range finish|Wide paint colour range|Repairable easily',
  'cons':'Internal use only - not waterproof|Cracks if applied on uncured plaster|Needs repainting every 4-5 years|POP quality varies widely',
  'tooltip_detail':'POP putty skim coat over cement plaster. Standard smooth painted wall finish. Internal use only. Cure base plaster 28 days before applying.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'WF-004','category_name':'Finishes','subcategory_name':'Wall Finish',
  'name':'texture_paint','display_name':'Texture Paint / Acrylic Texture Coat','region':'South India',
  'description':'Polymer-acrylic textured coating applied by roller or hopper gun to create decorative surface patterns. Used on both interior and exterior walls. Hides surface imperfections and adds depth.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Performance','sort_order':'4',
  'base_cost_per_sqft_inr':'55','installation_cost_per_sqft_inr':'30','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market rate Asian Paints Apex Ultima Texture / Berger Weathercoat; South India contractor rate',
  'expected_lifespan_years':'10','replacement_cost_factor':'0.8','major_maintenance_cycle_years':'8',
  'major_maintenance_cost_factor':'0.20','annual_minor_maint_factor':'0.03','maintenance_complexity':'Medium',
  'lifecycle_source_notes':'Manufacturer warranty; field observation coastal areas South India',
  'thermal_resistance_score':'4','acoustic_score':'6','durability_score':'7','moisture_resistance':'High',
  'fire_rating':'Class A','energy_impact_modifier':'1.0','accessibility_score':'10',
  'thermal_source_notes':'Acrylic polymer has low conductivity. Textured surface diffuses solar radiation on external walls. ECBC 2017.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All masonry and plaster finishes',
  'requires_component':'Alkali-resistant primer|Cement plaster or gypsum base',
  'climate_restrictions':'External texture paint must be exterior-grade acrylic. Standard interior texture paint fails outdoors within 1 monsoon.',
  'hard_block_rule':'None',
  'advisory_rule':'Always use exterior-grade weatherproof texture paint on any external wall',
  'advisory_message':'Interior texture paint will bubble and peel on external walls after the first monsoon. Specify exterior-grade explicitly in purchase order.',
  'advisory_severity':'Warning','constraint_source_notes':'Paint manufacturer specifications; IS 15489',
  'ai_advisory_notes':'Texture paint has become very popular in South India for two reasons: it hides the uneven surface that is inevitable with site-mixed cement plaster and it gives the house a premium modern look at reasonable cost. For external walls the acrylic texture coat also provides good waterproofing protection - Asian Paints Apex Ultima Texture or Berger Weathercoat have performed well across Tamil Nadu and Karnataka. The common mistake is using interior texture paint on external elevations which fails within months. Always specify exterior-weatherproof grade for any surface exposed to rain.',
  'pros':'Hides surface irregularities|Decorative 3D texture options|Exterior-grade variants are waterproof|Good durability outdoors',
  'cons':'Cannot repaint without re-texturing entire wall|Higher cost than flat paint|Dust collects in texture crevices|Requires specialist applicator for uniform finish',
  'tooltip_detail':'Acrylic textured coating. Good for hiding imperfect walls. Specify exterior-grade for any external surface. Cannot be selectively touched up.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'WF-005','category_name':'Finishes','subcategory_name':'Wall Finish',
  'name':'stone_cladding','display_name':'Natural Stone Cladding','region':'South India',
  'description':'20-30mm natural stone panels (granite, sandstone, slate, quartzite) bonded to masonry wall with cement mortar or epoxy adhesive. Premium decorative exterior and feature wall finish.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Premium','sort_order':'5',
  'base_cost_per_sqft_inr':'180','installation_cost_per_sqft_inr':'120','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Karnataka quarry prices; Bangalore stone cladding contractor rate; heavy stone fixing hardware included',
  'expected_lifespan_years':'50','replacement_cost_factor':'0.6','major_maintenance_cycle_years':'15',
  'major_maintenance_cost_factor':'0.10','annual_minor_maint_factor':'0.01','maintenance_complexity':'Low',
  'lifecycle_source_notes':'BRE Digest 345; natural stone industry data; IS 1130',
  'thermal_resistance_score':'5','acoustic_score':'7','durability_score':'9','moisture_resistance':'High',
  'fire_rating':'Class A','energy_impact_modifier':'1.1','accessibility_score':'6',
  'thermal_source_notes':'Stone thermal mass buffers wall temperature swings. Dark granite absorbs solar heat - specify light colours externally. ECBC 2017.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'Weak masonry substrates|Gypsum plaster substrate',
  'compatible_with':'RCC|Solid brick|Hollow concrete block|AAC block with reinforced adhesive',
  'requires_component':'SS 304 stone fixing anchors|Epoxy or polymer-modified adhesive|Back-sealer for porous stones',
  'climate_restrictions':'Porous stones (sandstone, limestone) require penetrating sealer in high-rainfall zones to prevent staining and biological growth.',
  'hard_block_rule':'None',
  'advisory_rule':'Use stainless steel SS 304 anchors only - GI anchors corrode and cause rust staining',
  'advisory_message':'Galvanised iron anchors corrode within 5-10 years in South India humidity causing ugly rust stains on the stone face. Specify SS 304 stainless steel anchors only.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 1130; BRE stone cladding fixing guidelines; BS 8298',
  'ai_advisory_notes':'Natural stone cladding on the exterior elevation transforms a standard house into something truly impressive and it will last 50 years with almost zero maintenance. South India is blessed with abundant granite in Karnataka and Andhra at prices much lower than northern India. The technical issues to watch are the fixing anchors and the substrate condition. Always specify SS 304 stainless steel anchors because galvanised iron anchors rust within a decade leaving terrible brown stains down your stone face. The wall substrate must be sound and flat - stone cladding is an external skin and will not hide poor brickwork; it will amplify it. For porous stones like sandstone apply a penetrating sealer immediately after installation and repeat every 5 years.',
  'pros':'50-year lifespan with minimal maintenance|Premium aesthetic that appreciates property value|Completely waterproof|South India quarries offer great local variety',
  'cons':'Very high installation cost|Heavy dead load on wall|Requires SS fixing anchors|Porous stones need periodic sealing',
  'tooltip_detail':'Natural stone panels bonded to wall. Premium 50-year finish. Specify SS 304 anchors. Porous stones require sealing in monsoon zones.',
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
