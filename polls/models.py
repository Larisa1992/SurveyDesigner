from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# типы вопросов
TYPE_Q = ((1, 'Radio'), (2, 'Checkbox'),)

class Poll(models.Model):
    """Опрос из нескольких вопросов"""
    title = models.CharField(max_length=150, null=True, verbose_name=("Тема опроса")) 
    description = models.TextField(null=True, verbose_name="Описание")
    timer = models.IntegerField(verbose_name=("Максимальное время прохождения опроса"))
    publicationDate = models.DateTimeField(default=timezone.now, verbose_name=("Дата публикации"))
    
    def __str__(self):
        """Возвращает строковое представление модели"""
        return self.title

class Question(models.Model):
    """Вопросы для составления опросов"""
    text = models.CharField(max_length=500, null=True, verbose_name=("Вопрос"))
    # тип вопроса - chose поле
    typeQuestion = models.IntegerField(choices=TYPE_Q, default=1, verbose_name='Тип вопроса')
    timer = models.IntegerField(verbose_name=("Время ответа на вопрос (в секундах)"))
    polls = models.ManyToManyField(
        Poll,
        through='QuestionInPoll', # through - имя связующей модели
        through_fields=('question', 'poll'),
        related_name='polls'
    )
    picture = models.ImageField(upload_to='imgquestion/', verbose_name='Изображение', null=True,  blank=True)

    def get_parents(self):
        return ",".join([str(p) for p in self.polls.all()])

    def __str__(self):
        return f'{self.text}'

class QuestionInPoll(models.Model):
    """Таблица для связи вопросов и опросов (связь многие ко многим)"""
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, verbose_name="Вопрос")
    poll = models.ForeignKey(Poll, on_delete=models.SET_NULL, null=True, verbose_name="Опрос")
    score = models.SmallIntegerField(null=True, verbose_name="Количество баллов")
    
    def __str__(self):
        return f'Вопрос: "{str(self.question)}" опроса "{self.poll}"'

    # def get_absolute_url(self):
    #     return f'/poll_questions/{self.pk}/'

class Answer(models.Model):
    """Варианты ответа на вопрос"""
    textAnswer = models.CharField(max_length=150, verbose_name=("Вариант ответа"))
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name=("Вопрос"))
    rightFlg = models.BooleanField(default=False, verbose_name=("Правильный ответ"))

    def __str__(self):
        return f'{str(self.rightFlg)} {self.textAnswer}'
# class AnswerPoll(models.Model):
#     """Варианты ответа на вопрос"""
#     answer = models.Answer(Question, on_delete=models.CASCADE, verbose_name=("Вариант ответа"))
#     poll = models.ForeignKey(Poll, on_delete=models.CASCADE, verbose_name=("Опрос"))
#     score = models.SmallIntegerField(null=True, verbose_name="Количество баллов")

#     def __str__(self):
#         return f'{str(self.answer)} (баллов {self.score})'
class AnswerUser(models.Model):
    """Ответы пользователя"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=("Пользователь"))
    questionPoll = models.ForeignKey(QuestionInPoll, on_delete=models.CASCADE, verbose_name=("Вопрос из опроса"))
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name=("Вопрос")) #для вывода в __str__
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name=("Ответ"))
    score = models.SmallIntegerField(null=True, verbose_name="Количество баллов")
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, verbose_name=("Опрос"))

    def __str__(self):
        return f'{self.owner} {self.question} {self.answer}'

class AnswerPoll(models.Model):
    """Баллы за ответы в опросах"""
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name=("Ответ"))
    score = models.SmallIntegerField(null=True, verbose_name="Количество баллов")
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, verbose_name=("Опрос"))

    def __str__(self):
        return f'{self.answer} ({str(self.score)})'