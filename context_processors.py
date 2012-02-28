from datetime import datetime
def default(request):
    return {
        'name' : 'Cracket',
        'year' : datetime.today().year
    }