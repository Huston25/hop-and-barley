from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path, reverse_lazy

from users.views import UserRegistrationView, UserLoginView, UserLogoutView, AccountView

app_name = 'users'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('account/', AccountView.as_view(), name='account'),
    path('password-reset/', PasswordResetView.as_view(
        template_name='forgot_password.html',
        email_template_name='password_reset_email.html',
        success_url=reverse_lazy('users:password_reset_done')
        ),
         name='forgot_password'
         ),
    path('password-reset/done/', PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'
    ), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html',
        success_url=reverse_lazy('users:password_reset_complete')
    ),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(
             template_name='password_reset_complete.html',

         ), name='password_reset_complete'),

]