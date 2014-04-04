from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from models import MyUser
from forms import AuthenticateForm, UserCreateForm, TweetForm
from models import Tweet, UserProfile
from django.template import RequestContext

def index(request):
    # If User is logged in
    if request.user.is_authenticated():
        tweet_form = TweetForm()
        tweets = Tweet.objects.order_by('-id')[:10]
        return render(request,
                      'public.html',
                      {'tweet_form': tweet_form, 'next_url': '/tweets',
                       'tweets': tweets, 'username': request.user.username}) 

    # If User is not logged in
    auth_form = AuthenticateForm()
    user_form = UserCreateForm()

    return render(request,
                  'home.html',
                  {'auth_form': auth_form, 'user_form': user_form, })


def login_view(request):
    auth_form = AuthenticateForm()
    user_form = UserCreateForm()
    if request.method == 'POST':
        form = AuthenticateForm(data=request.POST)
        if form.is_valid():
            user = authenticate(email=request.POST['email'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
            else:
                return render_to_response('home.html', {
                'auth_form': form, 'user_form': user_form, 
                }, context_instance=RequestContext(request))

    return render_to_response('home.html', {
        'auth_form': auth_form, 'user_form': user_form, 
    }, context_instance=RequestContext(request))

@login_required
def settings(request):
    return render(request, 'settings.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def delete_user(request):
    if request.method == 'POST':
        newuser = request.user
        newuser.is_active = False
        newuser.save()
        return logout_view(request)
    return settings(request)

def signup(request):
    """
    User registration view.
    """
    auth_form = AuthenticateForm()

    if request.method == 'POST':
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(email=request.POST['email'], password=request.POST['password2'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')

        else:
            return render_to_response('home.html', {
                'auth_form': auth_form, 'user_form': form, 
            }, context_instance=RequestContext(request))

    elif request.method == 'GET':
        form = UserCreateForm()
        return render_to_response('home.html', {
            'auth_form': auth_form, 'user_form': form, 
        }, context_instance=RequestContext(request))

@login_required
def tweet_submit(request):
    if request.method == "POST":
        tweet_form = TweetForm(data=request.POST)
        if tweet_form.is_valid():
            tweet = tweet_form.save(commit=False)
            tweet.author = request.user
            tweet.save()
            return redirect('/')
        else:
            return index(request, tweet_form)
    return redirect('/')   

@login_required
def my_tweets(request):
        myform = TweetForm()
        tweets = Tweet.objects.filter(author=request.user.id)
        return render(request,
                      'my_tweets.html',
                      {'tweet_form': myform, 'user': request.user,
                       'tweets': tweets,
                    })
          