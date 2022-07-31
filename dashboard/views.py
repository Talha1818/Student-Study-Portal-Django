from django.shortcuts import render, redirect
from django.views.generic import DetailView

from .forms import *
from django.contrib import messages


# Create your views here.
def home(request):
    return render(request, 'dashboard/home.html')


def notes(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            notes_ = Notes(user=request.user, title=request.POST['title'],
                           description=request.POST['description'])
            notes_.save()
        messages.success(request, f'Notes added from {request.user.username} successfully!')
    else:
        form = NotesForm()
    notes_data = Notes.objects.filter(user=request.user)
    context = {'notes': notes_data, 'form': form}
    return render(request, 'dashboard/notes.html', context=context)


def deleteNote(request, pk=None):
    Notes.objects.filter(id=pk).delete()
    return redirect('notes')


class noteDetailsViews(DetailView):
    model = Notes
