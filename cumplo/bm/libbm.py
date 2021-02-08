# -*- coding: utf-8 -*-
# Copyright (c) 2021 José Hbez. All rights reserved
from django.conf import settings
import requests

# Ref: https://www.banxico.org.mx/SieAPIRest/service/v1/doc/catalogoSeries

#    Valor de UDIS
#    https://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?sector=8&accion=consultarCuadro&idCuadro=CP150&locale=es
SERIE_UDIS = "SP68257"

#    Tipo de Cambio
#    https://www.banxico.org.mx/tipcamb/main.do?page=tip&idioma=sp
SERIE_DOLLAR = "SF43718"

#    Tasas de Interés Interbancarias
#    https://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?sector=18&accion=consultarCuadro&idCuadro=CF111&locale=es
SERIE_TIIE = [
    "SF331451", #TIIE de Fondeo a Un Día Hábil Bancario, Mediana ponderada por volumen
    "SF43783", #TIIE a 28 días Tasa de interés en por ciento anual
    "SF43878", #Tasas de interés interbancarias Por ciento anual TIIE a 91 días
    "SF111916", #TIIE a 182 días
    "SF43947", #Tasas de interés interbancarias Por ciento anual TIIP a 28 días
]

SERIES_ID = [SERIE_DOLLAR, SERIE_UDIS ] +  SERIE_TIIE

def serie_property(serie_id):
    colors=[
        '#4dc9f6',
		'#f67019', #1
		'#f53794',
		'#537bc4',
		'#acc236',
		'#166a8f',
		'#00a950', #6
		'#58595b',
		'#8549ba'
    ]
    sp = {
        SERIE_DOLLAR: { 'label': 'Tipo de Cambio', 'color': colors[0]} ,
        SERIE_UDIS: { 'label': 'Valor de UDIS', 'color': colors[1]} ,

        "SF331451": { 'label': 'TIIE de fondeo a un día 1/', 'color': colors[2]} ,
        "SF43783": { 'label': 'TIIE a 28 días 2/', 'color': colors[3]} ,
        "SF43878": { 'label': 'TIIE a 91 días 2/', 'color': colors[4]} ,
        "SF111916": { 'label': 'TIIE a 182 días 2/', 'color': colors[5]} ,
        "SF43947": { 'label': 'TIIP a 28 días 3/ (Serie histórica)', 'color': colors[6]} ,
    }

    return sp.get(serie_id)

def make_request(serie_id, dt_from, dt_to):
    """
        params:
            serie_id=SP68257 or [SP68257,SP68257]
            dt_from: yyyy-MM-dd
            dt_to: yyyy-MM-dd
        return: dict 
            {
                'SP68257': [
                     {
                        "fecha": "01/02/2020",
                        "dato": "6.441288"
                    },
                ]
            }

    """
    if isinstance(serie_id,list):
        if len(serie_id)==0:
            raise Exception("Sorry, Does not make request, serie_id is a empty list")
        serie_id = ','.join(serie_id)
    if isinstance(serie_id, str):
        if len(serie_id) == 0:
            raise Exception("Sorry, Does not make request, serie_id is empty")
    resp = requests.get(
        "https://www.banxico.org.mx/SieAPIRest/service/v1/series/{}/datos/{}/{}".format(serie_id, dt_from, dt_to),
        headers={
            'Accept': 'application/json',
            'Bmx-Token': settings.BANXICO_TOKEN,
        }
    )
    if resp.status_code != 200:
        raise Exception(resp.text)
    
    payload = resp.json()
    
    series = payload.get('bmx', {}).get('series', [])    
    
    if len(series) == 0:
        raise Exception("Sorry, Not found series request, check SERIE_ID and date FROM,TO. Try again")

    data = {} 
    for sa in serie_id.split(","):
        for sb in series:
            if sb.get('idSerie') == sa:
                data.update({sa: sb.get('datos')})
    
    return data
