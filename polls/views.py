  
from django.forms import formset_factory, modelformset_factory
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, CreateView
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F, Count, Sum, Value, IntegerField, CharField
from django.db.models.functions import Coalesce
from django.template import loader

from datetime import datetime
# import requests
# timezone.now
from polls.models import Question, Poll, Answer, QuestionInPoll, AnswerUser, AnswerPoll
from polls.forms import QuestionForm, QuestionEditForm, AnswerForm, QuestionInPollForm, AnswerUserForm, PollForm, AnswerPollForm

def index(request):
    return render(request, 'index.html')

class PollAdminCreate(CreateView):  
    model = Poll  
    form_class = PollForm  
    success_url = reverse_lazy('admin_poll_list')  
    template_name = 'poll_create.html' 

class PollAdminList(ListView):  
    """ Список опросов для админа """
    model = Poll
    queryset = Poll.objects.all()
    context_object_name='poll_list'
    template_name = 'polls.html'

class PollList(ListView):  
    model = Poll
    # queryset = Poll.objects.filter(publicationDate__gte=timezone.now())
    context_object_name='poll_list'
    template_name = 'polls.html'

    def get_queryset(self):
        return Poll.objects.filter(publicationDate__gt=timezone.now())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print('username', self.request.user.username)
        # polls_status = QuestionInPoll.objects.filter(answeruser__owner=self.request.user).values('poll', 'poll__title').annotate(count_answ=Count('answeruser'))
        # context["status"] = QuestionInPoll.objects.filter(answeruser__owner=self.request.user).annotate(count_answ=Count('answeruser'))
        polls_status = AnswerUser.objects.filter(owner=self.request.user).values('poll', 'poll__title').annotate(count_answ=Count('answer'))
        context["polls_old"] = Poll.objects.filter(publicationDate__lt=timezone.now())
        context["polls_status"] = polls_status
        # print(context["polls_old"])
        return context

# @login_required
class QuestionList(ListView):
    model = Question
    # имя переменной, в которой хранится список объектов для отображения
    # по умолчанию object_list
    context_object_name = "questions"
    #queryset = Question.objects.filter(polls__publicationDate__lt(timezone.now)) # отображаем только актуальные опросы
    template_name = "question_user_list.html"

class QuestionCreateView(CreateView):
    template_name = 'question_create.html'
    form_class = QuestionForm
    success_url = reverse_lazy('index')

    # формирование словаря параметров для шаблона
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["polls"] = Poll.objects.all()
        return context

 # ответы всех пользователей       
# @login_required
class AnswerUserListView(ListView):
    model = AnswerUser
    form_class = AnswerUserForm
    success_url = reverse_lazy('polls')  
    template_name = 'statistics_all.html'

# user/statistics
class UserStatistics(ListView):
    model = AnswerUser
    # form_class = AnswerUserForm
    template_name = 'statistics_user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["status"] = AnswerUser.objects.filter(Q(owner=self.request.user) & Q(questionPoll__poll=self.kwargs['pk'])).exists()
        # AnswerUser.objects.filter(Q(owner=self.request.user))
        
        # QuestionInPoll.objects.filter(questionPoll_set.owner=self.request.user).annotate(count_answ = Count('questionPoll_set'))
        # context["status"] = AnswerUser.objects.filter(Q(owner=self.request.user))
        
        # user_score_2 - опрос, к-во пользователей его прошедших
        user_score = AnswerUser.objects.values('owner', 'questionPoll__poll').annotate(sum_score=Sum('score'))

        user_score_2 = user_score.values('questionPoll__poll').annotate(count_user=Count('owner', distinct=True))

        # можно одним запросом
        user_score_3 = AnswerUser.objects.values('owner', 'questionPoll__poll').annotate(sum_score=Sum('score')).values('questionPoll__poll').annotate(count_user=Count('owner'))
        # баллы текущего пользователя в разрезе опросов
        cur_score = user_score_2.filter(owner=self.request.user)

        # >>> user_score.annotate(cur_score=Value(100,output_field=IntegerField()))
        # <QuerySet [{'owner': 4, 'questionPoll__poll': 1, 'sum_score': 91, 'cur_score': 100}]>

        # добавляем к каждому опросу к-во баллов по текущему пользователю
        # for cur in cur_score:
        # 2)
        user_score = user_score.annotate(cur_score=Value(cur_score.get(questionPoll__poll=F('questionPoll__poll'))['sum_score'], output_field=IntegerField()))
        # 3) к-во пользователей по каждому опросу
        user_score = user_score.annotate(count_user=Value(user_score_2.get(questionPoll__poll=F('questionPoll__poll'))['count_user'], output_field=IntegerField()))
        # 4) оставляем пользователей с большим количеством баллов
        user_score = user_score.filter(sum_score__gt=F('cur_score'))
        # 5) считаем пользователей с большим количеством баллов
        user_score = user_score.values('questionPoll__poll','count_user').annotate(gte_count_user=Count('owner'))
        # 6) вычисляем проценты
        user_score = user_score.annotate(percent=F('gte_count_user')/F('count_user')*100)
        # context["status"] = QuestionInPoll.objects.filter(answeruser__owner=self.request.user).annotate(count_answ=Count('answeruser'))
        # count_user_poll = AnswerUser.objects.values('owner', 'questionPoll__poll').annotate(sum_score=Sum('score'))
        # <QuerySet [{'questionPoll__poll': 1, 'count_user': 1, 'gte_count_user': 1, 'percent': 100}]>
        user_score = user_score.update(questionPoll__poll=F('questionPoll__poll.title'))
        context["polls_status"] = user_score
        # print(context)
        return context

