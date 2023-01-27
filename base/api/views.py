from django.http import JsonResponse #format of how to respond in json

def getRoutes(request):
    routes=[ #e.g. create api that provide all the rooms in the website
        'GET /api',
        'GET /api/rooms', #gives out json obeject of all the rooms 
        'GET /api/rooms/:id' #gives out info about single room 
    ]
    return JsonResponse(routes,safe=False) #safe = we can use more than python dictionary. can be converted into json.