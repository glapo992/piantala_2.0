import folium


def mappa(coo_dict:dict)->folium:
    """creates a Folium object located on Area di Ricerca, Basovizza and locates on it the observations in the given dictionary

    :param coo_dict: dict with lat, lon and tooltip to show
    :type coo_dict: dict
    :return: folium map
    :rtype: folium
    """
    m = folium.Map(location=[45.645434, 13.849094],
                   zoom_start=17,
                   min_zoom=14,
                   height='100%',
                   width='100%',
                   tiles='cartoDB positron')
    # Per ogni osservazione nel set, fa un cerchio e lo aggiunge alla mappa
    for key in coo_dict:
        folium.Circle(location=[coo_dict[key]['lat'], coo_dict[key]['long']],
                      radius=3,
                      fill=True,
                      fill_color='blue',
                      color=False,
                      tooltip=[coo_dict[key]['specie_name']]).add_to(m)

    return m


def circleID(tagGPS:list[float], m:folium, tooltip:str)->folium:
    """ adds a poin on the map with a red circle

    :param tagGPS: lat and lon of the point
    :type tagGPS: list[float]
    :param m: folium map where the point is added 
    :type m: folium
    :param specie: tooltip text
    :type specie: str
    :return: folium object with the red circle
    :rtype: folium
    """
    try:
        folium.Circle(
            location=tagGPS,
            radius=3,
            fill=True,
            fill_color='red',
            #color=True,
            color='red',
            tooltip=[tooltip]).add_to(m)
        return m
    except:
        print('dataviz: no GPS tag')
        return m


def mapPlot(m:folium):
    """ Generates the html file to display from folium map  

    :param m: folium obj with the map to display
    :type m: folium
    :return: html template saved in the location
    :rtype: _type_
    """
    # Salva la mappa come file html
    return m.save('app/plantnet/templates/_circle_map.html')
