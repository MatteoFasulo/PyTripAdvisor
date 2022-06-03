import json
from db import db_connect
from math import sqrt

import folium
from folium import *
from folium import plugins

from OSMPythonTools.nominatim import Nominatim

def restaurantAddresses():
        conn, cursor = db_connect()
        cursor.execute("SELECT restaurant_name,restaurant_rating,restaurant_total_reviews,restaurant_price,address FROM restaurants")
        rows = cursor.fetchall()
        name,rating,total_reviews,price,address = list(map(list, zip(*rows)))
        conn.commit()
        conn.close()
        return name,rating,total_reviews,price,address

def sqlToGeoJSON():
    name,rating,total_reviews,price,address = restaurantAddresses()
    nominatim = Nominatim()
    results = [nominatim.query(indirizzo).toJSON()[0] if len(nominatim.query(indirizzo).toJSON()) > 0 else None for indirizzo in address]
    #results = list(filter(None, results))

    print(*results, sep="\n")


    with open('points.geojson', 'w', encoding='utf8') as file:
        geojson = {
        "type": "FeatureCollection",
        "features": []
        }

        for index, result in enumerate(results):
            if result is not None:
                json_point = {
                    "type": "Feature",
                    "properties": {
                        "place_id" : result.get('place_id'),
                        "osm_id" : result.get('osm_id'),
                        "name" : name[index],
                        "rating" : rating[index],
                        "total_reviews" : total_reviews[index],
                        "price" : price[index]
                    },
                    "geometry" : {
                        "type" : "Point",
                        "coordinates": [
                            float(result.get('lon')),
                            float(result.get('lat'))
                        ]
                    }
                }
                geojson.get('features').append(json_point)

        json.dump(geojson, file, indent=4)
    
def map_maker(output_filename = 'mappa'):
    m = Map(location=[41.9028, 12.4964], 
                tiles="CartoDB positron", 
                zoom_start=9,
                zoom_control=True, 
                prefer_canvas=True)

    layers = ['Expensive','Reasonable','Cheap']

    fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
    plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:", lng_formatter=fmtr, lat_formatter=fmtr).add_to(m)

    plugins.Geocoder(collapsed=False, position='topright', add_marker=True).add_to(m)

    plugins.Draw(
        export=True,
        filename='my_data.geojson',
        position='topleft',
        draw_options={'polyline': {'allowIntersection': False}},
        edit_options={'poly': {'allowIntersection': False}}
    ).add_to(m)

    fg = FeatureGroup(control=False, show=False)
    m.add_child(fg)

    f1 = plugins.FeatureGroupSubGroup(fg, layers[0].capitalize())
    m.add_child(f1)

    f2 = plugins.FeatureGroupSubGroup(fg, layers[1].capitalize())
    m.add_child(f2)

    f3 = plugins.FeatureGroupSubGroup(fg, layers[2].capitalize())
    m.add_child(f3)

    rating_colors = {
        '1.0' : '#B30000',
        '1.5' : '#B30000',
        '2.0' : '#B30000',
        '2.5' : '#B30000',
        '3.0' : '#B30000',
        '3.5' : '#B30000',
        '4.0' : '#774400',
        '4.5' : '#3C8800',
        '5.0' : '#00CC00',
        }

    with open('points.geojson','r',encoding="utf-8") as file:
        restaurants = json.load(file).get('features')

        for restaurant in restaurants:
            if float(restaurant['properties']['price']) == 1.0:
                Circle(
                    location=(restaurant['geometry']['coordinates'][1],restaurant['geometry']['coordinates'][0]),
                    radius=sqrt(restaurant['properties']['total_reviews']),
                    popup=Popup(
                        IFrame(
f"""<div style="display: flex;height: 165px;justify-content: space-between;flex-direction: column;width: 220px;">
<center><h3 style="font-family:'Raleway',sans-serif;font-size:18px;font-weight:800;">{restaurant['properties']['name']}</h3></center>
<br>
<center>Totale Recensioni: <strong>{restaurant['properties']['total_reviews']}</strong></center>
<br>
<center>&#8364; | &#9733; <strong>{restaurant['properties']['rating']}</strong></center>
</div>""",
width=240,
height=185)),
                    tooltip=restaurant['properties']['name'],
                    color=rating_colors.get(str(restaurant['properties']['rating'])),
                    fill=True,
                    ).add_to(f3)
            elif float(restaurant['properties']['price']) == 2.5:
                Circle(
                    location=(restaurant['geometry']['coordinates'][1],restaurant['geometry']['coordinates'][0]),
                    radius=sqrt(restaurant['properties']['total_reviews']),
                    popup=Popup(
                        IFrame(
f"""<div style="display: flex;height: 165px;justify-content: space-between;flex-direction: column;width: 220px;">
<center><h3 style="font-family:'Raleway',sans-serif;font-size:18px;font-weight:800;">{restaurant['properties']['name']}</h3></center>
<br>
<center>Totale Recensioni: <strong>{restaurant['properties']['total_reviews']}</strong></center>
<br>
<center>&#8364;&#8364; - &#8364;&#8364;&#8364; | &#9733; <strong>{restaurant['properties']['rating']}</strong></center>
</div>""",
width=240,
height=185)),
                    tooltip=restaurant['properties']['name'],
                    color=rating_colors.get(str(restaurant['properties']['rating'])),
                    fill=True,
                    ).add_to(f2)
            elif float(restaurant['properties']['price']) == 4:
                Circle(
                    location=(restaurant['geometry']['coordinates'][1],restaurant['geometry']['coordinates'][0]),
                    radius=sqrt(restaurant['properties']['total_reviews']),
                    popup=Popup(
                        IFrame(
f"""<div style="display: flex;height: 165px;justify-content: space-between;flex-direction: column;width: 220px;">
<center><h3 style="font-family:'Raleway',sans-serif;font-size:18px;font-weight:800;">{restaurant['properties']['name']}</h3></center>
<br>
<center>Totale Recensioni: <strong>{restaurant['properties']['total_reviews']}</strong></center>
<br>
<center>&#8364;&#8364;&#8364;&#8364; | &#9733; <strong>{restaurant['properties']['rating']}</strong></center>
</div>""",
width=240,
height=185)),
                    tooltip=restaurant['properties']['name'],
                    color=rating_colors.get(str(restaurant['properties']['rating'])),
                    fill=True,
                    ).add_to(f1)

    
    plugins.LocateControl().add_to(m)
    plugins.MiniMap(position='bottomright').add_to(m)
    
    
    plugins.Fullscreen(position='topleft', title='Full Screen', title_cancel='Exit Full Screen', force_separate_button=True).add_to(m)
    plugins.MeasureControl(position='bottomleft', primary_length_unit='kilometers', secondary_length_unit='meters').add_to(m)

    TileLayer('Stamen Terrain').add_to(m)
    TileLayer('Stamen Toner').add_to(m)
    TileLayer('Stamen Water Color').add_to(m)
    TileLayer('cartodbpositron').add_to(m)
    TileLayer('cartodbdark_matter').add_to(m)

    LayerControl().add_to(m)
    m.save(f'{output_filename}.html')

if __name__ == '__main__':
    #sqlToGeoJSON()
    #map_maker()
    import pandas as pd
    print(pd.read_csv("test.csv").head())
    #import geopandas as gp
    #df = gp.read_file("points.geojson")
    #municipi = gp.read_file("municipi.geojson")
    #points_within = gp.sjoin(df, municipi, op="within")
    #points_within.to_csv("test.csv")

    #print(df.head())
    
