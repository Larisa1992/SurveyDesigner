from django.contrib import admin
from django.contrib.admin.views.main import ChangeList

from polls.models import Poll, Question, Answer, QuestionInPoll
from polls.forms import PollQuestionChangeListForm

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    pass

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text','typeQuestion', 'get_parents')
    autocomplete_fieids = ('polls',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass

@admin.register(QuestionInPoll)
class QuestionInPollAdmin(admin.ModelAdmin):
    pass

# class QuestionChangeList(ChangeList):
#     def __init__(self, request, model, list_display,
#         list_display_links, list_filter, date_hierarchy,
#         search_fields, list_select_related, list_per_page,
#         list_max_show_all, list_editable, model_admin):
#         super(QuestionChangeList, self).__init__(request, model,
#         list_display, list_display_links, list_filter,
#         date_hierarchy, search_fields, list_select_related,
#         list_per_page, list_max_show_all, list_editable, model_admin)
        
#          # these need to be defined here, and not in MovieAdmin
#         self.list_display = ['text', 'typeQuestion', 'polls']
#         self.list_display_links = ['text']
#         self.list_editable = ['polls']

# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):

#     def get_changelist(self, request, **kwargs):
#         return QuestionChangeList

#     def get_changelist_form(self, request, **kwargs):
#         return PollQuestionChangeListForm