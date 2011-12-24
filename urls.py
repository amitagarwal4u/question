from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^contact/$', 'question.contacts.views.contact'),
    (r'^comment/thankyou/', 'comment.views.thankyou'),
    (r'^comment/', 'comment.views.contactview'),
    url(r"^aiteo/", include("aiteo.urls")),
    url(r'^admin/', include(admin.site.urls)),
    # Example:
    # (r'^question/', include('question.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
