from users.views import logout, register
from django.contrib.auth import views
from django.urls import path, include, reverse_lazy
  
app_name = 'users'  
urlpatterns = [  
	# path('', include('django.contrib.auth.urls')),/
	# path('login/', login, name='login'),
	path('login/', views.LoginView.as_view(template_name='login.html'), name='login'),
	path('logout/', logout, name='logout'),
	path('register/', register, name='register'),
	path('password_change/', views.PasswordChangeView.as_view(title="Смена пароля", success_url=reverse_lazy('users:password_change_done')), name='password_change'), #страница изменения пароля
	path('password_change/done', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
# success_url=reverse_lazy('users:password_change_done')
	# path('password-reset/', views.PasswordResetView.as_view(success_url=reverse_lazy('users:password_reset_done')), name='password_reset'),
	path('password-reset/', views.PasswordResetView.as_view(success_url=reverse_lazy('users:password_reset_done')), name='password_reset'),
	path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
	path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
	path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]