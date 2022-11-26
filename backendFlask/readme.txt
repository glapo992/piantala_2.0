ESEMPIO

Contiene una bozza di bakend scritto in flask da buttare su pythonanywhere 


Da quello che ho capito poi più o meno dal main scritto in python si richiamano i vari script che fanno le cose 
Qui lo script richiama una pagina html nella cartella templates (non cambiare nome a questa cartella)

PER IL FORNTEND
fask ha una struttura sua
i file html vanno sempre nella cartella templates
i file statici (css, JS e immagini ) in uan caretlla separata chiamata static
flask interagisce solo con gli html e non con gli altri(per quello sono statici)


NOTA 
ho creato un virtual environment (vFlask) nella cartella con tutte le dependecies
SETUP: 
nel venv sono state settate le variabili d'ambiente: 
    FLASK_APP = app.py      --> dice a flask quale file deve lanciare senza specificare ogni volta il comando completo
    FLASK_ENV = development --> imposta l'ambiente come svilppo lanciando il deugger. permette di aggiornare il server senza riavviarlo ogni volta

Per attivarlo --> . vFlask/bin/activate
Per eseguire --> python3 ./app
Per uscire dal venv --> deactivate

Flask crea un server locale su http://127.0.0.1:5000

per fare le cose fighe con le mappe. basta dargli in pasto un json o un csv
KEPLER --> https://betterprogramming.pub/geo-data-visualization-with-kepler-gl-fbc15debbca4

Flask-WTF ->estensione per la gestione dei form