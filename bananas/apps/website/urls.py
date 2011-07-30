# -*- coding: utf-8; mode: django -*-
from django.conf.urls.defaults import patterns, url
from website.views import AvatarView, MarketView

urlpatterns = patterns('website.views',
    url(r'^avatar/(?P<avatar_pk>\d+)/$', AvatarView.as_view(), name='avatar_index'),
    url(r'^market/(?P<avatar_pk>\d+)/(?P<market_pk>\d+)/$', MarketView.as_view(), name='market_index'),
)
