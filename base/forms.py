from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room,User


class MyUserCreationForm(UserCreationForm):#descend from user creation form
    class Meta:
        model=User
        fields=['name','username','email','password1','password2']
class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields= '__all__' #create a form field based on the class Room in models.py __all__ shows all the fields. Can be filtered to delete certain fields
        exclude=['host','participants']

class UserForm(ModelForm):
    class Meta:
        model=User
        fields = ['avatar','name','username','email','bio']