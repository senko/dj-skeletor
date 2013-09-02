from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^register/$', 'apps.users.views.register', name='registerUser'),
    url(r'^register/activate/(\w+)/$', 'apps.users.views.register_verify',
        name="registerVetify"),
    url(r'^login_check/$', 'apps.users.views.login_check', name='loginCheck'),
)
