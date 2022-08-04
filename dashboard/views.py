from django.shortcuts import render, redirect
from django.views.generic import DetailView

from .forms import *
from django.contrib import messages
from youtubesearchpython import VideosSearch


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


def homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            home_ = Homework(user=request.user, subject=request.POST['subject'],
                             title=request.POST['title'],
                             description=request.POST['description'],
                             due=request.POST['due'],
                             is_finished=finished
                             )
            home_.save()
        messages.success(request, f'Homework added from {request.user.username} successfully!')
    else:
        form = HomeworkForm()
    home_ = Homework.objects.filter(user=request.user)
    if len(home_) == 0:
        homework_done = True
    else:
        homework_done = False
    context = {
        'form': form,
        'homework': home_,
        'homework_done': homework_done
    }
    return render(request, 'dashboard/homework.html', context)


def homeworkDelete(request, pk=None):
    Homework.objects.filter(id=pk).delete()
    return redirect('homework')


def homeworkUpdate(request, pk):
    homework = Homework.objects.get(id=pk)
    print(homework.is_finished)
    if homework.is_finished:
        print("YES")
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')


def youtube(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dic = {
                'input': text,
                'title': i['title'],
                'duration': i['duration'],
                'thumbnail': i['thumbnails'][0]['url'],
                'channel': i['channel']['name'],
                'link': i['link'],
                'views': i['viewCount']['short'],
                'published': i['publishedTime'],
            }

            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            # print(desc)
            result_dic['description'] = desc

            result_list.append(result_dic)
            context = {
                'form':form,
                'result': result_list
            }
        return render(request, 'dashboard/youtube.html',context)
    else:
        form = DashboardForm()
    context = {
        'form': form
    }
    return render(request, 'dashboard/youtube.html', context)
