from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'devesite.views.home', name='home'),
    # url(r'^devesite/', include('devesite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^$', 'main.views.home'),
     url(r'^lista/', 'main.views.lista'),
     url(r'^admin/', include(admin.site.urls)),
     url(r'^blog/', include('articles.urls')),
)

urlpatterns += staticfiles_urlpatterns()
