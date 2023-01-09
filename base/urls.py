#handle all the urls that directs to specific apps
from django.urls import path
from . import views

urlpatterns=[
    
    path('',views.home,name="home"),
    
    path('login/',views.loginPage,name="Login"),
    path('logout/',views.logoutUser,name="logout"),
    path('register/',views.registerPage,name="register"),
    path('room/<str:pk>/',views.room,name="room"),
    # ^  pass the id  now you can write like /room/777(id value)
    path('create-room/',views.createRoom,name="create-room"),
    path('update-room/<str:pk>/',views.updateRoom,name="update-room"),
    path('delete-room/<str:pk>/',views.deleteRoom,name="delete-room"),
    path('delete-message/<str:pk>/',views.deleteMessage,name="delete-message"),
]