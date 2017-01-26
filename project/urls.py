from django.conf.urls import include, url

from django.contrib import admin
from django.contrib.auth import views as auth_views
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'myapp.views.home', name='home'),
    # url(r'^myapp/', include('myapp.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('apps.users.urls')),

    #Log IN & OUT
    url(r'^accounts/login/$', auth_views.login),
    url(r'^login/$', auth_views.login, name="login"),
    url(r'^logout/$', auth_views.logout, name="logout"),

    # Password reset
    url(r'^accounts/password_reset/$',
        auth_views.password_reset,
        name='password_reset_request'
    ),
    url(r'^accounts/password_reset/done/$',
        auth_views.password_reset_done,
        name='password_reset_done'
    ),
    url(r'^accounts/reset/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
        auth_views.password_reset_confirm,
        name='password_reset_confirm'
    ),
    url(r'^accounts/reset/done/$',
        auth_views.password_reset_complete,
        name='password_reset_complete'
    ),

    #Change Password
    url(r'^accounts/change_password/$',
        auth_views.password_change,
        name='password_change'),
    url(r'^accounts/change_password_done/$',
        auth_views.password_change_done,
        name='password_change_done'),
]
