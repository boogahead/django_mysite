from django.contrib import admin
#admin panel
# Register your models here.

from .models import Room,Topic,Message,User

admin.site.register(User)

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)