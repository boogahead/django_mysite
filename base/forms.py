from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields= '__all__' #create a form field based on the class Room in models.py __all__ shows all the fields. Can be filtered to delete certain fields
        