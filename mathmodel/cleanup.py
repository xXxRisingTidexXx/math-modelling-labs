from json import loads, dumps
from area import area

with open('layers/rivers.geojson') as stream:
    content = stream.read()
collection = loads(content)
collection['features'] = [f for f in collection['features'] if area(f['geometry']) >= 1e6]
with open('layers/riversx.geojson', 'w+') as stream:
    stream.write(dumps(collection, ensure_ascii=False, sort_keys=False, indent=2))
