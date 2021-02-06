# -*- coding: utf-8 -*-
# Copyright (c) Jose Hbez. All rights reserved.

import requests

# Ref: https://www.banxico.org.mx/SieAPIRest/service/v1/doc/catalogoSeries

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
            'Bmx-Token': '605621c6401fdc5df8f8a4c578d8a8bffc60ed02683824aabe8914f98922d708',
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
