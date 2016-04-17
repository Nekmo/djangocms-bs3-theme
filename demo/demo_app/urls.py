from django.conf.urls import *

from demo.demo_app.views import ChangeThemeOptionsView

urlpatterns = patterns('',
    url(r'^$', ChangeThemeOptionsView.as_view(), name='change_theme_options'),
    # url(r'^sublevel/$', 'sample_view', name='app_sublevel'),
)
