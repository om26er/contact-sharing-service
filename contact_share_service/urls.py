from django.conf.urls import url

from simple_login import views as simple_login_views

from contact_share_service import views as share_views
from contact_share_service.models import User


urlpatterns = [
    url(
        r'^api/register$',
        share_views.UserRegistrationView.as_view()
    ),
    url(
        r'^api/request_activation_key',
        simple_login_views.RequestActivationKey.as_view(user_model=User)
    ),
    url(
        r'^api/activate$',
        simple_login_views.ActivateAccount.as_view(user_model=User)
    ),
    url(
        r'^api/forgot_password',
        simple_login_views.RequestPasswordReset.as_view(
            user_model=User
        )
    ),
    url(
        r'^api/change_password',
        simple_login_views.ChangePassword.as_view(user_model=User)
    ),
    url(
        r'^api/login$',
        simple_login_views.Login.as_view(user_model=User)
    ),
    url(
        r'^api/me',
        share_views.RetrieveUpdateDestroyProfile.as_view()
    ),
    url(
        r'^api/status$',
        simple_login_views.AccountStatus.as_view(user_model=User)
    ),

    url(r'^api/create', share_views.CreateListCard.as_view()),
    url(r'^api/retrieve', share_views.CreateListCard.as_view()),
]
