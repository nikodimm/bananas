# -*- coding: utf-8; mode: django -*-
from django.conf.urls.defaults import patterns, url
from website.views import AvatarView

urlpatterns = patterns('website.views',
    url(r'^avatar/(?P<pk>\d+)/$', AvatarView.as_view(), name='avatar_index'),
)
