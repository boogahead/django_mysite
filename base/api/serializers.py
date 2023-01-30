#take certain python object and change into a json object to return

from rest_framework.serializers import ModelSerializer
from base.models import Room

class RoomSerializer(ModelSerializer):
    class Meta:
        model =Room
        fields='__all__' #go to models.py, go to class Rooms, and serialize everything inside.
