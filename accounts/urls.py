from django.conf.urls import url
from . import views
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView, LogoutView
from django.urls import path

app_name = "accounts"

urlpatterns = [
    path('logout/', LogoutView.as_view(template_name='accounts/logout.html'), name="logout"),
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name="user_login"),

    path('password_reset/', PasswordResetView.as_view(template_name='accounts/reset_password.html',
                                                      success_url='accounts/password_reset_done',
                                                      email_template_name='frontend/reset_password_email.html'),
         name='reset_password'),
    path('password_done/', PasswordResetDoneView.as_view(template_name='accounts/reset_password_done.html', ),
         name='password_reset_done'),
    path('reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/',
         PasswordResetConfirmView.as_view(template_name='accounts/reset_password_confirm.html'),
         name='password_reset_confirm'),

    path('reset-password/complete/',
         PasswordResetCompleteView.as_view(template_name='accounts/reset_password_complete.html'),
         name='password_reset_complete'),

    path('view_profile/', views.view_profile, name='view_profile'),
    path('status_edit/', views.status_edit, name='status_edit'),
    path('my_requests/', views.my_requests, name='my_requests'),

    # path('home/', views.view_profile, name='home'),
    path('view_profile/(?P<pk>[0-9]+)/$', views.view_profile, name='view_profile'),
    path('edit_profile/', views.user_edit, name='user_edit'),
    path('change_password/', views.change_password, name='change_password'),
    path('all_requests/', views.all_requests, name='all_requests'),

]
