import json
import csv

file = open(r'Data/bases.json', encoding='utf-8')
data = json.load(file)

features = data['9']

with open('bases.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'map_id', 'layer_id', 'icon_id', 'lat', 'lng', 'title', 'description'])

    for feature in features:
        ID = feature['id']
        map_id = feature['map_id']
        layer_id = feature['layer_id']
        icon_id = feature['icon_id']
        lat = feature['lat']
        lng = feature['lng']
        title = feature['title']
        desc = feature['description']
        writer.writerow([ID, map_id, layer_id, icon_id, lat, lng, title, desc])
