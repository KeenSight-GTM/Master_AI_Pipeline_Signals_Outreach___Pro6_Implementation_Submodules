from pathlib import Path
import json,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];D=R/'docs'
mods=json.loads((R/'product-design/module_catalog.json').read_text())['modules']
groups=json.loads((D/'service_groups.json').read_text())
assert sorted(x for v in groups.values() for x in v)==sorted(x['module_id'] for x in mods)
stages=json.loads((D/'stage_cards.json').read_text());assert len(stages)==27 and len({x['step'] for x in stages})==27
index=json.loads((D/'diagram_index.json').read_text())
for item in index['diagrams']:
 path=D/'diagrams'/item['id'];assert path.with_suffix('.mmd').is_file();ET.parse(path.with_suffix('.svg'))
classes=json.loads((D/'class_inventory.json').read_text());assert len(classes)==index['class_count']==119
assert len({c['name'] for c in classes})==119
assert len(mods)==39
bindings=json.loads((R/'protocol/command_bindings.json').read_text());assert len(bindings['commands'])==38
print(json.dumps({'status':'PASS_DESIGN_INVENTORY_NOT_RUNTIME','modules':39,'collector_command_ids':38,'step_cards':27,'record_classes':119,'rendered_views':index['rendered_count'],'service_groups':len(groups)},indent=2))
