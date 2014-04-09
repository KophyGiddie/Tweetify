from django.shortcuts import render, redirect, render_to_response
from django.shortcuts import Http404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from forms import AuthenticateForm, UserCreateForm, TweetForm
from models import Tweet
from django.template import RequestContext
from models import MyUser
from django.core.exceptions import ObjectDoesNotExist


def index(request):
    # If User is logged in
    if request.user.is_authenticated():
        tweet_form = TweetForm()
        # tweets = Tweet.objects.filter(author=request.user.followed_by.all).order_by('-id')[:10]
        tweets = Tweet.objects.all().order_by('-id')[:10]
        return render(request,
                      'public.html',
                      {'tweet_form': tweet_form,
                       'tweets': tweets})

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
    tweet_form = TweetForm()
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return render(request, 'settings.html', {'form': form,})
    form = UserCreateForm(instance=request.user)
    return render(request, 'settings.html', {'form': form, 'tweet_form': tweet_form})


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
        tweets = Tweet.objects.filter(author=request.user.followed_by.all).order_by('-id')[:10]
        tweet_form = TweetForm(data=request.POST)
        if tweet_form.is_valid():
            tweet = tweet_form.save(commit=False)
            tweet.author = request.user
            tweet.save()
            return redirect('/')
        else:
            return render(request,
                      'public.html',
                      {'tweet_form': tweet_form,
                       'tweets': tweets})
    return redirect('/')   



@login_required
def user(request, username):
        value = False
        user_list = MyUser.objects.all()
        myform = TweetForm()
        try:
            myuser = MyUser.objects.get(username=username)
        except MyUser.DoesNotExist:
            raise Http404
        tweets = Tweet.objects.filter(author=myuser.id).order_by('-id')[:10]
        my_following_list = request.user.follows.all()
        not_following = []
        for i in user_list:
            if (i not in my_following_list):
                not_following.append(i)
        if myuser not in not_following:
            value = True
        return render(request,
                      'profile.html',
                      {'tweet_form': myform, 'myuser': myuser,
                       'tweets': tweets, 'non_follow_list': not_following, 'value': value
                    })

@login_required
def people(request):
    tweet_form = TweetForm()
    user_follows = request.user.follows.all()
    print 'this is for pple %s' % user_follows
    user_followed_by = request.user.followed_by.all()
    return render(request,
                  'people.html',
                  {'tweet_form': tweet_form,
                   'user_follows': user_follows,
                   'user_followed_by': user_followed_by, })

@login_required
def follow(request, username):
    if request.method == "POST":
        try:
            myuser = MyUser.objects.get(username=username)
            request.user.follows.add(myuser)
        except ObjectDoesNotExist:
            return redirect('/user/people')        

    return redirect('/user/people')

@login_required
def unfollow(request, username):
    if request.method == "POST":
        try:
            myuser = MyUser.objects.get(username=username)
            request.user.follows.remove(myuser)
        except ObjectDoesNotExist:
            return redirect('/user/people')        

    return redirect('/user/people')

@login_required
def mentions(request):
        all_tweets = Tweet.objects.all()
        myform = TweetForm()
        mention_tweets = []
        for tweet in all_tweets:
            if (tweet.tweet_text.find(request.user.username) != -1):
                mention_tweets.append(tweet)

        return render(request,
                      'mentions.html',
                      {'tweet_form': myform,
                       'mention_tweets': mention_tweets,
                    })

@login_required
def userlist(request):
    tweet_form = TweetForm()
    user_list = MyUser.objects.all()
    return render(request,
                  'allusers.html',
                  {'tweet_form': tweet_form,
                   'user_list': user_list })