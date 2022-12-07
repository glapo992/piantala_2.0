import folium
import pandas as pd


def mappa(filejson):
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
    df = pd.read_json(filejson)
    m = folium.Map(location=[45.645434, 13.849094],
                   zoom_start=17.3,
                   min_zoom=14,
                   height='100%',
                   width='100%',
                   tiles='cartoDB positron')
    # Per ogni osservazione nel set, fa un cerchio e lo aggiunge alla mappa
    for i in range(len(df)):
        folium.Circle(location=[df.iloc[i]['lat'], df.iloc[i]['long']],
                      radius=1,
                      tooltip=[df.iloc[i]['specie']]).add_to(m)

    # Salva la mappa come file html
    return m.save('templates/circle_map.html')
