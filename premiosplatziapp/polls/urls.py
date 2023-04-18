from django.urls import path
#import views for current module
from . import views

urlpatterns = [
    path("", views.index, name="index") #route for index
]