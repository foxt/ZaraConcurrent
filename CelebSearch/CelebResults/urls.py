from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hackernews.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'CelebResults.views.index'),
    url(r'results/$', 'CelebResults.views.results'),

)