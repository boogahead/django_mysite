from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields= '__all__' #create a form field based on the class Room in models.py __all__ shows all the fields. Can be filtered to delete certain fields
        exclude=['host','participants']

class UserForm(ModelForm):
    class Meta:
        model=User
        fields = ['username','email']