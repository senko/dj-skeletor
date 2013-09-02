from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myapp.views.home', name='home'),
    # url(r'^myapp/', include('myapp.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('apps.users.urls')),

    #Log IN & OUT
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^login/$', 'django.contrib.auth.views.login', name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name="logout"),

    # Password reset
    url(r'^accounts/password_reset/$',
        'django.contrib.auth.views.password_reset',
        name='password_reset_request'
    ),
    (r'^accounts/password_reset/done/$',
        'django.contrib.auth.views.password_reset_done'
    ),
    url(r'^accounts/reset/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        name='password_reset_form'
    ),
    (r'^accounts/reset/done/$',
        'django.contrib.auth.views.password_reset_complete'
    ),

    #Change Password
    url(r'^accounts/change_password/$',
        'django.contrib.auth.views.password_change',
        name='password_change'),
    url(r'^accounts/change_password_done/$',
        'django.contrib.auth.views.password_change_done',
        name='password_change_done'),
)
