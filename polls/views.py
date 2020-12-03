  
from django.forms import formset_factory, modelformset_factory
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, CreateView
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
# import requests
# timezone.now
from polls.models import Question, Poll, Answer, QuestionInPoll
from polls.forms import QuestionForm, QuestionEditForm, AnswerForm, QuestionInPollForm

def index(request):
    return render(request, 'index.html')

class QuestionList(ListView):
    model = Question
    # имя переменной, в которой хранится список объектов для отображения
    # по умолчанию object_list
    context_object_name = "questions"
    #queryset = Question.objects.filter(polls__publicationDate__lt(timezone.now)) # отображаем только актуальные опросы
    template_name = "question_user_list.html"

# список постов (для пункта 4)
class PollList(ListView):  
    model = Poll
    context_object_name='poll_list'
    template_name = 'polls.html'

# М2М таблица для редактирования баллов
# class PollEdit(UpdateView):
#     model = QuestionInPoll
#     context_object_name = "question_list"
#     paginate_by = 10
#     template_name = 'poll_questions.html'
#     success_url = 'polls/'
def balls(request, poll_id):
    # print(f'GET balls {poll_id}')
    r_id = request.POST.get('rowid')
    # print(f'rowid {r_id}' )
    # and request.POST['rowid']:
    cur_poll = Poll.objects.get(id=poll_id)
    # print(f'cur_poll {cur_poll.id}' )
    if request.method == 'POST' and request.POST.get('rowid'):
        print('POST')
        print(request.path)
        r_id = request.POST.get('rowid')
        print(f'rowid {r_id}' )
        qp = QuestionInPoll.objects.get(id=request.POST['rowid'])
        qp.score = int(request.POST['score'])
        qp.save()
        kik = request.POST['poll_id']
        print(f'poll_id POST = {kik}')
        # form = QuestionInPollForm(instance=qObj, data = request.POST)
        # if form.is_valid():
        #     form.save()
        # return HttpResponseRedirect(reverse_lazy('poll_questions', kwargs={'poll_id': request.POST['poll_id'], 'poll': cur_poll} ))
        return HttpResponseRedirect(reverse_lazy('poll_questions', kwargs={'poll_id': request.POST['poll_id']} ))
    elif request.method == 'POST':
        print(request.POST['poll_id'])
        pubDate = request.POST.get('publicationDate')
        # print(f'pubDate {pubDate} and typeof {type(pubDate)}')
        
        if pubDate:
            pubDate_converted = datetime.strptime(pubDate, '%Y-%m-%dT%H:%M')
            print(f'pubDate_converted {pubDate_converted} and typeof {type(pubDate_converted)}')
            cur_poll.publicationDate = pubDate_converted

        cur_poll.title = request.POST.get('title')
        cur_poll.description = request.POST.get('description')

        cur_poll.timer = request.POST.get('timer')
        cur_poll.save()
        print(request.POST)
        return HttpResponseRedirect(reverse_lazy('poll_questions', kwargs={'poll_id': request.POST['poll_id'] } ))

    gp_list = QuestionInPoll.objects.filter(poll=cur_poll)
        # form = QuestionInPollForm(instance=g_list)
        # g_list = QuestionInPoll.objects.filter(poll=poll_id)
    # poll_id - ид текущего опроса    
    context = {'gp_list': gp_list, 'poll_id': poll_id, 'poll': cur_poll }
    return render(request, 'poll_questions.html', context)


# D5.7 Формы
def q_form(request):
    form = QuestionForm
    return render(request, 'question_user_edit.html', {'form': form})

class QuestionEditview(UpdateView):
    template_name='question_edit.html'
    model = Question
    form_class = QuestionEditForm
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # context['answers'] = Answer.objects.filter(question=pk_url_kwarg)
        print(context)
        return context

class QuestionCreateView(CreateView):
    template_name = 'question_user_create.html'
    form_class = QuestionForm
    success_url = reverse_lazy('index')

    # формирование словаря параметров для шаблона
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["polls"] = Poll.objects.all()
        context["test_obj"] = "list answer"
        return context

class QuestionManagerList(ListView):
    model = Question
    template_name = 'question_list.html'

def question_edit(request, _id):
    """ редактируем """
    qObj = Question.objects.get(id=_id)
    # fr = book.friend # ссылка на друга по внешнему ключу
    ans_list=Answer.objects.filter(question=_id)
    if request.method != 'POST':
        form = QuestionEditForm(instance=qObj)
    else:
        form = QuestionEditForm(instance=qObj, data = request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    # вывести пустую или недействительную форму
    context = {'qObj': qObj, 'form' : form, 'ans_list' : ans_list}
    return render(request, 'question_edit.html', context)


# extra=4
AnswerFormSet = modelformset_factory(Answer, form=AnswerForm, can_order=True, can_delete=True, extra=4, max_num=4)

# Answer.objects.filter(question=_id)
def question_answer_create(request, _id):
    qObj = Question.objects.get(id=_id)
    answer_list=[ {'ans_id': obj.id ,'question': obj.question, 'textAnswer': obj.textAnswer, 'rightFlg': obj.rightFlg} for obj in Answer.objects.filter(question=_id)]
    if request.method == 'POST':
        answer_formset = AnswerFormSet(request.POST, request.FILES, prefix='answer', queryset=Answer.objects.filter(question=_id))
        # answer_formset = AnswerFormSet(request.POST, request.FILES, prefix='answer')
        # answer_formset = AnswerFormSet(request.POST, request.FILES, prefix='answer', initial= [{'question': _id}, {'question': _id}, {'question': _id}, {'question': _id}])
        form = QuestionEditForm(instance=qObj, data = request.POST)
        if answer_formset.is_valid() and form.is_valid():
            answer_formset.save(commit=False)
            for ans in answer_formset.new_objects:
                print('new objects answer_form', type(ans))
                ans.question = qObj
                # ans['question'] = _id
                print('new objects answer_form',ans)
                ans.save()
            answer_formset.save(commit=True)
            # if form.cleaned_data:
            for answer_form in answer_formset.deleted_objects: #отфильтровать только заполненные формы
                print('deleted_objects objects answer_form', answer_form.id)
                # answer_form.delete()
                # rubric = form.save(coramit=False)
                # rubric.order = form.cleaned_data[ORDERING_FIELD_NAME]
            # for answer_form in answer_formset.changed_objects:
            #     answer_form.save()
            form.save()
            return HttpResponseRedirect(reverse_lazy('q_list'))
        else:
            print('not save')
    else:
        # answerSet=Answer.objects.filter(question=_id)
        # answer_formset = AnswerFormSet(prefix='answer', initial=list(answerSet))
        # answer_list=[ {'question': obj.question, 'textAnswer': obj.textAnswer, 'rightFlg': obj.rightFlg} for obj in Answer.objects.filter(question=_id)]
        # print(answer_list)
        answer_formset = AnswerFormSet(prefix='answer', initial=answer_list)
        # answer_formset = AnswerFormSet(prefix='answer', initial= [{'question': _id}, {'question': _id}, {'question': _id}, {'question': _id}])
        form = QuestionEditForm(instance=qObj)
    return render(request, 'question_answer_create.html', {'qObj': qObj, 'question_form' : form, 'answer_formset': answer_formset})
