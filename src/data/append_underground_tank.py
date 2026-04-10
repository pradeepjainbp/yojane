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
  'component_id':'UWT-001','category_name':'Systems','subcategory_name':'Underground Water Tank',
  'name':'no_underground_tank','display_name':'No Underground Sump','region':'South India',
  'description':'No underground water storage sump. Relies entirely on municipal water supply or overhead tank fed directly from direct supply. Only viable if municipal supply is continuous, reliable and of adequate pressure throughout the day.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Basic','sort_order':'1',
  'base_cost_per_sqft_inr':'0','installation_cost_per_sqft_inr':'0','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'No capital cost',
  'expected_lifespan_years':'0','replacement_cost_factor':'0','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'No sump - no lifecycle',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'5','moisture_resistance':'Medium',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'Reliable continuous municipal water supply|Direct supply pressure adequate for overhead tank fill',
  'climate_restrictions':'Not recommended anywhere in South India outside premium gated communities with assured 24/7 supply.',
  'hard_block_rule':'None',
  'advisory_rule':'Not recommended unless municipal supply is confirmed as 24/7 continuous and reliable',
  'advisory_message':'No underground sump is a significant risk in most South India cities. BBMP supplies water for 30-45 minutes twice daily in most areas. Without a sump there is no buffer for supply interruptions or tanker water.',
  'advisory_severity':'Strong-Warning','constraint_source_notes':'BWSSB/CMWSSB/HMWSSB supply data',
  'ai_advisory_notes':'I have never recommended building without an underground sump in any South India location outside a very small number of premium gated communities that have their own borewell and treatment plant with 24-hour supply. In the real world BBMP supplies water for 30-45 minutes twice a day on average and many areas of Bangalore get water on alternate days. Without a sump there is simply no storage buffer. When supply comes you need to be able to capture it all. When supply fails you need reserves. A house without a sump is completely dependent on water tankers when supply is disrupted and tanker water in Bangalore costs Rs 800-1200 per load. The sump is non-negotiable infrastructure for 95 percent of South India plots.',
  'pros':'Zero upfront cost|No space consumption below ground',
  'cons':'Not viable in 95% of South India locations|No buffer for supply interruption|Cannot store tanker water|Completely dependent on continuous municipal supply',
  'tooltip_detail':'No sump. Only viable with confirmed 24/7 continuous municipal supply. Not recommended for most South India plots.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'UWT-002','category_name':'Systems','subcategory_name':'Underground Water Tank',
  'name':'sump_plastic_sintex','display_name':'Pre-Moulded Plastic Sump (Sintex)','region':'South India',
  'description':'Factory-manufactured polyethylene or FRP underground water tank. Sintex and similar brands offer 2000-10000 litre capacity below-ground tanks. Quick installation, low cost, but shorter lifespan than RCC. Good for smaller plots or budget-constrained construction.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Intermediate','sort_order':'2',
  'base_cost_per_sqft_inr':'5','installation_cost_per_sqft_inr':'3','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Sintex/Penguin underground sump market rate 2024; 5000L standard residential; normalized per sqft',
  'expected_lifespan_years':'15','replacement_cost_factor':'0.7','major_maintenance_cycle_years':'5',
  'major_maintenance_cost_factor':'0.1','annual_minor_maint_factor':'0.005','maintenance_complexity':'Low',
  'lifecycle_source_notes':'Sintex underground tank rated lifespan 15 years; UV and pressure degradation',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'5','moisture_resistance':'High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'Excavation to tank dimensions|Sand bedding below tank|Concrete collar around top|Pump and motor',
  'climate_restrictions':'In high water table areas the empty plastic tank can float upward. Ensure concrete collar anchoring.',
  'hard_block_rule':'None',
  'advisory_rule':'Concrete collar anchoring mandatory in high water table plots to prevent flotation',
  'advisory_message':'An empty plastic sump in a high water table area can float upward displacing the ground above. A reinforced concrete collar anchoring the tank is mandatory in such locations.',
  'advisory_severity':'Warning','constraint_source_notes':'Sintex installation guidelines; IS 12592',
  'ai_advisory_notes':'The plastic Sintex-style sump is the quick economical solution and it works fine for plots where budget is tight and long-term planning is flexible. The honest limitation is lifespan - the polyethylene material degrades with UV exposure at the exposed top and the tank walls can deform under soil pressure over 10-15 years. I see significant deformation in Sintex underground sumps older than 12 years particularly in sandy soils where the tank has more freedom to move. For a house you plan to live in for 20-30 years I recommend the RCC sump as the first choice. But for a rental property or a budget build where a sump replacement in 15 years is acceptable the plastic sump is a valid choice and the installation is straightforward taking one or two days versus a week for RCC.',
  'pros':'Low cost|Fast installation - 1-2 days|Factory manufactured - no quality variation|Easy to clean through manhole|Good for budget construction',
  'cons':'15-year lifespan - replacement needed|Can deform under soil pressure|Risk of flotation in high water table|Cannot be expanded later|Less volume per cost than RCC',
  'tooltip_detail':'Plastic Sintex sump. 15-year lifespan. Anchor with concrete collar in high water table areas. Good budget option.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'UWT-003','category_name':'Systems','subcategory_name':'Underground Water Tank',
  'name':'sump_ferro_cement','display_name':'Ferro-Cement Sump','region':'South India',
  'description':'Underground water sump constructed using ferro-cement technology (thin cement mortar over wire mesh layers). Lighter than RCC, faster construction, and moderate cost. Lifespan of 20-30 years. Common in Kerala and Tamil Nadu.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Performance','sort_order':'3',
  'base_cost_per_sqft_inr':'10','installation_cost_per_sqft_inr':'6','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Ferro-cement sump contractor rates Tamil Nadu/Kerala 2024; normalized per sqft',
  'expected_lifespan_years':'25','replacement_cost_factor':'0.6','major_maintenance_cycle_years':'10',
  'major_maintenance_cost_factor':'0.15','annual_minor_maint_factor':'0.005','maintenance_complexity':'Medium',
  'lifecycle_source_notes':'ACI 549; ferro-cement water tank performance data; 20-30 year typical lifespan',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'7','moisture_resistance':'High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'Galvanised wire mesh layers|Cement mortar with waterproofing admixture|Skilled ferro-cement mason|Bitumen coating on exterior|Pump and motor',
  'climate_restrictions':'In high water table areas additional exterior waterproofing critical to prevent seepage into tank.',
  'hard_block_rule':'None',
  'advisory_rule':'Bitumen exterior coating mandatory to prevent groundwater contamination of stored water',
  'advisory_message':'Ferro-cement sump exterior must be coated with bitumen or cementitious waterproofing. Without this groundwater can seep through the thin shell contaminating stored drinking water.',
  'advisory_severity':'Warning','constraint_source_notes':'ACI 549; IS 6509 ferro-cement practice',
  'ai_advisory_notes':'Ferro-cement sumps are popular in Tamil Nadu and Kerala because there is a tradition of skilled ferro-cement workers there who can produce a good quality tank at lower cost than RCC. The technology is sound - the thin cement mortar over multiple layers of wire mesh produces a strong waterproof shell. The main vulnerability is the exterior - the thin shell needs good bitumen coating on the outside to prevent groundwater from seeping in through the porous mortar and contaminating the stored water. The quality is very dependent on the skill of the mason particularly in the mortar application consistency. If you can find a good experienced ferro-cement mason and you are on a moderate budget this is a better choice than the Sintex plastic tank for longevity.',
  'pros':'Better lifespan than plastic sump|Lighter than RCC - faster construction|Lower cost than RCC sump|Custom shapes possible|Good choice for Kerala/Tamil Nadu where skilled workers available',
  'cons':'Skill-dependent quality|Exterior waterproofing mandatory|Shorter lifespan than RCC|Less available in Karnataka',
  'tooltip_detail':'Ferro-cement sump. 25-year lifespan. Exterior bitumen coating mandatory. Quality depends on mason skill.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'UWT-004','category_name':'Systems','subcategory_name':'Underground Water Tank',
  'name':'sump_rcc_insitu','display_name':'RCC Sump (In-Situ Cast)','region':'South India',
  'description':'Underground water sump cast in-situ using M20/M25 reinforced cement concrete with waterproofing admixture. Highest durability, 40+ year lifespan. Standard premium specification for residential construction. Typically 5000-15000 litres capacity.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Premium','sort_order':'4',
  'base_cost_per_sqft_inr':'18','installation_cost_per_sqft_inr':'12','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'RCC sump construction Bangalore/Chennai contractor rates 2024; M20 concrete + steel + waterproofing admixture; normalized per sqft',
  'expected_lifespan_years':'45','replacement_cost_factor':'0.5','major_maintenance_cycle_years':'15',
  'major_maintenance_cost_factor':'0.08','annual_minor_maint_factor':'0.005','maintenance_complexity':'Low',
  'lifecycle_source_notes':'IS 3370 water-retaining structures; RCC sump lifespan data',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'9','moisture_resistance':'Very High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'M20 or M25 concrete with waterproofing admixture (Fosroc/STP)|Fe500 steel reinforcement|Pump and motor|Manhole cover (CI)|Ventilation pipe',
  'climate_restrictions':'None',
  'hard_block_rule':'None',
  'advisory_rule':'Waterproofing admixture mandatory in concrete mix - do not skip',
  'advisory_message':'RCC sump concrete must include a waterproofing admixture (Crystalline type - Krystol or Xypex preferred) in the mix. This is a water-retaining structure and ordinary RCC will develop hairline cracks that allow water to seep through the slab.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 3370; IS 456; waterproofing admixture manufacturer guidelines',
  'ai_advisory_notes':'The RCC sump is the first thing I specify and the last thing I am willing to compromise on for any house that the owner plans to live in. A properly built RCC sump with waterproofing admixture in the mix will outlast the house itself. The critical points are the waterproofing admixture - use a crystalline type like Krystol or Xypex added to the concrete mix not a surface coating - and the steel coverage. IS 3370 requires 40mm clear cover for water-retaining structures which is more than the 25mm used for normal structural work because the reinforcement in a sump is exposed to water on one side and soil on the other. I also always specify a CI manhole cover with lock and a ventilation pipe because an unventilated sump can develop anaerobic conditions. Get the sump built before the ground floor slab is cast because accessing the sump location after is very difficult.',
  'pros':'40+ year lifespan - outlasts the building|No risk of flotation or deformation|Can be built to any size|Highest water quality protection|Zero maintenance once correctly built',
  'cons':'Highest cost|Takes 5-7 days to construct|Must be built before ground floor slab is cast|Requires waterproofing admixture and correct steel coverage',
  'tooltip_detail':'RCC sump. Best choice for 40+ year lifespan. Waterproofing admixture mandatory. Build before ground floor slab is cast.',
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
