#from django.http import JsonResponse #format of how to respond in json
from rest_framework.decorators import api_view  
from rest_framework.response import Response 
from base.models import Room
from .serializers import RoomSerializer

@api_view(['GET']) #http methods that are allowed to access the api
def getRoutes(request):
    routes=[ #e.g. create api that provide all the rooms in the website
        'GET /api',
        'GET /api/rooms', #gives out json obeject of all the rooms 
        'GET /api/rooms/:id' #gives out info about single room 
    ]
    return Response(routes) #safe = we can use more than python dictionary. can be converted into json.

@api_view(['GET'])
def getRooms(request):
    rooms=Room.objects.all()#all the rooms in DB
    serializer=RoomSerializer(rooms,many=True) #pass the object we want to serialize - here, many means whether theres multiple objects we need to serialize, and in this case, it is.
    return Response(serializer.data) #have serializer return the data of serializer

@api_view(['GET'])
def getRoom(request,pk):
    room=Room.objects.get(id=pk)#all the rooms in DB
    serializer=RoomSerializer(room,many=False) #pass the object we want to serialize - here, many means whether theres multiple objects we need to serialize, and in this case, it is not.
    return Response(serializer.data) #have serializer return the data of serializer