from django.contrib import admin
from django.contrib.admin.views.main import ChangeList

from polls.models import Poll, Question, Answer, QuestionInPoll, AnswerUser, AnswerPoll

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'publicationDate', 'created_dttm')
    list_display_links = ('id', 'title')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id','text','typeQuestion', 'get_parents')
    autocomplete_fieids = ('polls',)
    list_display_links = ('id', 'text')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):  
    list_display = ('id', 'textAnswer','question')
    list_display_links = ('id', 'textAnswer')

@admin.register(QuestionInPoll)
class QuestionInPollAdmin(admin.ModelAdmin):
    list_display = ('id','question','poll')
    search_fields = ('question',)

@admin.register(AnswerUser)
class AnswerUserAdmin(admin.ModelAdmin):
    list_display = ('id','owner','questionPoll', 'poll')
    search_fields = ('owner',)

@admin.register(AnswerPoll)
class AnswerPollAdmin(admin.ModelAdmin):
    list_display = ('id', 'answer','poll', 'answer')
    search_fields = ('poll',)