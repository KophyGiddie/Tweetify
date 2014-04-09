from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'tweetify_app.views.index'),
    url(r'^login$', 'tweetify_app.views.login_view'),
    url(r'^logout$', 'tweetify_app.views.logout_view'),
    url(r'^signup$', 'tweetify_app.views.signup'),
    url(r'^settings$', 'tweetify_app.views.settings'),
    url(r'^delete_user$', 'tweetify_app.views.delete_user'),
    url(r'^tweet_submit$', 'tweetify_app.views.tweet_submit'),
    url(r'^user/people$', 'tweetify_app.views.people'),
    url(r'^user/(?P<username>\w+)$', 'tweetify_app.views.user'),
    url(r'^follow/(?P<username>\w+)$', 'tweetify_app.views.follow'),
    url(r'^unfollow/(?P<username>\w+)$', 'tweetify_app.views.unfollow'),
    url(r'^mentions$', 'tweetify_app.views.mentions'),
    url(r'^userlist$', 'tweetify_app.views.userlist'),
    url(r'^admin/', include(admin.site.urls)),
)
