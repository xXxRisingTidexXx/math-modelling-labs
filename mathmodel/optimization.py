from json import loads, dumps
from typing import Any, Dict
from area import area
from shapely.geometry import shape, mapping


def main():
    whitelist = {'relation/2081686', 'relation/7388499'}
    for layer in ['oblasts', 'rivers']:
        with open(f'layers/{layer}.geojson') as stream:
            content = stream.read()
        collection = loads(content)
        collection['features'] = [
            x
            for x in (
                {**f, 'geometry': optimize(f['geometry'])}
                for f in collection['features']
            )
            if area(x['geometry']) >= 15e6 or x['id'] in whitelist
        ]
        with open(f'layers/{layer}x.geojson', 'w+') as stream:
            stream.write(
                dumps(collection, ensure_ascii=False, sort_keys=False, indent=2)
            )


def optimize(geometry: Dict[str, Any]) -> Dict[str, Any]:
    x = mapping(shape(geometry).simplify(0.008))


if __name__ == '__main__':
    main()
