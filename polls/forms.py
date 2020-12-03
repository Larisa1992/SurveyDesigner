from django import forms
from polls.models import Poll, Question, Answer,QuestionInPoll

# редактировать список опросов в модели вопросов
class PollQuestionChangeListForm(forms.ModelForm):
    # here we only need to define the field we want to be editable
    polls = forms.ModelMultipleChoiceField(queryset= Poll.objects.all(), required=False)

# D5.7 Формы
# https://docs.djangoproject.com/en/2.2/ref/forms/widgets/#django.forms.Select
class QuestionForm(forms.ModelForm):  
    # polls = forms.ModelChoiceField(queryset=Poll.objects.all(), label='Опрос', help_text='He забудьте задать опрос!',
    #     widget=forms.widgets.Select(attrs={'size': 8}), empty_label="(Nothing)") 
    # CheckboxSelectMultiple
    # SelectMultiple
    polls = forms.ModelChoiceField(queryset=Poll.objects.all(), label='Опросы', widget=forms.widgets.SelectMultiple, empty_label="(Nothing)") 
    
    class Meta:  
        model = Question  
        fields = '__all__'

class QuestionEditForm(forms.ModelForm):  
    class Meta:  
        model = Question  
        fields = '__all__'

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        # fields = ('textAnswer', 'rightFlg')
        fields = '__all__'

class QuestionInPollForm(forms.ModelForm):
    class Meta:
        model = QuestionInPoll
        fields = ('question', 'score')
        # fields = '__all__'