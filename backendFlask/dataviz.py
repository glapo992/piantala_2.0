import folium
import pandas as pd


def mappa(filecsv):
    '''
    Crea la mappa

    Parameters
    ---
    filecsv : str
        Path al csv con i dati

    Returns
    ---
    circle_map.html : file
        File html con la mappa
    '''
    df = pd.read_csv(filecsv)
    m = folium.Map(location=[45.645434, 13.849094],
                   zoom_start=16,
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
