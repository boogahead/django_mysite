from django.shortcuts import render

from django.http import HttpResponse
# Create your views here.
#function / classes deals with what something people will see if they go to certain url

rooms = [
    {'id':1,'name':'Lets learn python!'},
    {'id':2,'name':'Design with me'},
    {'id':3,'name':'Frontend Developers'},
]
def home(request):
    context={'rooms':rooms} #save the things you want to send in inside the context variable
    return render(request,'base/home.html',context) #the rooms[] is passed onto the 'home' page.
    #(templates folder inside base folder) base/home.html 
def room(request,pk): #can pass in dynamic value
    room=None
    for i in rooms:
        if i['id']==int(pk):
            room=i
    context={'room':room}
    return render(request,'base/room.html',context)