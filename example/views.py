# example/views.py
from datetime import datetime

from django.shortcuts import render

from example.model.model import SalaryPrediciton

model = SalaryPrediciton()

def index(request):
    print(request.method)
    if request.method == 'POST':
        result = {
            "url": request.POST['url'],
            "values": [{
                "key": "date",
                "value": "2021-10-10"
            }, {
                "key": "date",
                "value": "2021-10-10"
            }, {
                "key": "date",
                "value": "2021-10-10"
            }]
        }

        return render(request, 'index.html', {'result': result})
    score = model.predict(result['url'])
    result['score'] = score
    return render(request, 'index.html', { 'result': '' })