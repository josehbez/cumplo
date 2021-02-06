# -*- coding: utf-8 -*-
# Copyright (c) Jose Hbez. All rights reserved.

from django.test import TestCase
from . import libbm

class APITestCase(TestCase):

    def test_udis(self):
        """        
            Valor de UDIS
            https://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?sector=8&accion=consultarCuadro&idCuadro=CP150&locale=es
        """
        serie_id = "SP68257"
        payload = libbm.make_request(serie_id,'2021-01-01','2021-01-01')
        self.assertDictEqual(payload, {serie_id: [{'fecha': '01/01/2021', 'dato': '6.606988'}]})

    def test_dollar(self):
        """
            Tipo de Cambio
            https://www.banxico.org.mx/tipcamb/main.do?page=tip&idioma=sp
        """
        serie_id = "SF43718"
        payload = libbm.make_request(serie_id,'2021-01-04','2021-01-04')
        self.assertDictEqual(payload, {serie_id: [{'fecha': '04/01/2021', 'dato': '19.8457'}]})

    def test_tiie(self):
        """
            Tasas de Interés Interbancarias
            https://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?sector=18&accion=consultarCuadro&idCuadro=CF111&locale=es
        """
        serie_id = [
            "SF331451", #TIIE de Fondeo a Un Día Hábil Bancario, Mediana ponderada por volumen
            "SF43783", #TIIE a 28 días Tasa de interés en por ciento anual
            "SF43878", #Tasas de interés interbancarias Por ciento anual TIIE a 91 días
            "SF111916", #TIIE a 182 días
            "SF43947", #Tasas de interés interbancarias Por ciento anual TIIP a 28 días
        ]
        payload = libbm.make_request(serie_id,'2021-01-04','2021-01-04')
        self.assertDictEqual(payload, {'SF331451': [{'fecha': '04/01/2021', 'dato': '4.30'}], 'SF43783': [{'fecha': '04/01/2021', 'dato': '4.4805'}], 'SF43878': [{'fecha': '04/01/2021', 'dato': '4.4590'}], 'SF111916': None, 'SF43947': None})