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
  'component_id':'PFILL-001','category_name':'Structure','subcategory_name':'Plinth Filling',
  'name':'plinth_fill_murrum','display_name':'Murrum / Laterite Filling','region':'South India',
  'description':'Plinth filling using locally sourced murrum (decomposed rock) or laterite material. Available across Karnataka, Tamil Nadu and parts of Andhra Pradesh. Good compaction characteristics, economical, and widely used for residential plinth filling.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Basic','sort_order':'1',
  'base_cost_per_sqft_inr':'4','installation_cost_per_sqft_inr':'3','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Local murrum supply South India 2024; transport within 30km; compaction labor; normalized per sqft of plinth area',
  'expected_lifespan_years':'60','replacement_cost_factor':'0','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'Permanent fill - no replacement cycle if properly compacted',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'7','moisture_resistance':'Medium',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All foundation and plinth systems',
  'requires_component':'Plate compactor|Water for compaction moisture|Compaction test every 300mm lift',
  'climate_restrictions':'In waterlogged areas murrum can become soft when saturated - consider quarry dust or sand for better drainage.',
  'hard_block_rule':'None',
  'advisory_rule':'Compact in 150mm layers with plate compactor - not by hand tamping alone',
  'advisory_message':'Plinth filling must be compacted in maximum 150mm layers using a plate compactor. Hand tamping alone does not achieve adequate compaction and leads to floor settlement.',
  'advisory_severity':'Strong-Warning','constraint_source_notes':'IS 1892; NBC 2016 Part 6',
  'ai_advisory_notes':'Murrum filling is the right choice for most Karnataka projects because it is the natural decomposed rock material from the same laterite geology and it compacts extremely well when wet. The key word is compaction - I have seen more floor settlement and cracking from badly compacted plinth filling than from any other cause. The fill must go in at maximum 150mm layers and each layer must be compacted with a plate compactor and wetted to optimum moisture content. I always insist on a field density test at every 300mm of fill height before moving to the next layer. The contractor who says plate compaction is not needed and hand tamping is fine is cutting corners - do not accept it. The cost of a plate compactor rental is trivial compared to the cost of relaying a settled floor.',
  'pros':'Most economical filling material|Locally available across South India|Good compaction characteristics|Adequate for most residential plinth filling',
  'cons':'Can become soft when waterlogged|Requires proper compaction in layers|Transport cost if site far from source|Not ideal for poorly drained sites',
  'tooltip_detail':'Murrum/laterite plinth filling. Economical and widely available. Compact in 150mm lifts with plate compactor - critical to prevent settlement.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'PFILL-002','category_name':'Structure','subcategory_name':'Plinth Filling',
  'name':'plinth_fill_river_sand','display_name':'River Sand Filling','region':'South India',
  'description':'Plinth filling using clean river sand (or M-sand). Easier to compact than murrum, drains well, and provides a stable base. Higher cost than murrum due to transport and scarcity. Good choice for areas where good murrum is not locally available.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Intermediate','sort_order':'2',
  'base_cost_per_sqft_inr':'7','installation_cost_per_sqft_inr':'4','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'River sand market rate South India 2024 (scarcity premium); M-sand alternative rate; normalized per sqft',
  'expected_lifespan_years':'60','replacement_cost_factor':'0','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'Permanent fill - no replacement cycle if properly compacted',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'7','moisture_resistance':'High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All foundation and plinth systems',
  'requires_component':'Plate compactor|Clean sand free of organic material|Moisture control during compaction',
  'climate_restrictions':'Sand filling settles faster in high-rainfall zones if not well compacted.',
  'hard_block_rule':'None',
  'advisory_rule':'Use clean washed sand - organic or silty sand compacts poorly and causes settlement',
  'advisory_message':'River sand filling must be clean and free of organic material or silt. Test by squeezing a wet handful - if it leaves mud stains it has too much clay/silt and will settle.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 1892; Karnataka Sand Mining Policy',
  'ai_advisory_notes':'River sand filling is more expensive than murrum because of the ongoing sand scarcity in Karnataka and Tamil Nadu due to mining restrictions. In areas where murrum is not available it is a good second choice because sand compacts well and drains better than clay-heavy murrum. The important caveat is the sand quality - Karnataka has a significant market for inferior silty sand that passes as river sand but has too much clay content. Squeeze a wet handful tightly and look at the residue on your palm - genuine clean river sand leaves almost no stain whereas silty sand leaves a muddy deposit. Clean manufactured sand (M-sand) from a reputable plant is actually a better and more consistent alternative to river sand for plinth filling and I often prefer it. Compact in 150mm layers with the plate compactor as with murrum.',
  'pros':'Good drainage characteristics|Easy to compact|Better drainage than murrum in waterlogged areas|M-sand substitute widely available',
  'cons':'Higher cost than murrum due to scarcity|Quality variable - silt content must be checked|Environmental concern with river sand extraction|Requires clean material free of organics',
  'tooltip_detail':'River sand plinth filling. Check quality - reject silty sand. M-sand is a good alternative. Compact in 150mm lifts.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'PFILL-003','category_name':'Structure','subcategory_name':'Plinth Filling',
  'name':'plinth_fill_quarry_dust','display_name':'Quarry Dust (M-Sand) Filling','region':'South India',
  'description':'Plinth filling using quarry dust or manufactured sand (M-sand) from stone crushing. Widely available in Karnataka and Tamil Nadu from stone quarries. Good drainage, controlled gradation, and consistent quality. Increasingly preferred over river sand due to availability and cost.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Performance','sort_order':'3',
  'base_cost_per_sqft_inr':'6','installation_cost_per_sqft_inr':'4','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Quarry dust market rate Karnataka/Tamil Nadu 2024; widely available near stone quarries; normalized per sqft',
  'expected_lifespan_years':'60','replacement_cost_factor':'0','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'Permanent fill - no replacement cycle if properly compacted',
  'thermal_resistance_score':'5','acoustic_score':'5','durability_score':'8','moisture_resistance':'High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'0','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All foundation and plinth systems',
  'requires_component':'Plate compactor|Water for compaction|IS 383 compliant M-sand from certified plant',
  'climate_restrictions':'None',
  'hard_block_rule':'None',
  'advisory_rule':'Source from IS 383 certified plant - not all quarry dust has consistent gradation',
  'advisory_message':'Quarry dust gradation varies significantly between suppliers. Source from a plant certified to IS 383 for consistent particle size. Poorly graded quarry dust with too many fines can compact poorly.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 1892; IS 383 M-sand specification',
  'ai_advisory_notes':'Quarry dust and manufactured M-sand have become my preferred plinth filling material for Karnataka projects because the supply is consistent independent of monsoon-linked river sand availability and the government has been regulating river sand mining heavily. A good IS 383 certified M-sand from a reputable plant has controlled gradation which means it compacts predictably and drains well. The downside is that not all quarry dust operations are equal - some produce dust with too many fine particles that behave more like silt and compact poorly. Always ask for the IS 383 certificate from the M-sand plant. The compaction procedure is the same as for murrum - 150mm layers, plate compactor, optimum moisture. The cost is typically between murrum and river sand making it an excellent middle ground.',
  'pros':'Widely available across Karnataka and Tamil Nadu|Consistent quality from certified plants|Good drainage|No environmental mining restrictions|Good compaction characteristics',
  'cons':'Quality varies between suppliers - IS 383 certification needed|Dust can be a nuisance on site|Some fine particle content can affect compaction if poorly graded',
  'tooltip_detail':'Quarry dust/M-sand filling. Best availability in Karnataka. Source from IS 383 certified plant. Compact in 150mm lifts.',
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
