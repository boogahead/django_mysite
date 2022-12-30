from django.shortcuts import render,redirect
from .models import Room
from django.http import HttpResponse
from .forms import RoomForm
# Create your views here.
#function / classes deals with what something people will see if they go to certain url

#rooms = [
#    {'id':1,'name':'Lets learn python!'},
#    {'id':2,'name':'Design with me'},
#    {'id':3,'name':'Frontend Developers'},
#]

def home(request):
    rooms=Room.objects.all # give all the rooms in the database
    context={'rooms':rooms} #save the things you want to send in insi de the context variable
    return render(request,'base/home.html',context) #the rooms[] is passed onto the 'home' page.
    #(templates folder inside base folder) base/home.html 
def room(request,pk): #can pass in dynamic value
    room=Room.objects.get(id=pk) # return back one single item id=pk means unique id so it can spew out only one room
    context={'room':room}
    return render(request,'base/room.html',context)

def createRoom(request):
    form=RoomForm()
    if request.method=='POST':
        form=RoomForm(request.POST)# pass all the data to form.
        if form.is_valid():#if valid,
            form.save() #save
            return redirect('home') #redirect user back to the homepage

    context={'form':form} #pass empty dictionary
    return render(request,'base/room_form.html',context)

def updateRoom(request,pk): #passing pk to know what item we are updating
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room) #fill with the room value 

    if request.method=='POST':
        form= RoomForm(request.POST,instance=room) #specifies which room to edit
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context={'form':form} #want to prefill the info
    return render(request,'base/room_form.html',context)

def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room}) # "room" will be specified as obj