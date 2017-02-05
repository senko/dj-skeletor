from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register/$', views.register, name='registerUser'),
    url(r'^register/activate/(\w+)/$', views.register_verify,
        name="registerVetify"),
    url(r'^login_check/$', views.login_check, name='loginCheck'),
]
