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

# ── CEILING (Finishes) ────────────────────────────────────────────────────────
# Cost unit: base_cost_per_sqft_inr = INR per sqft of ceiling/floor area
# 5 options: Bare slab → POP false ceiling → Gypsum board → Wooden → Metal tile
new_rows = [
{
  'component_id':'CEIL-001','category_name':'Finishes','subcategory_name':'Ceiling',
  'name':'bare_slab_painted','display_name':'Bare RCC Slab (Painted)','region':'South India',
  'description':'Exposed RCC slab soffit cleaned, POP skim-patched and painted with ceiling emulsion. No false ceiling. Maximum ceiling height retained. Standard in utility, service and budget construction.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Basic','sort_order':'1',
  'base_cost_per_sqft_inr':'18','installation_cost_per_sqft_inr':'12','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'CPWD DSR 2023 Item 12.15 POP patching + ceiling paint; market rate South India',
  'expected_lifespan_years':'10','replacement_cost_factor':'0.95','major_maintenance_cycle_years':'5',
  'major_maintenance_cost_factor':'0.30','annual_minor_maint_factor':'0.05','maintenance_complexity':'Low',
  'lifecycle_source_notes':'Repaint cycle 4-6 years; BRE Digest 345',
  'thermal_resistance_score':'2','acoustic_score':'3','durability_score':'9','moisture_resistance':'High',
  'fire_rating':'Class A','energy_impact_modifier':'1.0','accessibility_score':'10',
  'thermal_source_notes':'Exposed concrete slab radiates stored heat downward at night. No insulation layer. ECBC 2017 baseline.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'Ducted AC|Concealed electrical in false ceiling',
  'compatible_with':'All structural systems',
  'requires_component':'Alkali-resistant primer|Ceiling emulsion paint|Scaffolding for painting',
  'climate_restrictions':'In Hot-Dry zones bare concrete ceiling retains daytime heat and radiates it into living spaces at night - thermal discomfort without AC.',
  'hard_block_rule':'None',
  'advisory_rule':'Ducted AC cannot be installed without a false ceiling space for ductwork',
  'advisory_message':'If you plan ducted air conditioning now or in the future, you must install a false ceiling with minimum 9-inch plenum depth. Bare slab blocks this option permanently.',
  'advisory_severity':'Warning','constraint_source_notes':'ECBC 2017; NBC 2016; ASHRAE 62.1',
  'ai_advisory_notes':'Bare painted slab is the most economical ceiling option and actually looks quite good in modern minimalist interiors if the slab soffit is reasonably flat and well-finished. The key advantage is maximum ceiling height - you retain every inch of your 10 or 11 foot floor-to-floor height rather than losing 10-12 inches to a false ceiling frame. The main functional limitation is that all electrical conduit and AC piping must be planned to chase along the walls because there is no ceiling void to hide them. If you ever decide to add ducted AC later you will need to add a false ceiling at that point which costs more as a retrofit.',
  'pros':'Maximum ceiling height retained|No maintenance beyond repainting|Exposed slab looks modern when flat|Lowest cost option',
  'cons':'Exposes all electrical conduit - must plan carefully|No space for ducted AC|Bare concrete radiates heat downward at night|Slab imperfections visible',
  'tooltip_detail':'Painted bare RCC slab. Maximum height retained. No space for ducted AC or concealed wiring. Repaint every 5 years.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'CEIL-002','category_name':'Finishes','subcategory_name':'Ceiling',
  'name':'pop_false_ceiling','display_name':'POP False Ceiling (Plaster of Paris)','region':'South India',
  'description':'Plaster of Paris false ceiling on galvanised MS channel frame suspended from RCC slab. Smooth paintable surface with integrated lighting provision. Most popular false ceiling in South India residential.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Standard','sort_order':'2',
  'base_cost_per_sqft_inr':'90','installation_cost_per_sqft_inr':'50','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'CPWD DSR 2023 Item 12.16; Karnataka PWD SOR 2024-25; market rate Bangalore/Chennai POP ceiling contractor',
  'expected_lifespan_years':'15','replacement_cost_factor':'0.9','major_maintenance_cycle_years':'7',
  'major_maintenance_cost_factor':'0.20','annual_minor_maint_factor':'0.03','maintenance_complexity':'Medium',
  'lifecycle_source_notes':'BRE Digest 345; field observation South India - humidity cycles cause joint cracking',
  'thermal_resistance_score':'4','acoustic_score':'5','durability_score':'6','moisture_resistance':'Low',
  'fire_rating':'Class A','energy_impact_modifier':'1.1','accessibility_score':'9',
  'thermal_source_notes':'Air gap between slab and POP surface reduces downward heat radiation. ECBC 2017.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'Bathrooms without moisture-resistant treatment|High-humidity rooms without exhaust',
  'compatible_with':'All structural systems',
  'requires_component':'GI channel perimeter and intermediate frame|Hanger wires from slab|POP compound|Recessed light provisions|MS anchors',
  'climate_restrictions':'In bathrooms and kitchens use moisture-resistant gypsum board instead of POP - standard POP dissolves with steam over time.',
  'hard_block_rule':'None',
  'advisory_rule':'Never use POP in bathrooms - use moisture-resistant gypsum board instead',
  'advisory_message':'POP false ceiling in bathrooms absorbs steam and collapses within 3-5 years. Specify MR gypsum board for any wet area false ceiling.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 2547; manufacturer application guidelines',
  'ai_advisory_notes':'POP false ceiling is what most South India homeowners want because it gives a smooth premium-looking ceiling with nice integrated downlights and it hides all the electrical conduit and AC piping. The quality is almost entirely down to the plasterer - a good POP worker creates a surface you cannot distinguish from a smooth wall while a bad one leaves visible joint lines and uneven surfaces within a year. The critical quality check is the GI frame - insist on minimum 0.5mm galvanised channel sections and hanger wires every 4 feet. Cheap thin frames sag and crack the POP within 3-5 years especially in the humidity of coastal South India.',
  'pros':'Smooth seamless finish|Hides all conduit and AC piping|Integrated lighting design possible|Thermal buffer vs bare slab',
  'cons':'Dissolves in moisture - not for bathrooms|Joint lines appear with frame sag|Difficult to repair patches invisibly|Reduces ceiling height by 10-12 inches',
  'tooltip_detail':'Most popular residential false ceiling. Smooth finish, hides conduit. Specify GI frame 0.5mm+ gauge. Never in bathrooms - use MR gypsum there.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'CEIL-003','category_name':'Finishes','subcategory_name':'Ceiling',
  'name':'gypsum_board_ceiling','display_name':'Gypsum Board False Ceiling (Drywall)','region':'South India',
  'description':'12.5mm gypsum dryboard on GI metal stud frame with taped and jointed seamless finish. Superior flatness, moisture-resistant grades available for bathrooms. Faster installation than POP.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Performance','sort_order':'3',
  'base_cost_per_sqft_inr':'125','installation_cost_per_sqft_inr':'55','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market rate Saint-Gobain Gyproc/USG Boral 12.5mm dryboard + GI frame; Bangalore/Chennai contractor rate',
  'expected_lifespan_years':'20','replacement_cost_factor':'0.85','major_maintenance_cycle_years':'10',
  'major_maintenance_cost_factor':'0.15','annual_minor_maint_factor':'0.02','maintenance_complexity':'Low',
  'lifecycle_source_notes':'Manufacturer 10yr warranty; BS EN 520; BRE Digest 345',
  'thermal_resistance_score':'5','acoustic_score':'7','durability_score':'7','moisture_resistance':'Medium',
  'fire_rating':'Class A','energy_impact_modifier':'1.1','accessibility_score':'9',
  'thermal_source_notes':'Gypsum board k-value 0.16 W/m.K better insulator than POP compound. Air gap aids further. ECBC 2017.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'GI stud and track frame|12.5mm gypsum board|Joint compound and mesh tape|Alkali-resistant primer|Moisture-resistant (MR) grade for bathrooms',
  'climate_restrictions':'Specify moisture-resistant (MR) grade boards for bathrooms and kitchens. Standard gypsum board absorbs moisture in wet areas.',
  'hard_block_rule':'None',
  'advisory_rule':'Specify MR grade gypsum board in all wet area ceilings - bathrooms, toilets, kitchens',
  'advisory_message':'Standard gypsum board swells and sags in bathroom steam within 2-3 years. MR grade is mandatory for any moisture-exposed ceiling.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 2095; BS EN 520; manufacturer application guide',
  'ai_advisory_notes':'Gypsum board gives a flatter and more consistent ceiling than POP because it is factory-manufactured to precise thickness unlike site-mixed POP compound. The jointing and taping skill matters enormously - a trained drywall finisher creates invisible joints while an untrained one leaves visible ridges. For bathrooms and kitchens always specify MR (moisture-resistant) grade pink-faced board which costs only 20-25% more but will not sag. The fire rating is genuinely better than POP because the crystalline water bound in gypsum releases when heated which delays fire spread - a real safety benefit for upper floors.',
  'pros':'Better fire rating than POP|MR grade available for wet areas|Factory consistent thickness = flatter ceiling|Faster installation than POP',
  'cons':'More expensive than POP|Joint lines visible if taped poorly|Reduces ceiling height|Damaged boards cannot be POP-patched easily',
  'tooltip_detail':'Drywall false ceiling. Better fire rating and flatness than POP. Specify MR grade for bathrooms. Requires skilled joint taping.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'CEIL-004','category_name':'Finishes','subcategory_name':'Ceiling',
  'name':'wooden_ceiling','display_name':'Timber / Wooden Ceiling Panel','region':'South India',
  'description':'Solid hardwood, engineered wood or timber veneer panels on concealed MS clip or T-bar framework. Traditional South India heritage aesthetic or contemporary linear wood look. Feature ceilings in living and dining areas.',
  'climate_zone':'Warm-Humid|Temperate','spectrum_position':'Premium','sort_order':'4',
  'base_cost_per_sqft_inr':'280','installation_cost_per_sqft_inr':'90','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market rate engineered wood or teak veneer panel + MS T-bar; Bangalore/Chennai interior contractor',
  'expected_lifespan_years':'30','replacement_cost_factor':'0.7','major_maintenance_cycle_years':'5',
  'major_maintenance_cost_factor':'0.15','annual_minor_maint_factor':'0.02','maintenance_complexity':'Medium',
  'lifecycle_source_notes':'BRE Digest 345; IS 287; engineered wood manufacturer data',
  'thermal_resistance_score':'6','acoustic_score':'8','durability_score':'7','moisture_resistance':'Low',
  'fire_rating':'Class C','energy_impact_modifier':'1.0','accessibility_score':'8',
  'thermal_source_notes':'Wood k-value 0.13 W/m.K excellent insulator. Air gap above panel adds further resistance. ECBC 2017.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'Bathrooms|Kitchens|High-humidity rooms without exhaust fans',
  'compatible_with':'All structural systems',
  'requires_component':'MS T-bar or clip frame|Timber oil or lacquer finish|Vapour barrier in humid climates',
  'climate_restrictions':'Not suitable for bathrooms, kitchens or any high-humidity space. Coastal high-salinity zones require marine-grade wood treatment. Not recommended in Hot-Dry zones without humidity control.',
  'hard_block_rule':'BLOCK_IN_BATHROOMS_AND_WET_AREAS',
  'advisory_rule':'Verify timber moisture content below 12% before installation',
  'advisory_message':'Wood ceiling panels installed with moisture content above 12% will warp and pull away from the frame in the first monsoon. Kiln-dried timber is mandatory.',
  'advisory_severity':'Strong-Warning','constraint_source_notes':'IS 287; IS 4021 timber seasoning',
  'ai_advisory_notes':'A timber ceiling in the living or dining area creates warmth and character that no other material can match and it has excellent acoustic properties - the room stops echoing. Engineered wood veneer panels are better than solid wood for ceiling applications because they are dimensionally stable and do not warp with seasonal humidity changes the way solid planks do. Always specify kiln-dried timber with moisture content below 12% and apply a penetrating oil or lacquer finish before installation to seal the wood from humidity. Avoid solid timber ceilings in coastal Kerala or Chennai where the high ambient humidity causes expansion and contraction that loosens fixings over time.',
  'pros':'Outstanding acoustic absorption - eliminates echo|Warm natural aesthetic|Excellent thermal insulation|Long lifespan with proper treatment',
  'cons':'Not suitable for wet areas|Warp risk if moisture content high|Class C fire rating - lower than gypsum|High cost|Requires periodic retreatment',
  'tooltip_detail':'Timber panel ceiling. Excellent acoustic and thermal performance. Dry areas only. Kiln-dried timber mandatory. Outstanding in living and dining.',
  'status':'Active','verify_flags':'base_cost_per_sqft_inr','data_filled_by':'AI'
},
{
  'component_id':'CEIL-005','category_name':'Finishes','subcategory_name':'Ceiling',
  'name':'metal_tile_grid','display_name':'Metal Tile / Lay-in Grid Ceiling','region':'South India',
  'description':'600x600mm metal or mineral fibre tiles in exposed T-bar aluminium grid. Fully demountable - easy access to services above. Common in commercial and utility spaces. Growing use in residential utility and kitchen areas.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Standard','sort_order':'5',
  'base_cost_per_sqft_inr':'80','installation_cost_per_sqft_inr':'30','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market rate Armstrong/Saint-Gobain mineral fibre tiles + T-grid; South India contractor rate',
  'expected_lifespan_years':'20','replacement_cost_factor':'0.8','major_maintenance_cycle_years':'8',
  'major_maintenance_cost_factor':'0.15','annual_minor_maint_factor':'0.02','maintenance_complexity':'Low',
  'lifecycle_source_notes':'Manufacturer data; IS 14977; BRE Digest 345',
  'thermal_resistance_score':'5','acoustic_score':'8','durability_score':'6','moisture_resistance':'Medium',
  'fire_rating':'Class A','energy_impact_modifier':'1.1','accessibility_score':'10',
  'thermal_source_notes':'Mineral fibre tiles k-value 0.05-0.10 W/m.K. Good insulation. Aluminium grid has negligible thermal bridging. ECBC 2017.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'High-humidity bathrooms without adequate exhaust|Areas prone to water leaks above',
  'compatible_with':'All structural systems',
  'requires_component':'Aluminium main T-bar and cross-T grid|Perimeter angle|600x600 mineral fibre or metal tiles|Hanger wires from slab',
  'climate_restrictions':'In bathrooms use humidity-resistant mineral fibre tiles rated for high moisture. Standard mineral fibre tiles stain and sag from steam.',
  'hard_block_rule':'None',
  'advisory_rule':'Any water leak from slab above will stain and collapse mineral fibre tiles',
  'advisory_message':'Mineral fibre lay-in tiles are highly vulnerable to water damage from above. Waterproof the slab thoroughly before installing. A single roof leak will require tile replacement.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 14977; manufacturer installation guide',
  'ai_advisory_notes':'Metal and mineral fibre grid ceilings are the most practical ceiling choice for kitchens and utility rooms because individual tiles can be lifted out to access electrical connections plumbing valves and AC drain lines above. In a residential kitchen this is enormously useful - when a pipe needs attention or an AC drain clogs you lift two tiles instead of breaking open a plastered ceiling. The acoustic performance of mineral fibre tiles is actually excellent - better than POP or gypsum board - which is a bonus in home offices or study rooms. The commercial look does not suit every room but in a modern kitchen or utility space it is very functional.',
  'pros':'Individual tiles demountable - easy service access above|Excellent acoustic absorption|Fastest installation|Easy partial replacement if damaged',
  'cons':'Commercial appearance - not suitable for all rooms|Mineral fibre tiles stain from water leaks|Cannot integrate smooth curves or coves|Tiles sag in high humidity without HR grade',
  'tooltip_detail':'Modular tile-and-grid ceiling. Best for kitchens and utility areas - lift tiles to access pipes and wiring above. Good acoustic absorption.',
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
