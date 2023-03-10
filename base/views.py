from django.shortcuts import render,redirect
from .models import Room,Topic,Message
from django.http import HttpResponse
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

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
        username=request.POST.get('username').lower()
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
    #page='register'
    form=UserCreationForm() #create a template user creation form

    if request.method == 'POST': #process form created
        form=UserCreationForm(request.POST)# go through the usercreation form input made by user
        if form.is_valid():#if form valid
            user=form.save(commit=False)  #check whether there are any dirty data (upper case in email for example) so dont commit straightaway
            user.username=user.username.lower() #turn username to lowercase if there are any uppercase
            user.save()
            login(request,user) #log the registered user in 
            return redirect('home')# return to homepage
        else:
            messages.error(request,"An error has Occured during registration!")
        
    return render(request,'base/login_register.html',{'form':form})

def home(request):
    q= request.GET.get('q') if request.GET.get('q')!= None else '' # q is whatever we passed through te url if nothing passed in , just set as empty

    
    rooms=Room.objects.filter(
        Q(topic__name__contains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    ) # give all the rooms in the database 
    #rooms=Room.objects.all()
    topics=Topic.objects.all()
    
    room_count=rooms.count()

    room_messages=Message.objects.filter(Q(room__topic__name__icontains=q)) # can switch to people who follow you etc # added feature to filter activities by room name
                                        # ^ refer to Room class in models.py
    context={'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages} #save the things you want to send in insi de the context variable
    return render(request,'base/home.html',context) #the rooms[] is passed onto the 'home' page.
    #(templates folder inside base folder) base/home.html 

def room(request,pk): #can pass in dynamic value
    room=Room.objects.get(id=pk) # return back one single item id=pk means unique id so it can spew out only one room
    participants=room.participants.all() # query all the participants


    if request.method=='POST':
        message=Message.objects.create( #create message
            user=request.user,
            room=room,
            body=request.POST.get('body')#get body from message
        )
        room.participants.add(request.user) #add participants to the participants tab   
        return redirect('room',pk=room.id) # go back to room with updated message
    room_messages=room.message_set.all() # we can query the children of certian Model. wea re getting all the children(comments) from the model Messages. (its in models.py messages)
    #give us the set of messages related to the specified room

    context={'room':room,'room_messages':room_messages,'participants':participants}
    return render(request,'base/room.html',context)

def userProfile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all() # find all the room that the user is in
    room_message=user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user,'rooms':rooms,'room_message':room_message,'topics':topics}
    return render(request,'base/profile.html',context)

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

@login_required(login_url='Login') #if user is not authenticated, user will be directed to a page to login
def deleteMessage(request,pk):
    message=Message.objects.get(id=pk)
    if request.user!=message.user: #if the creator of the room is not equal to the guy trying to delete it,
        return HttpResponse('you are not allowed here')# say that they are not allowed to do so
    if request.method=='POST':
        message.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':message}) # "room" will be specified as obj