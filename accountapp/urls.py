from django.urls import path, reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from accountapp import views
from accountapp.token import AccountAppToken

app_name = 'accountapp'
urlpatterns = [
    path('', views.home, name='home'),
    path('faith', views.faith, name='faith'),
    path('announcement', views.announcement, name='announcement'),
    path('ministry', views.children_ministry, name='ministry'),
    path('calendar', views.calendar, name='calendar'),
    path('signup', views.signup, name='signup'),
    path('signup_activate', views.signup_activate, name='signup_activate'),
    path('login', views.login, name='login'),
    path('profile', views.profile, name='profile'),
    path('sentMessage', views.sentMessage, name='sentMessage'),
    path('logout', views.logout, name='logout'),
    path('activate_account/<uid>/<token>', views.activate_account, name='activate_account'),
    path('forget_password', views.forget_password, name='forget_password'),
    path('change_password', PasswordChangeView.as_view(template_name='reset_password.html',
                                                       success_url=reverse_lazy('accountapp:change_password_done')), name='change_password'),
    path('change_password_done', views.change_password_done, name='change_password_done'),
    path('reset_password/<uidb64>/<token>', PasswordResetConfirmView.as_view(template_name='reset_password.html',
                                                                             success_url=reverse_lazy('accountapp:reset_password_done'),
                                                                             token_generator=AccountAppToken()), name='reset_password'),
    path('reset_password_done', views.change_password_done, name='reset_password_done'),
]
