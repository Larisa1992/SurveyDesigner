"""SurveyDesigner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from polls import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('user/', include('users.urls', namespace='users')),
    path('questions/', views.QuestionList.as_view(), name='questions'), # доступные опросы для авторизованного пользователя
    path('q_form/', views.q_form, name='q_form'), # форма на основе классов форм
    path('q_create/', views.QuestionCreateView.as_view(), name='q_create'), # форма на основе классов форм
    # path('q_edit/', question_edit, name='q_edit'), # форма на основе классов форм
    path('q_edit/<int:_id>/', views.question_edit, name='question_edit'), # форма редактирования вопроса
    path('q_update/<int:_id>/', views.QuestionEditview.as_view(), name='q_update'), # форма редактирования вопроса с ответами
    path('q_list/', views.QuestionManagerList.as_view(), name='q_list'), # список всех вопросов с переходом для редактирования
    path('question_manage/<int:_id>/', views.question_answer_create, name='question_answer_create'),
    path('polls/', views.PollList.as_view(), name='poll_list'),
    path('balls/<int:poll_id>/', views.balls, name='poll_questions'), #пункт 4 - баллы за вопрос
    path('polls/<int:poll_id>/', views.poll_start, name='poll_start'), # Опрос со списком опросов для пользователя
    path('statistics/', views.AnswerUserListView.as_view(), name='statistics'), # Опрос со списком опросов для пользователя
    # path('user/statistics/', views.UserStatistics.as_view(), name='user_statistics'), # Опрос со списком опросов для пользователя
    path('user/statistics/', views.user_start, name='user_statistics'), # Опрос со списком опросов для пользователя
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)