from django.conf.urls import *


urlpatterns = patterns(
    url(r'^$', 'main_view', name='app_main'),
    url(r'^sublevel/$', 'sample_view', name='app_sublevel'),
)
