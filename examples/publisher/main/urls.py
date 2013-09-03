from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^1/$', 'main.views.home1', name='home1'),
    url(r'^2/$', 'main.views.home2', name='home2'),
    url(r'^3/$', 'main.views.home3', name='home3'),
    url(r'^main/', include('main.urls')),

)
