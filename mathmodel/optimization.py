from json import loads, dumps
from typing import Any, Dict, List
from area import area, ring__area, polygon__area
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
            if area(x['geometry']) >= 1.5e7 or x['id'] in whitelist
        ]
        with open(f'layers/{layer}x.geojson', 'w+') as stream:
            stream.write(
                dumps(
                    collection,
                    ensure_ascii=False,
                    sort_keys=False,
                    indent=2
                )
            )


def optimize(geometry: Dict[str, Any]) -> Dict[str, Any]:
    figure = mapping(shape(geometry).simplify(0.008))
    if figure['type'] == 'Polygon':
        return {**figure, 'coordinates': coalesce(figure['coordinates'])}
    elif figure['type'] == 'MultiPolygon':
        return {
            **figure,
            'coordinates': [
                p
                for p in map(coalesce, figure['coordinates'])
                if polygon__area(p) >= 5e6
            ]
        }
    return figure


def coalesce(coordinates: List[List[List[float]]]) -> List[List[List[float]]]:
    return [
        r
        for i, r in enumerate(coordinates)
        if i == 0 or abs(ring__area(r)) >= 1e6
    ]


if __name__ == '__main__':
    main()