AnswerPollFormSet = modelformset_factory(AnswerPoll, form=AnswerPollForm, can_order=True, can_delete=True, extra=4, max_num=4)

def answer_ball_old(request, poll_id, q_id):
    """ баллы за ответы в опросе для конкретного вопроса"""
    print(poll_id, q_id)
    # qp_Obj = QuestionInPoll.objects.get(id= int(qp_id))

    cur_poll = Poll.objects.get(id= int(poll_id))
    cur_question = Question.objects.get(id= int(q_id))
    print('cur_question - qp_Obj ', cur_question)
    cur_answer = cur_question.answer_set.all()

    print('cur_poll', cur_poll)
    print('cur_answer', cur_answer)

    # внешний ключ фильтруем по объекту, а не по ссылке
    # answer_list=[ {'ans_id': obj.id ,'question': obj.question, 'textAnswer': obj.textAnswer, 'rightFlg': obj.rightFlg} for obj in Answer.objects.filter(question=qObj)]
   
    if request.method == 'POST':
        print('answer_ball _request.POST: ', request.POST)
        answerPoll_formset = AnswerPollFormSet(request.POST)
        if answerPoll_formset.is_valid():
            answerPoll_formset.save(commit=False)
            for ans in answerPoll_formset.changed_objects:
                print('new changed_objects answer_form', ans)
                # ans.save()
            # answer_formset.save(commit=True)
            # if form.cleaned_data:
            # for answer_form in answer_formset.deleted_objects: #отфильтровать только заполненные формы
                # print('deleted_objects objects answer_form', answer_form.id)
                # answer_form.save()
            return HttpResponseRedirect(reverse_lazy('q_list'))
        else:
            print('not save')
    else:
        answerPoll_formset = AnswerPollFormSet(prefix='answer', queryset=AnswerPoll.objects.filter(poll=cur_poll))
    return render(request, 'answer_poll.html', {'question': cur_question.text, 'formset': answerPoll_formset})

def answer_ball(request, poll_id, q_id):
    template = loader.get_template('answer_poll.html')
    
    cur_poll = Poll.objects.get(id= int(poll_id))
    cur_question = Question.objects.get(id= int(q_id))
    print('poll_id', poll_id, cur_poll)
    print('q_id', q_id, cur_question)
    
    ans_poll = AnswerPoll.objects.filter(Q(poll=cur_poll) & Q(answer__question=cur_question))
    print(ans_poll)
    content = { "q_title": cur_question.text, 'poll': cur_poll.title, "ans_poll": ans_poll}
    return HttpResponse(template.render(content, request))

