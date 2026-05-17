from django.urls import path
from . import views 


urlpatterns = [
    path("signup/",views.RegisterView.as_view()),
    path("login/",views.LoginView.as_view()),
    path("logout/",views.LogoutView.as_view()),
    path("profile/detail/",views.ProfileDetailView.as_view()),
    path("profile/update/",views.ProfileUpdateView.as_view()),
    path("email/update/",views.EmailUpdateView.as_view()),
    path('password/change/',views.PasswordChangeView.as_view())
]
