from django.conf.urls import url

from rest_framework.authtoken import views

from contact_share_service import views as share_views


urlpatterns = [
    url(r'^api/register$', share_views.UserRegistrationView.as_view()),
    url(r'^api/forgot_password', share_views.PasswordResetView.as_view()),
    url(r'^api/change_password', share_views.ChangePasswordView.as_view()),
    url(r'^api/login$', views.obtain_auth_token),
    url(r'^api/create', share_views.CreateCardView.as_view()),
    url(r'^api/retrieve', share_views.RetrieveCardsView.as_view()),
]
