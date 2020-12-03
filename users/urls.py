from users.views import login, logout, register
from django.urls import path  
  
app_name = 'users'  
urlpatterns = [  
	path('login/', login, name='login'),  
	path('logout/', logout, name='logout'),
	path('register/', register, name='register'),
]