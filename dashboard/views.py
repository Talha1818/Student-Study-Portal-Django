from django.shortcuts import render, redirect
from django.views.generic import DetailView

from .forms import *
from django.contrib import messages
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def home(request):
    return render(request, 'dashboard/home.html')


@login_required
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


@login_required
def deleteNote(request, pk=None):
    Notes.objects.filter(id=pk).delete()
    return redirect('notes')


class noteDetailsViews(DetailView):
    model = Notes


@login_required
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


@login_required
def homeworkDelete(request, pk=None):
    Homework.objects.filter(id=pk).delete()
    return redirect('homework')


@login_required
def homeworkUpdate(request, pk):
    homework = Homework.objects.get(id=pk)
    # print(homework.is_finished)
    if homework.is_finished:
        # print("YES")
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')


@login_required
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
                'form': form,
                'result': result_list
            }
        return render(request, 'dashboard/youtube.html', context)
    else:
        form = DashboardForm()
    context = {
        'form': form
    }
    return render(request, 'dashboard/youtube.html', context)


@login_required
def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todo_ = Todo(user=request.user,
                         title=request.POST['title'],
                         is_finished=finished
                         )
            todo_.save()
        messages.success(request, f'Todo added from {request.user.username} successfully')
    else:
        form = TodoForm()
    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todo_done = True
    else:
        todo_done = False

    context = {
        'form': form,
        'todo': todo,
        'todo_done': todo_done
    }
    return render(request, 'dashboard/todo.html', context=context)


@login_required
def todoUpdate(request, pk):
    todo = Todo.objects.get(id=pk)
    # print(homework.is_finished)
    if todo.is_finished:
        # print("YES")
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect('todo')


@login_required
def todoDelete(request, pk=None):
    Todo.objects.filter(id=pk).delete()
    return redirect('todo')


@login_required
def books(request):
    if request.method == "POST":
        form = BooksForm(request.POST)
        # if form.is_valid():
        text = request.POST['text']
        url = f'https://www.googleapis.com/books/v1/volumes?q={text}'
        get_data = requests.get(url)
        a = get_data.json()
        results = []
        for i in range(10):
            result_dic = {
                'title': a['items'][i]['volumeInfo'].get('title'),
                'subtitle': a['items'][i]['volumeInfo'].get('subtitle'),
                'description': a['items'][i]['volumeInfo'].get('description'),
                'pageCount': a['items'][i]['volumeInfo'].get('pageCount'),
                'categories': a['items'][i]['volumeInfo'].get('categories'),
                'ratingsCount': a['items'][i]['volumeInfo'].get('ratingsCount'),
                'thumbnail': a['items'][i]['volumeInfo']['imageLinks'].get('thumbnail'),
                'previewLink': a['items'][i]['volumeInfo'].get('previewLink'),

            }

            results.append(result_dic)
            context = {
                'form': form,
                'result': results
            }
        return render(request, 'dashboard/books.html', context)
    else:
        form = BooksForm()
    context = {
        'form': form
    }
    return render(request, 'dashboard/books.html', context)


@login_required
def dictionary(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']

        try:
            url = f'https://api.dictionaryapi.dev/api/v2/entries/en_US/{text}'
            get_data = requests.get(url)
            re = get_data.json()
            context = {
                'input': text,
                'form': form,
                'phonetics': re[0]['word'],
                'audio': re[0]['phonetics'][0]['audio'],
                'definition': re[0]['meanings'][0]['definitions'][0]['definition'],
                'synonyms': re[0]['meanings'][0]['definitions'][0]['synonyms']

            }
        except:
            context = {
                'form': form,
                'input': ''
            }
        return render(request, 'dashboard/dictionary.html', context)
    else:
        form = DashboardForm()
        context = {
            'form': form
        }
    return render(request, 'dashboard/dictionary.html', context)


@login_required
def wiki(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        wiki_ = wikipedia.page(text)
        context = {
            'form': form,
            'title': wiki_.original_title,
            'link': wiki_.url,
            'details': wiki_.summary
        }
        return render(request, 'dashboard/wiki.html', context)
    else:
        form = DashboardForm()
        context = {
            'form': form,
            'input': False,
        }
    return render(request, 'dashboard/wiki.html', context)


@login_required
def conversion(request):
    if request.method == 'POST':
        form = ConversionForm(request.POST)
        if request.POST['measurement'] == 'length':
            meas_form = ConversionLengthForm()
            context = {
                'form': form,
                'm_form': meas_form,
                'input': True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) > 0:
                    if first == 'yard' and second == 'foot':
                        answer = f"{input} yard = {int(input) * 3} foot"
                    if first == 'foot' and second == 'yard':
                        answer = f"{input} foot = {int(input) / 3} yard"
                context = {
                    'form': form,
                    'm_form': meas_form,
                    'input': True,
                    'answer': answer
                }
        if request.POST['measurement'] == 'mass':
            meas_form = ConversionMassForm()
            context = {
                'form': form,
                'm_form': meas_form,
                'input': True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) > 0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f"{input} pound = {int(input) * 0.45} kilogram"
                    if first == 'kilogram' and second == 'pound':
                        answer = f"{input} kilogram = {int(input) * 2.2} pound"
                context = {
                    'form': form,
                    'm_form': meas_form,
                    'input': True,
                    'answer': answer
                }

    else:
        form = ConversionForm()
        context = {
            'form': form
        }
    return render(request, 'dashboard/conversion.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"{username} created successfully!")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'dashboard/register.html', context)


@login_required
def profile(request):
    homework = Homework.objects.filter(is_finished=False, user=request.user)
    todos = Todo.objects.filter(is_finished=False, user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    if len(todos) == 0:
        todo_done = True
    else:
        todo_done = False

    context = {
        'homework': homework,
        'todos': todos,
        'homework_done': homework_done,
        'todo_done': todo_done,
    }

    return render(request, 'dashboard/profile.html', context)
