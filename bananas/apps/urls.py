from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'bananas.views.home', name='home'),
    # url(r'^bananas/', include('bananas.foo.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
