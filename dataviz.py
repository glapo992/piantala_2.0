import folium
import pandas as pd


def mappa(filejson):
    '''
    Crea la mappa

    Parameters
    ---
    filejson : str
        Path al json con i dati

    Returns
    ---
    m : folium obj
        Oggetto con la mappa
    '''
    df = pd.read_json(filejson)
    m = folium.Map(location=[45.645434, 13.849094],
                   zoom_start=17,
                   min_zoom=14,
                   height='100%',
                   width='100%',
                   tiles='cartoDB positron')
    # Per ogni osservazione nel set, fa un cerchio e lo aggiunge alla mappa
    for i in range(len(df)):
        folium.Circle(location=[df.iloc[i]['lat'], df.iloc[i]['long']],
                      radius=3,
                      fill=True,
                      fill_color='blue',
                      color=False,
                      tooltip=[df.iloc[i]['specie']]).add_to(m)

    return m


def circleID(tagGPS, m, specie):
    '''
    Accetta la mappa creata sopra e ci aggiunge l'osservazione corrente 
  
    Parameters
    ---
    tagGPS : list
        Lista contenente i dati GPS

    m : str
        Path al json con i dati
    
    specie : str
        Specie della pianta
     
    Returns
    ---
    m : folium obj
        Oggetto con la mappa
    '''
    try:
        folium.Circle(
            location=[tagGPS[0], tagGPS[1]],
            radius=3,
            fill=True,
            fill_color='red',
            #color=True,
            color='red',
            tooltip=[specie]).add_to(m)
        return m
    except:
        return m


def mapPlot(m):
    '''
    Genera il file html contenente la mappa

    Returns
    ---
    circle_map.html : file
        File html con la mappa
    '''
    # Salva la mappa come file html
    return m.save('templates/circle_map.html')