def balls_update(request, an_p_id):
    if request.method == 'POST':
        print(request.POST)
        p_id = request.POST['p_id']
        if not request.POST['an_p_id']:
            return redirect('poll_questions', poll_id=p_id) #poll_questions - название url
        else:
            an_p = AnswerPoll.objects.get(id=an_p_id)
            if not an_p:
                return redirect('admin_poll_list')
            an_p.score = int(request.POST['score'])
            an_p.save()
        return redirect('poll_questions', poll_id=p_id)
        # return redirect('admin_poll_list')
    else:
        return redirect('poll_questions', poll_id=p_id)
        # return redirect(f'balls/{p_id}/')


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
    if request.method == 'POST' and request.POST.get('rowid'): #сохраняем баллы за вопрос
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
    elif request.method == 'POST': #сохраняем изменения в опросе
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

    #вопросы текущего опроса
    qp_list = QuestionInPoll.objects.filter(poll=cur_poll)
    # prefetch_related
        # form = QuestionInPollForm(instance=g_list)
        # g_list = QuestionInPoll.objects.filter(poll=poll_id)

    # только вопросы в выборке, для отбора объектов вопросов
    qp_list_vall = qp_list.values('question')
    # вопросы текущего опроса
    question_list = Question.objects.filter(id__in=qp_list_vall)

    context = {'qp_list': qp_list, 'poll_id': poll_id, 'poll': cur_poll, 'question_list': question_list}
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
    # answer_list=[ {'ans_id': obj.id ,'question': obj.question, 'textAnswer': obj.textAnswer, 'rightFlg': obj.rightFlg} for obj in Answer.objects.filter(question=_id)]
    # внешний ключ фильтруем по объекту, а не по ссылке
    answer_list=[ {'ans_id': obj.id ,'question': obj.question, 'textAnswer': obj.textAnswer, 'rightFlg': obj.rightFlg} for obj in Answer.objects.filter(question=qObj)]
    print(qObj)
    print(_id)
    print(answer_list)
    if request.method == 'POST':
        answer_formset = AnswerFormSet(request.POST, request.FILES, prefix='answer', queryset=Answer.objects.filter(question=qObj))
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
                answer_form.save()
            form.save()
            return HttpResponseRedirect(reverse_lazy('q_list'))
        else:
            print('not save')
    else:
        # answerSet=Answer.objects.filter(question=_id)
        # answer_formset = AnswerFormSet(prefix='answer', initial=list(answerSet))
        # answer_list=[ {'question': obj.question, 'textAnswer': obj.textAnswer, 'rightFlg': obj.rightFlg} for obj in Answer.objects.filter(question=_id)]
        # print(answer_list)
        print(answer_list)
        # answer_formset = AnswerFormSet(prefix='answer', initial=answer_list)
        answer_formset = AnswerFormSet(prefix='answer', queryset=Answer.objects.filter(question=qObj), initial = [{'question': qObj}])
        # answer_formset = AnswerFormSet(prefix='answer', initial= [{'question': _id}, {'question': _id}, {'question': _id}, {'question': _id}])
        form = QuestionEditForm(instance=qObj)
    return render(request, 'question_answer_create.html', {'qObj': qObj, 'question_form' : form, 'answer_formset': answer_formset})


def poll_start(request, poll_id):
    """ Страница прохождения опроса для пользователя """
    cur_poll = Poll.objects.get(id=poll_id)
    # подтягиваем данные по внешнему ключу question
    questions = QuestionInPoll.objects.filter(poll=poll_id).select_related('question')
    message = ''
    for q in questions:
        print(q.question.text)
        for ans in q.question.answer_set.all():
            print(ans.textAnswer, ans.rightFlg)
    if request.method == 'POST':
        print(request.POST, type(request.POST))
        # print('201' , request.POST['ans-check'], type(request.POST['ans-check']), int(request.POST['ans-check']))
        # работает, выводит все атрибуты
        # ans_check = request.POST.lists()
        # for ans in ans_check:
        #     print(ans)
        set_ans = set(request.POST.getlist('ans-user')) # ответы пользователя
        print('getlist set_ans', set_ans)
        c_qInPoll = QuestionInPoll.objects.get(id=request.POST['q-in-p'])
        
        if 'q_id' in request.POST:
            c_question = Question.objects.get(id=request.POST['q_id'])
        else:
            None
        print(c_question)
        # удаляем предыдущий ответ пользователя
        answer_db = AnswerUser.objects.filter(owner = request.user, questionPoll= c_qInPoll) 
        if (answer_db.exists()):
            answer_db.delete()
            message = 'Ответ успешно обновлен'
            print('delete all answer')
        if len(set_ans)>0 and c_question:
            for tans in set_ans:
                tans = int(tans) # приводим ид ответов пользователя к целому числу
                print('tans', tans)
                n_score = AnswerPoll.objects.filter(answer=tans, poll=poll_id).first() # количество баллов данного ответа в текущем опросе
                n_score = n_score.score if n_score.score else 0
                print( 'n_score', n_score)
                c_answer = Answer.objects.get(id=tans) # ответ пользователя
                c_ansUser = AnswerUser.objects.create(owner = request.user, questionPoll= c_qInPoll, answer=c_answer, score=n_score, question=c_question, poll=cur_poll)
                c_ansUser.save()
                print('Ответы пользователя успешно сохранены ', c_ansUser.id)
                message = 'Ответ успешно сохранен'
        else:
            message = 'не выбран вариант ответа'
            print('не выбран вариант ответа')
    # answer_list=[ {'ans_id': obj.id ,'question': obj.question, 'textAnswer': obj.textAnswer, 'rightFlg': obj.rightFlg} for obj in Answer.objects.filter(question=_id)]
    context = {'questions': questions, 'poll_id': poll_id, 'message': message}
    return render(request, 'poll_start.html', context)

