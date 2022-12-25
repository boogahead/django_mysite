#handle all the urls that directs to specific apps
from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name="home"),
    path('room/<str:pk>/',views.room,name="room"),
    # ^  pass the id  now you can write like /room/777(id value)
]