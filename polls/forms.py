from django import forms
from django.forms import SplitDateTimeWidget, SelectDateWidget

from polls.models import Poll, Question, Answer, QuestionInPoll, AnswerUser, AnswerPoll


class PollForm(forms.ModelForm):
    publicationDate = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M'], widget=forms.DateTimeInput)
    class Meta:  
        model = Poll  
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'width': '10'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'row': '4'}),
        }

# class QuestionForm(forms.ModelForm):   
#     class Meta:  
#         model = Question  
#         fields = '__all__'
#         widgets = {
#         'text': forms.TextInput(attrs={'class':'form-control'}),
#         'polls': forms.CheckboxSelectMultiple(attrs={'queryset':Poll.objects.all()})}

class QuestionEditForm(forms.ModelForm):  
    class Meta:  
        model = Question  
        fields = '__all__'
        widgets = {
            'text': forms.TextInput(attrs={'class':'form-control', 'width': '10'}),
            'polls': forms.CheckboxSelectMultiple(attrs={'queryset':Poll.objects.all()}),
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('textAnswer',)

# class QuestionInPollForm(forms.ModelForm):
#     class Meta:
#         model = QuestionInPoll
#         fields = ('question', 'score')

class AnswerUserForm(forms.ModelForm):
    class Meta:
        model = AnswerUser
        fields = '__all__'

class AnswerPollForm(forms.ModelForm):
    class Meta:
        model = AnswerPoll
        fields = '__all__'