from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Topic(models.Model):
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name

#inherit from models
class Room(models.Model):
    host = models.ForeignKey(User,on_delete=models.SET_NULL,null=True) # make sure that this CAN be null
    topic = models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True) # make sure that this CAN be null
    name = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)  #database can be blank with null=true blank= true : can be left blank 
    participants = models.ManyToManyField(User,related_name='participants',blank=True)  #store all users currently active in the room
    
    updated= models.DateTimeField(auto_now=True)   # any time we run the save method, it saves timestamps
    created=models.DateTimeField(auto_now_add=True) # auto_now = take snapshot any time _now_add = only saved when created
    
    class Meta:
        ordering=['-updated','-created'] # most recently updated item first by adding -
    def __str__(self) :
        #return super().__str__()
        return self.name


class Message(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE) #user can have many messages , message can have only one user
    room=models.ForeignKey(Room, on_delete=models.CASCADE) #many to one relationship   -- when parent deleted, delete all messages in the room
    body = models.TextField() 
    updated= models.DateTimeField(auto_now=True)   # any time we run the save method, it saves timestamps
    created=models.DateTimeField(auto_now_add=True) # auto_now = take snapshot any time _now_add = only saved when created
    def __str__(self) :
        return self.body[0:50] # only return first 50 characters