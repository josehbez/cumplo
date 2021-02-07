# -*- coding: utf-8 -*-
# Copyright (c) Jose Hbez. All rights reserved.

from django.test import TestCase
from . import libbm

class APITestCase(TestCase):

    def test_udis(self):
        serie_id = libbm.SERIE_UDIS
        payload = libbm.make_request(serie_id,'2021-01-01','2021-01-01')
        self.assertDictEqual(payload, {serie_id: [{'fecha': '01/01/2021', 'dato': '6.606988'}]})

    def test_dollar(self):
        serie_id = libbm.SERIE_DOLLAR
        payload = libbm.make_request(serie_id,'2021-01-04','2021-01-04')
        self.assertDictEqual(payload, {serie_id: [{'fecha': '04/01/2021', 'dato': '19.8457'}]})

    def test_tiie(self):
        serie_id = libbm.SERIE_TIIE
        payload = libbm.make_request(serie_id,'2021-01-04','2021-01-04')
        self.assertDictEqual(payload, {'SF331451': [{'fecha': '04/01/2021', 'dato': '4.30'}], 'SF43783': [{'fecha': '04/01/2021', 'dato': '4.4805'}], 'SF43878': [{'fecha': '04/01/2021', 'dato': '4.4590'}], 'SF111916': None, 'SF43947': None})