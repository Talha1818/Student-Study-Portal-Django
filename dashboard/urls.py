from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('notes', views.notes, name='notes'),
    path('deleteNote/<int:pk>', views.deleteNote, name='deleteNote'),
    path('notes_detail/<int:pk>', views.noteDetailsViews.as_view(), name='notes_detail'),
]