def user_stat(request):
    # 1) баллы по всем пользователям в разрезе опросов
    # print(request.user)
    user_score = AnswerUser.objects.values('owner', 'poll_id', 'poll__title').annotate(sum_score=Sum('score'))
    # print(user_score)
    # 2.1) оценки текущего пользователя по каждому опросу
    cur_score = user_score.filter(owner=request.user)
    # 2.2) баллы в разрезе опросов, дополненны баллами текущего пользователя
    # {'owner': 5, 'poll_id': 1, 'sum_score': 6, 'cur_score': 4}
    add_cur_sum = user_score.annotate(cur_score=Value(cur_score.get(poll_id=F('poll_id'))['sum_score'], output_field=IntegerField()))
    # 2.3) оставляем записи с оценками, больше оценки текущего пользователя
    gt_user_poll = add_cur_sum.filter(sum_score__gt=F('cur_score'))
    print('gt_user_poll')
    print(gt_user_poll)
    if gt_user_poll:
        print('есть лучшии')
        gt_count = gt_user_poll.exclude(owner=request.user).values('poll_id').annotate(gt_count=Count('owner', distinct=True))
    else:
        gt_user_poll = add_cur_sum
        gt_count = gt_user_poll.values('poll_id').annotate(gt_count=Count('owner', distinct=True))
    # 2.4) количество пользователей, набравших больше баллов, чем текущий пользователь
    # gt_count = gt_user_poll.exclude(owner=request.user).values('poll_id').annotate(gt_count=Count('owner', distinct=True))
    print(gt_user_poll)
    # gt_count = gt_user_poll.values('poll_id').annotate(gt_count=Count('owner', distinct=True))
    # 3) количество пользователей по каждому опросу
    distinct_user_poll = user_score.values('poll_id').annotate(count_user=Count('owner', distinct=True))
    # print('distinct_user_poll')
    # print(distinct_user_poll)
    # print('cur_score')
    # print(cur_score)
    # print('gt_count')
    # print(gt_count)
    # 4) собираем результаты в один набор данных
    pre_statistics = cur_score.annotate(count_user=Value(distinct_user_poll.get(poll_id=F('poll_id'))['count_user'], output_field=IntegerField())).annotate(gt_count=Value(gt_count.get(poll_id=F('poll_id'))['gt_count'] , output_field=IntegerField()))
    # >>> print(pre_statistics)
    # <QuerySet [{'owner': 4, 'poll_id': 1, 'sum_score': 4, 'count_user': 2, 'gt_count': 1}]>
    # 6) вычисляем рейтинг
    user_statistics = pre_statistics.annotate(percent=(F('gt_count')*100)/F('count_user'))
    # <QuerySet [{'owner': 4, 'poll_id': 1, 'sum_score': 4, 'count_user': 2, 'gt_count': 1, 'percent': 50}]>
    context = { "user_statistics": user_statistics }
    print(context)
    return render(request, 'statistics_user.html', context)

# def user_stat_old(request):
#     #баллы по всем пользователям в разрезе опросов
#     user_score = AnswerUser.objects.values('owner', 'questionPoll__poll', 'poll__title').annotate(sum_score=Sum('score'))
#     # user_score_2 = user_score.values('questionPoll__poll').annotate(count_user=Count('owner', distinct=True))
#     user_score_2 = user_score.values('poll__title', 'questionPoll__poll').annotate(count_user=Count('owner', distinct=True))
#     # Пользователь, опрос, сумма баллов
#     user_score_3 = AnswerUser.objects.values('owner', 'questionPoll__poll', 'poll__title').annotate(sum_score=Sum('score')).values('questionPoll__poll').annotate(count_user=Count('owner'))
#     # баллы текущего пользователя в разрезе опросов
#     cur_score = user_score.filter(owner=request.user)
#     # добавляем к каждому опросу к-во баллов по текущему пользователю
#     # 2)
#     user_score = user_score.annotate(cur_score=Value(cur_score.get(questionPoll__poll=F('questionPoll__poll'))['sum_score'], output_field=IntegerField()))
#     # 3) к-во пользователей по каждому опросу
#     user_score = user_score.annotate(count_user=Value(user_score_2.get(questionPoll__poll=F('questionPoll__poll'))['count_user'], output_field=IntegerField()))
#     # 4) оставляем пользователей с большим количеством баллов
#     user_score = user_score.filter(sum_score__gte=F('cur_score'))
#     # 5) считаем пользователей с большим количеством баллов
#     user_score = user_score.values('questionPoll__poll','count_user', 'poll__title').annotate(gte_count_user=Count('owner'))
    
#     # 6) вычисляем проценты
#     user_score = user_score.annotate(percent=(F('gte_count_user')/F('count_user'))*100)
#     context = { "user_score": user_score }
#     print(context)
#     return render(request, 'statistics_user.html', context)