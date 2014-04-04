from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'tweetify_app.views.index'), # root
    url(r'^login$', 'tweetify_app.views.login_view'), # login
    url(r'^logout$', 'tweetify_app.views.logout_view'), # logout
    url(r'^signup$', 'tweetify_app.views.signup'), # signup
    url(r'^settings$', 'tweetify_app.views.settings'),
    url(r'^delete_user$', 'tweetify_app.views.delete_user'),
    url(r'^tweet_submit$', 'tweetify_app.views.tweet_submit'),
    url(r'^my_tweets$', 'tweetify_app.views.my_tweets'),    
    url(r'^admin/', include(admin.site.urls)),
)
