import uuid


class ToDB:

    def sendData(specie, affidabilità, genus, family, commonName):
        #aprire connessione al dB
        #generazione nuovo UUID come visto a lezione
        uuid = uuid.uuid1()
        #invio dati #
        return uuid