import uuid


class ToDB:
    '''accetta 2 liste con tag GPS e ripsposta api
    genera in uuid unico 
    '''

    def sendData(tagGPS, risposta):
        #aprire connessione al dB
        #generazione nuovo UUID come visto a lezione
        uuid = uuid.uuid1()
        #invio dati #
        return uuid


'''
tagGPS[0]=latitudine
tagGPS[0]= longitudine
risposta:
        0=specie
        1=affidabilità risposta
        2=genere
        3=famiglia
        4=nome comune
'''