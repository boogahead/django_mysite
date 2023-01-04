from django.shortcuts import render,redirect
from .models import Room,Topic
from django.http import HttpResponse
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
# Create your views here.
#function / classes deals with what something people will see if they go to certain url

#rooms = [
#    {'id':1,'name':'Lets learn python!'},
#    {'id':2,'name':'Design with me'},
#    {'id':3,'name':'Frontend Developers'},
#]

def loginPage(request):
    page='login'
    if request.user.is_authenticated: #if user already logged in, return them to homepage
        return redirect('home')

    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')# receiving data from frontend

        try: #try to query user
            user=User.objects.get(username=username)
        except:
            messages.error(request,'User Does Not Exist')
        user=authenticate(request,username=username,password=password) # if exist, authenticate the user give us an error / give a user that mathches the credentials
        if user is not None : # if we have a user
            login(request,user)# add session to database
            return redirect('home') #send logged in user to home page
        else:
            messages.error(request,'username or password does not exist')

    context={'page':page}
    return render(request,'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    page='register'
    return render(request,'base/login_register.html')

def home(request):
    q= request.GET.get('q') if request.GET.get('q')!= None else '' # q is whatever we passed through te url if nothing passed in , just set as empty

    
    rooms=Room.objects.filter(Q(topic__name__contains=q) |
    Q(name__icontains=q) |
    Q(description__icontains=q)
    ) # give all the rooms in the database 
    #rooms=Room.objects.all()
    topics=Topic.objects.all()
    
    room_count=rooms.count()

    context={'rooms':rooms,'topics':topics,'room_count':room_count} #save the things you want to send in insi de the context variable
    return render(request,'base/home.html',context) #the rooms[] is passed onto the 'home' page.
    #(templates folder inside base folder) base/home.html 
def room(request,pk): #can pass in dynamic value
    room=Room.objects.get(id=pk) # return back one single item id=pk means unique id so it can spew out only one room
    context={'room':room}
    return render(request,'base/room.html',context)

@login_required(login_url='Login') #if user is not authenticated, user will be directed to a page to login
def createRoom(request):
    form=RoomForm()
    if request.method=='POST':
        form=RoomForm(request.POST)# pass all the data to form.
        if form.is_valid():#if valid,
            form.save() #save
            return redirect('home') #redirect user back to the homepage

    context={'form':form} #pass empty dictionary
    return render(request,'base/room_form.html',context)

@login_required(login_url='Login') #if user is not authenticated, user will be directed to a page to login
def updateRoom(request,pk): #passing pk to know what item we are updating
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room) #fill with the room value 

    if request.user!=room.host: #if the creator of the room is not equal to the guy trying to delete it,
        return HttpResponse('you are not allowed here')# say that they are not allowed to do so

    if request.method=='POST':
        form= RoomForm(request.POST,instance=room) #specifies which room to edit
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context={'form':form} #want to prefill the info
    return render(request,'base/room_form.html',context)

@login_required(login_url='Login') #if user is not authenticated, user will be directed to a page to login
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.user!=room.host: #if the creator of the room is not equal to the guy trying to delete it,
        return HttpResponse('you are not allowed here')# say that they are not allowed to do so
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room}) # "room" will be specified as obj