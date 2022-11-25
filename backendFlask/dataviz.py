import folium
import pandas as pd


class Dataviz:
    '''bisogna passare alla funzione il file CSV preparato leggendo il DB'''

    def mappa(filecsv):
        df = pd.read_csv('kc_house_data.csv')
        m = folium.Map(location=[45.645434, 13.849094], zoom_start=16.5)
        # go through each observation in set, make circle, and add to map.
        for i in range(len(df)):
            folium.Circle(
                location=[df.iloc[i]['lat'], df.iloc[i]['long']],
                radius=10,
            ).add_to(m)

        # Same as before, we save it to file
        return m.save('circle_map.html')
