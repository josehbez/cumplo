from django.http import JsonResponse, request
from .models import Serie
from .libbm import serie_property, SERIES_ID


class API: 
    

    mfilter = lambda s: Serie.objects.values_list('date','value').filter(serie=s).order_by('-date')
    mlabels = lambda o: [ i[0] for i in o]

    @classmethod
    def Historical(cls, request):
        labels = []
        series = {}

        for serie_id in SERIES_ID: 
            serie = cls.mfilter(serie_id)
            series.update({serie_id: serie})
            labels += cls.mlabels(serie)
    
        labels = list(set(labels))        
        labels.sort()
        
        payload ={
            'success': False,
            'message': 'Error a obtner la informacion', 
            'payload': None
        }

        if len(labels)>0:
            datasets = []
            for serie_id in SERIES_ID:
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
            payload.update({
             'success': True, 
             'payload': {
                    'labels': labels,
                    'datasets':datasets
                }
            })        

        return JsonResponse(payload)
    