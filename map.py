import folium
import pandas

data = pandas.read_csv('Volcanoes.txt')
lat = list(data['LAT'])
lon = list(data['LON'])
elev = list(data['ELEV'])
name = list(data['NAME'])

# add color range to marker
def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'

html = """<h4>Volcano information:</h4>
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

map = folium.Map(location=(38.58, -99.03), zoom_start=6)

fg_volcanoes = folium.FeatureGroup(name='Volcanoes')



for lt, ln, el, nm in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html=html % (nm, nm, el), width=200, height=100)
    # using the conventional marker
    # fg.add_child(folium.Marker(location=(lt, ln), popup=folium.Popup(iframe), icon=folium.Icon(color=color_producer(el))))

    #using a circle marker
    folium.CircleMarker(location=(lt, ln), radius=6, popup=folium.Popup(iframe), 
    fill_color=color_producer(el), color='grey', fill_opacity=0.7).add_to(fg_volcanoes)

fg_populations = folium.FeatureGroup(name='Populations')
# adding a polygon layer for population
folium.GeoJson(
   data=open('world.json', 'r', encoding='UTF-8-sig').read(),
   style_function= lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000 else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}
).add_to(fg_populations)

map.add_child(fg_volcanoes)
map.add_child(fg_populations)
map.add_child(folium.LayerControl())

map.save('Map.html')
