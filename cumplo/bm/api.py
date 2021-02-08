# -*- coding: utf-8 -*-
# Copyright (c) 2021 José Hbez 

import json
from django.http import JsonResponse, request
from .models import Serie
from .libbm import serie_property, SERIES_ID, SERIE_DOLLAR, make_request, SERIE_UDIS, SERIE_TIIE
from datetime import datetime

class API: 
    
    mfilter = lambda **f: Serie.objects.values_list('date','value').filter(**f).order_by('-date')
    mlabels = lambda o: [ i[0] for i in o]

    @classmethod
    def build_payload(cls, series_id, filter_model=None):
        labels = []
        series = {}
        for serie_id in series_id: 
            if filter_model:
                serie = cls.mfilter(serie=serie_id, **filter_model)
            else:
                serie = cls.mfilter(serie=serie_id)
            series.update({serie_id: serie})
            labels += cls.mlabels(serie)
    
        labels = list(set(labels))        
        labels.sort()
        

        datasets = []
        if len(labels)>0:            
            for serie_id in series_id:
                serie = series.get(serie_id)
                
                data = []
                for label in labels:
                    value = 0
                    for s in serie:                        
                        if label == s[0]: 
                            value = s[1]
                            break
                    data.append(value)
                sp = serie_property(serie_id)
                datasets.append(
                    {
                        'label': sp.get('label'),
                        'backgroundColor': sp.get('color'),
                        'borderColor': sp.get('color'), 
                        'data': data,
                        'fill': False
                    }
                )
                  
        return len(labels) and labels or None,  len(datasets) and datasets or None
        
    payload =  lambda s=None, m =None, p=None: {'success': s or False,'message': m or "Error al obtener los registros",'payload': p or None}

    @classmethod
    def Historical(cls, request):
        labels, datasets = cls.build_payload(SERIES_ID)
        payload = cls.payload()
        if labels and datasets:
            payload = cls.payload(s=True,p={'labels': labels, 'datasets': datasets})
        else:
            payload = cls.payload(m='Warning: No hay registros históricos para gráficar')
        return JsonResponse(payload)
    
    @classmethod
    def make_request_banxico(cls, series_id, request):
        payload = cls.payload()
        try:
            if request.method != 'POST':
                raise Exception("Fatal: Solo peticiones POST permitidas")
            
            data = json.loads(request.body)
            DATE_FORMAT="%Y-%m-%d"
            dt_from = data.get('dt-from') #or datetime.now().strftime(DATE_FORMAT)
            dt_to = data.get('dt-to') #or datetime.now().strftime(DATE_FORMAT)
            if not dt_from or not dt_to:
                raise Exception("Error: Los parametros dt-from:YYYY-mm-dd y dt-to:YYYY-mm-dd son requeridos.")
            
            dt_from = datetime.strptime(dt_from,DATE_FORMAT).strftime(DATE_FORMAT)
            dt_to = datetime.strptime(dt_to,DATE_FORMAT).strftime(DATE_FORMAT)

            if dt_from > dt_to:
                raise Exception("Warning: Fecha de inicio debe ser menor a la final.")
            
            resp = make_request(series_id, dt_from, dt_to)

            if isinstance(series_id, str):
                series_id = [series_id]
        
            for serie_id in series_id:
                series = cls.mfilter(serie=serie_id)                
                rows = resp.get(serie_id)
                if not rows:
                    continue
                for row in rows:
                    rowDate = datetime.strptime(row.get('fecha'), "%d/%m/%Y")
                    rowValue = float(row.get('dato'))
                    try: 
                        rowExist = series.get(date=rowDate.strftime(DATE_FORMAT))                        
                        dateExist = rowExist[0]
                        valueExist = rowExist[1]
                        if valueExist != rowValue:
                            Serie.objects.filter(serie=serie_id,date=dateExist, value=valueExist).update(
                                value=rowValue
                            )                            
                    except Serie.DoesNotExist as e:                        
                        Serie(
                            date=rowDate,
                            value=rowValue,
                            serie=serie_id
                        ).save()            
            labels, datasets = cls.build_payload(series_id=series_id, filter_model={'date__gte':dt_from,'date__lte': dt_to})
            if labels and datasets:
                payload = cls.payload(s=True,p={'labels': labels, 'datasets': datasets})
            else:
                raise Exception("Error: Al obtener los datos de la db para construir la gráfica")
        except Exception as e:
            payload = cls.payload(m=str(e))        
        return JsonResponse(payload)

    @classmethod
    def Dollar(cls, request):
        return cls.make_request_banxico(SERIE_DOLLAR, request)
    
    @classmethod
    def Udis(cls, request):
        return cls.make_request_banxico(SERIE_UDIS, request)
    
    @classmethod
    def Tiie(cls, request):
        return cls.make_request_banxico(SERIE_TIIE, request)