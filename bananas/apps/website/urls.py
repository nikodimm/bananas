# -*- coding: utf-8; mode: django -*-
from django.conf.urls.defaults import patterns, url
from website.views import AvatarView, MarketView, VacancyListView, CompanyView

urlpatterns = patterns('website.views',
    url(r'^avatar/(?P<avatar_pk>\d+)/$', AvatarView.as_view(), name='avatar_index'),
    url(r'^vacancy/(?P<avatar_pk>\d+)/$', VacancyListView.as_view(), name='vacancy_index'),
    url(r'^market/(?P<avatar_pk>\d+)/(?P<market_pk>\d+)/$', MarketView.as_view(), name='market_index'),
    url(r'^company/(?P<avatar_pk>\d+)/(?P<company_pk>\d+)/$', CompanyView.as_view(), name='company_index'),
)
