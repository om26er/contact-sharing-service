from django.conf.urls import url

from rest_framework.authtoken import views

from contact_share_service import views as share_views


urlpatterns = [
    url(r'^api/register$', share_views.UserRegistrationView.as_view()),
    url(r'^api/forgot_password', views.obtain_auth_token),
    url(r'^api/login$', views.obtain_auth_token),
]
