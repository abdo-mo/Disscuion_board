from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Board   
from django.contrib.auth.models import User
from .models import Topic, Post
from .forms import NewTopicForm, PostForm
from django.contrib.auth.decorators import login_required 
from django.db.models import Count 
from django.views.generic import UpdateView, ListView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import requests




#Create your views here.
def home(request):
    boards = Board.objects.all()
    api_url = 'http://api.openweathermap.org./data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q='
    city_name = 'cairo'
    url = api_url + city_name
    response = requests.get(url)
    content = response.json()
    city_weather = {
        'city':city_name,
        'temperature':content['main']['temp'],
        'description':content['weather'][0]['description'],
        'icon':content['weather'][0]['description']
    }
    print('city', city_weather['description'])
    return render(request,'home.html' ,{'boards':boards, 'city_weather':city_weather})



# class HomeListView(ListView):
#     model = Board
#     context_object_name = 'boards'
#     template_name = 'home.html'

    

def board_topics(request, board_id):
    board = get_object_or_404(Board, pk = board_id)
    queryset = board.topics.order_by('-created_date').annotate(comments=Count('posts'))
    page = request.GET.get('page',1)
    paginator = Paginator(queryset,10)
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)
    return render(request, 'topics.html', {'board':board, 'topics':topics})
@login_required
def new_topic(request, board_id):
    board = get_object_or_404(Board, pk = board_id)
    #user = User.objects.first()
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit = False)
            topic.board = board
            topic.created_by = request.user
            topic.save()

            post = Post.objects.create(
                message = form.cleaned_data.get('message'),
                created_by = request.user,
                topic = topic
            )
            return redirect('board_topics', board_id = board.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board':board, 'form':form})

def topic_posts(request, board_id, topic_id):
    topic = get_object_or_404(Topic, board__pk=board_id, pk = topic_id)  
    session_num = 'view_topic_{}'.format(topic.pk)
    if not request.session.get(session_num, False):
        topic.views += 1
        topic.save()
        request.session[session_num] = True
    

    return render(request, 'topic_posts.html', {'topic':topic})
@login_required
def replay_post(request, board_id, topic_id):
    topic = get_object_or_404(Topic, board__pk=board_id, pk = topic_id)
    if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit = False)
                post.topic = topic
                post.created_by = request.user
                post.save()

                topic.updated_by = request.user
                topic.updated_date = timezone.now()
                topic.save()

                return redirect('topic_posts', board_id = board_id, topic_id=topic.pk)
    else:
        form = PostForm()

    return render(request, 'replay_post.html', {'topic':topic, 'form':form})

@method_decorator(login_required, name = 'dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'

    def form_valid(self, form):
        post = form.save(commit = False)
        post.updated_by = self.request.user
        post.updated_date = timezone.now()
        post.save()

        return redirect('topic_posts', board_id = post.topic.board.pk, topic_id = post.topic.pk)

def search_view(request):
    if request.method == "POST":
        searched = request.POST.get('search')
        request.session['search'] = searched
        topics = Topic.objects.filter(subject__icontains=searched)
        return render(request, 'search.html',{'searched':searched, 'topics':topics})
    else:
        searched = request.session['search']
        topics = Topic.objects.filter(subject__icontains=searched)
        return render(request, 'search.html',{'searched':searched, 'topics':topics})
def searchBoard_view(request):
    if request.method == "GET":
        searched = request.session['search']
        boards = Board.objects.filter(name__icontains=searched)
        return render(request, 'board_search.html',{'searched':searched, 'boards':boards})
    else:
        return render(request, 'board_search.html')

def searchUser_view(request):
    if request.method == "GET":
        searched = request.session['search']
        users = User.objects.filter(username__icontains=searched)
        return render(request, 'user_search.html',{'searched':searched, 'users':users})
    else:
        return render(request, 'user_search.html')



class searchUserTopic_view(ListView):
    model = Topic    
    template_name = 'user_search_topic.html'
    context_object_name = 'topics'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        return Topic.objects.filter(created_by = user)
