import folium
import pandas as pd

#temporaneo solo per test
from exifManager import ExifManager as em


class Dataviz:
    '''bisogna passare alla funzione il CSV con coordinate GPS preparato leggendo il DB'''

    def mappa(filecsv):
        df = pd.read_csv(filecsv)
        m = folium.Map(location=[45.645434, 13.849094],
                       zoom_start=16.5,
                       min_zoom=14,
                       height='100%',
                       width='100%',
                       tiles='cartodbdark_matter')
        #'MapQuest Open Aerial'
        # go through each observation in set, make circle, and add to map.
        for i in range(len(df)):
            folium.Circle(
                location=[df.iloc[i]['LATITUDINE'], df.iloc[i]['LONGITUDINE']],
                radius=1,
                tooltip=[df.iloc[i]['SPECIE']]).add_to(m)

        # Same as before, we save it to file
        return m.save('templates/circle_map.html')
