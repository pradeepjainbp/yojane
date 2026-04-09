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

# ── SENIOR-FRIENDLY / ACCESSIBILITY (Special) ──────────────────────────────────
# Aging-in-place and accessibility design levels
# Cost: INR per sqft premium over standard construction
# 4 options: Standard → Basic adaptations → Universal design → Full aging-in-place
new_rows = [
{
  'component_id':'SF-001','category_name':'Special','subcategory_name':'Senior-Friendly',
  'name':'standard_no_adaptations','display_name':'Standard Construction (No Accessibility Features)','region':'South India',
  'description':'Standard residential construction with no specific provisions for elderly or mobility-impaired occupants. Steps at entry, narrow doors, standard bathroom fittings. Suitable for young families with no near-term accessibility requirement.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Baseline','sort_order':'1',
  'base_cost_per_sqft_inr':'0','installation_cost_per_sqft_inr':'0','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'No premium - baseline construction cost.',
  'expected_lifespan_years':'0','replacement_cost_factor':'0','major_maintenance_cycle_years':'0',
  'major_maintenance_cost_factor':'0','annual_minor_maint_factor':'0','maintenance_complexity':'Low',
  'lifecycle_source_notes':'N/A',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'5','moisture_resistance':'High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'1.0','accessibility_score':'3',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'None beyond standard construction',
  'climate_restrictions':'None','hard_block_rule':'None',
  'advisory_rule':'Consider future accessibility needs if any occupant is over 50 or has mobility concerns',
  'advisory_message':'Retrofitting accessibility features (ramps, wide doors, grab bars) after construction is completed costs 5-8x more than incorporating them during construction. If any occupant may need these features in the next 10-15 years, design them in now.',
  'advisory_severity':'Info','constraint_source_notes':'NBC 2016 Part 3 accessibility; IS 16847',
  'ai_advisory_notes':'Standard construction without accessibility features is perfectly appropriate if all occupants are young and healthy and the home will be sold before anyone needs accessibility support. However South India families often have three generations living together and even without elderly parents now the building will be 30-40 years old before it is demolished. I always ask clients to at least design doorways at 900mm clear width (instead of the standard 750mm) and eliminate the threshold step at the main entry - both cost almost nothing during construction but save enormous expense if a wheelchair is ever needed.',
  'pros':'No cost premium|No design constraints|Standard construction skill set',
  'cons':'Retrofit cost is 5-8x build cost for accessibility features|Narrow doors and steps exclude wheelchair users|South India families often have elderly parents moving in',
  'tooltip_detail':'Standard construction. No accessibility features. Retrofitting later costs 5-8x more. At minimum design 900mm doorways and eliminate entry step.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'SF-002','category_name':'Special','subcategory_name':'Senior-Friendly',
  'name':'basic_adaptations','display_name':'Basic Accessibility Adaptations','region':'South India',
  'description':'Minimum practical adaptations: ramped main entry, 900mm clear door widths, grab bar provision in master bathroom, anti-skid flooring in bathrooms, slip-resistant threshold strips at level changes. Cost-effective aging-in-place starter package.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Standard','sort_order':'2',
  'base_cost_per_sqft_inr':'8','installation_cost_per_sqft_inr':'4','cost_confidence':'High',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market rate ramp construction + wider door frames + grab bar installation + anti-skid tiles; normalised per sqft',
  'expected_lifespan_years':'30','replacement_cost_factor':'0.7','major_maintenance_cycle_years':'10',
  'major_maintenance_cost_factor':'0.10','annual_minor_maint_factor':'0.01','maintenance_complexity':'Low',
  'lifecycle_source_notes':'IS 16847; NBC 2016 Part 3',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'8','moisture_resistance':'High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'1.0','accessibility_score':'6',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'Concrete ramp at main entry (1:12 slope max)|900mm clear door frames at bedroom and bathroom|SS grab bar provisions in master bathroom walls (sleeve during construction)|Anti-skid vitrified tiles in bathrooms',
  'climate_restrictions':'None','hard_block_rule':'None',
  'advisory_rule':'Cast grab bar sleeves into bathroom walls during construction - retrofitting into tiled walls is expensive and ugly',
  'advisory_message':'Grab bars for bathrooms must be fixed to structural walls or reinforced backing plates. The sleeve or backing plate must be installed before tiling. Retrofitting grab bars through finished tiles without backing requires breaking tiles - cast the sleeves in now even if grab bars are not installed yet.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 16847; NBC 2016 Part 3 Table 4',
  'ai_advisory_notes':'The basic adaptation package is what I recommend as the minimum for any permanent home in South India because the incremental cost during construction is tiny compared to retrofit cost. The four most important decisions are: ramp at the main entry (slope 1:12 maximum), 900mm clear door width at master bedroom and bathroom, casting grab bar sleeves into the bathroom wall before tiling so they can be installed any time later, and anti-skid tiles in all bathrooms. These four changes cost approximately Rs 50000-80000 on a 1500 sqft house and make it accessible to a wheelchair user or a person with mobility impairment - a meaningful life change that could enable an elderly parent to live independently.',
  'pros':'Low cost premium during construction|Enables wheelchair access to main living areas|Anti-skid tiles prevent bathroom falls - major injury risk in elderly|Grab bar sleeves allow future installation without tile breaking',
  'cons':'Does not address multi-storey accessibility (stairs)|Standard bathroom still not fully wheelchair accessible|No home automation for assisted living',
  'tooltip_detail':'Ramp, 900mm doorways, grab bar sleeves, anti-skid bathrooms. Rs 50-80k on 1500sqft. Low cost now vs very high retrofit cost later.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'SF-003','category_name':'Special','subcategory_name':'Senior-Friendly',
  'name':'universal_design','display_name':'Universal Design (IS 16847 Compliant)','region':'South India',
  'description':'Full universal design compliance per IS 16847 and NBC 2016 Part 3. Includes: zero-threshold entry, 1050mm door widths, turning radius in bathrooms, roll-in shower, lever handles throughout, accessible kitchen counter heights, visual and tactile wayfinding.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Performance','sort_order':'3',
  'base_cost_per_sqft_inr':'25','installation_cost_per_sqft_inr':'10','cost_confidence':'Medium',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market rate full universal design specification; Bangalore/Chennai accessibility consultant rate; normalised per sqft',
  'expected_lifespan_years':'40','replacement_cost_factor':'0.65','major_maintenance_cycle_years':'15',
  'major_maintenance_cost_factor':'0.08','annual_minor_maint_factor':'0.01','maintenance_complexity':'Low',
  'lifecycle_source_notes':'IS 16847; NBC 2016 Part 3; CPWD accessibility guidelines',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'8','moisture_resistance':'High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'1.0','accessibility_score':'9',
  'thermal_source_notes':'No thermal contribution.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'Accessibility consultant review|1050mm clear door frames|1500mm turning circle in bathrooms|Roll-in shower with fold-down seat|Lever handles all doors|Contrasting colour floor-wall junction strips|Accessible kitchen layout',
  'climate_restrictions':'None','hard_block_rule':'None',
  'advisory_rule':'Engage accessibility consultant at schematic design stage - not after plans are drawn',
  'advisory_message':'Universal design compliance affects room dimensions, door widths and bathroom layout in ways that change the floor plan. An accessibility consultant must be involved at schematic design stage before dimensions are committed.',
  'advisory_severity':'Warning','constraint_source_notes':'IS 16847; NBC 2016 Part 3; RPwD Act 2016',
  'ai_advisory_notes':'Universal design is not just about wheelchair access - it benefits everyone. Lever door handles are easier to open with wet hands or full grocery bags. A zero-threshold shower is safer for young children and easier to clean. Wider doorways make moving furniture into the house dramatically easier. The IS 16847 standard provides precise requirements for turning radii, reach zones and visual contrast. The key room affected is the bathroom which needs 1500mm clear turning circle inside and specific fixture positions - this must be planned from the beginning of space planning as it affects the overall bathroom footprint.',
  'pros':'Meets IS 16847 and NBC 2016 standards|Usable by wheelchair users and all mobility levels|Benefits all users daily - lever handles, zero threshold|Property more marketable to wider buyer pool',
  'cons':'Bathroom footprint increases to accommodate turning radius|Higher cost than basic adaptations|Requires accessibility consultant from design stage|Some traditional aesthetics difficult to achieve',
  'tooltip_detail':'Full IS 16847 universal design. 1050mm doors, 1500mm turning circle in bathrooms, roll-in shower, lever handles. Consultant from design stage mandatory.',
  'status':'Active','verify_flags':'None','data_filled_by':'AI'
},
{
  'component_id':'SF-004','category_name':'Special','subcategory_name':'Senior-Friendly',
  'name':'full_aging_in_place','display_name':'Full Aging-in-Place Design','region':'South India',
  'description':'Comprehensive aging-in-place design integrating universal design with home automation, medical alert systems, elevator or lift provision, accessible kitchen and bedroom on ground floor, and smart home monitoring. Designed for lifetime occupancy.',
  'climate_zone':'Warm-Humid|Hot-Dry|Temperate|Composite','spectrum_position':'Premium','sort_order':'4',
  'base_cost_per_sqft_inr':'55','installation_cost_per_sqft_inr':'20','cost_confidence':'Low',
  'cost_last_updated':'2024-Q1','cost_source_notes':'Market estimate including home lift + automation + full universal design; highly variable; [VERIFY]',
  'expected_lifespan_years':'40','replacement_cost_factor':'0.6','major_maintenance_cycle_years':'10',
  'major_maintenance_cost_factor':'0.15','annual_minor_maint_factor':'0.02','maintenance_complexity':'High',
  'lifecycle_source_notes':'IS 16847; NBC 2016 Part 3; home lift standards IS 14665',
  'thermal_resistance_score':'1','acoustic_score':'1','durability_score':'8','moisture_resistance':'High',
  'fire_rating':'Non-Rated','energy_impact_modifier':'1.0','accessibility_score':'10',
  'thermal_source_notes':'No thermal contribution. Smart home automation reduces energy waste.',
  'max_floors_supported':'20','min_floors_required':'1','max_span_supported_m':'N/A',
  'incompatible_with':'None','compatible_with':'All structural systems',
  'requires_component':'Home lift or residential elevator shaft (built in during construction)|Smart home automation|Medical alert panic button system|Ground floor master bedroom with full accessible bathroom|Accessible kitchen with adjustable counters|Home monitoring sensor network',
  'climate_restrictions':'None','hard_block_rule':'None',
  'advisory_rule':'Reserve lift shaft space during construction even if lift is not installed immediately - retrofitting shaft is major structural work',
  'advisory_message':'A residential lift shaft must be built into the structure from the beginning. Retrofitting a lift shaft into an existing multi-storey house requires major structural interventions and is enormously expensive. Build the shaft now; install the lift when needed.',
  'advisory_severity':'Strong-Warning','constraint_source_notes':'IS 14665 lifts; NBC 2016 Part 3; IS 16847',
  'ai_advisory_notes':'Aging-in-place design at this comprehensive level is the right choice for anyone who wants to live in their home for the rest of their life and avoid care home dependency. South India has strong family values around caring for elderly parents at home and this full package makes that practically achievable without physical strain on caregivers. The single most important structural decision is the lift shaft - build it from the beginning even if the lift is not installed for 10-15 years. A 1400mm x 1400mm concrete shaft costs Rs 80000-120000 to build during construction and approximately Rs 8-15 lakhs to retrofit later. The ground floor master bedroom with full accessible bathroom is the practical life-changer - when stairs become difficult the ground floor bedroom allows full independent living.',
  'pros':'Enables full independent living at all ages and mobility levels|Home lift provision for multi-storey without stairs dependence|Smart home monitoring for safety|Ground floor bedroom eliminates stair risk',
  'cons':'Highest cost premium|Home lift shaft must be built from start - cannot retrofit|Requires accessibility consultant and smart home specialist|Over-specified if occupants are young and mobile',
  'tooltip_detail':'Full aging-in-place: lift shaft, ground floor master bedroom, automation, medical alert. Build lift shaft now - retrofitting costs 8-15 lakh extra.',
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
