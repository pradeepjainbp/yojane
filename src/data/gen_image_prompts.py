import csv, sys, os
sys.stdout.reconfigure(encoding='utf-8')

with open(os.path.join(os.path.dirname(__file__), 'registry.csv'), encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

CONTEXT = {
    'Foundation Type': 'foundation excavation trench with TMT rebar cage, freshly poured M20 concrete footing',
    'Excavation Depth': 'construction site foundation trench at measured depth, red laterite or black cotton soil exposed',
    'Concrete Mix': 'freshly mixed concrete being poured from transit mixer into formwork, M-grade concrete',
    'Steel Grade': 'TMT steel reinforcement bars bundled or bent into cage, construction site yard',
    'Damp Proof Course': 'damp proof course layer visible between foundation masonry and wall, DPC membrane or mortar band',
    'Soil Treatment': 'anti-termite chemical soil treatment being sprayed under slab, nozzle and chemical pump visible',
    'Plinth Height': 'raised plinth of residential building under construction, brick or concrete plinth above ground level',
    'Plinth Filling': 'plinth fill material being compacted between foundation walls, murrum or quarry dust backfill',
    'Underground Water Tank': 'underground water sump construction, in-situ RCC sump or moulded plastic sump in excavated pit',
    'Structural System': 'structural frame under construction showing columns, beams and slab, building skeleton stage',
    'Wall System': 'wall under construction showing masonry pattern, freshly laid with mortar joints visible',
    'Wall Configuration': 'wall cross-section or cutaway showing single wythe or cavity wall construction detail',
    'Mortar Type': 'mortar mix on trowel, mortar joint between bricks, close-up masonry construction detail',
    'Lintel & Sunshade': 'RCC lintel beam or chajja sunshade above door or window opening in brick wall',
    'Wall Finish': 'freshly plastered wall with smooth finish, plasterer applying material with trowel',
    'Roof Type': 'residential roof structure under construction, South India home roofline',
    'Roofing Material': 'roofing material installation close-up on residential building, South India',
    'Insulation': 'thermal insulation material being installed on roof deck, rolls or rigid boards',
    'Waterproofing': 'waterproofing membrane or coating being applied on flat concrete roof terrace, South India',
    'Parapet': 'parapet wall at roof edge, brick or RCC parapet with plaster finish',
    'Rainwater Harvesting': 'rainwater harvesting system, recharge pit or collection tank under construction, South India plot',
    'Flooring': 'flooring material laid in interior room, close-up of tile or stone finish, South India home',
    'Kitchen Countertop': 'kitchen countertop material installed, modern Indian modular kitchen',
    'Bathroom Fixtures': 'bathroom sanitaryware installed, Indian bathroom interior with natural light',
    'Doors': 'door installed in wall frame, South India home interior, finished room',
    'Windows': 'window installed in wall opening, South India residential building, exterior or interior view',
    'Plumbing': 'plumbing pipes being installed in wall channel, CPVC or PPR pipe with fittings',
    'Electrical': 'electrical conduit and wiring installation in wall, modular switch boxes, under-construction interior',
    'Electrical Load': 'residential electrical distribution board with circuit breakers, neat wiring installation',
    'Electrical Points': 'interior wall with modular electrical outlets and switch plates, finished plastered wall',
    'Solar': 'solar panels or solar water heater mounted on South India residential rooftop, clear sunny day',
    'Water Heating': 'water heater installation, electric geyser or solar heater, bathroom utility area',
    'Rainwater Plumbing': 'PVC drainpipe running along exterior wall from roof to ground, South India building',
    'Waste Management': 'on-site waste management setup, composting bin or biogas unit in residential compound',
    'Inverter / UPS Wiring': 'home inverter and battery backup system mounted on wall, neat wiring, South India home',
    'Compound Wall': 'residential plot compound wall boundary viewed from street, South India',
    'Gate & Entry': 'residential compound gate and entry at driveway, South India home',
    'Driveway Paving': 'driveway paving material close-up, residential entrance driveway South India',
    'Garden Landscape': 'residential garden landscaping in South India home compound, green plants and hardscape',
    'Lighting Strategy': 'interior room with ceiling light fixtures installed, living room South India home',
    'Ceiling': 'interior ceiling detail showing ceiling finish material, South India home interior',
    'Column Grid': 'reinforced concrete columns under construction, grid pattern, under-construction building',
    'Floor System': 'RCC floor slab construction with reinforcement visible before concrete pour',
    'HVAC': 'air conditioning unit or ceiling fan installed in South India residential interior',
    'Glazing': 'architectural glass panel or window glazing installation detail, clear or tinted glass',
    'Green Rating Target': 'green building features, solar panels, vertical garden, sustainable South India home',
    'Senior-Friendly': 'accessible home features, grab bars in bathroom, wide door or entrance ramp, Indian home',
    'High-Seismic': 'dense rebar cage in concrete column or shear wall, seismic-resistant construction detail',
    'Flood-Prone': 'elevated plinth construction with flood vents in base wall, flood-resilient building',
}

DEFAULT_CTX = 'building material or construction component, South India residential construction'

from collections import defaultdict
groups = defaultdict(list)
for r in rows:
    groups[r['subcategory_name']].append(r)

lines = []
lines.append('# Yojane - Image Prompts for Gemini')
lines.append('> Generated 2026-04-10 | 214 components | Paste each prompt into Gemini image generation')
lines.append('> Spec: realistic photo, 1:1 square or 4:3, no text overlay, no watermark, no visible people')
lines.append('')
lines.append('---')
lines.append('')

for sub in sorted(groups.keys()):
    comps = sorted(groups[sub], key=lambda c: int(c['sort_order']) if str(c['sort_order']).isdigit() else 99)
    ctx = CONTEXT.get(sub, DEFAULT_CTX)
    lines.append(f'## {sub}')
    lines.append('')
    for c in comps:
        cid = c['component_id']
        name = c['display_name']
        tier = c['spectrum_position'] or ''
        prompt = (
            f'Professional construction photograph, {name.lower()}, '
            f'{ctx}, '
            f'South India residential site, natural daylight, sharp focus, '
            f'realistic photo, no text, no watermark, no people'
        )
        lines.append(f'### {cid} - {name}  [{tier}]')
        lines.append(f'`{prompt}`')
        lines.append('')
    lines.append('---')
    lines.append('')

out = '\n'.join(lines)
out_path = os.path.join(os.path.dirname(__file__), 'image_prompts.md')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(out)
print(f'Written {len(rows)} prompts to image_prompts.md')
print(f'File size: {len(out)} chars, ~{len(lines)} lines')
