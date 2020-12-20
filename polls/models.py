from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# типы вопросов
TYPE_Q = ((1, 'Radio'), (2, 'Checkbox'),)

class Poll(models.Model):
    """Модель опроса"""
    title = models.CharField(max_length=150, null=True, verbose_name=("Тема опроса"))  #: Тема опроса.
    description = models.TextField(null=True, verbose_name="Описание") #: Описание назначения опроса.
    timer = models.IntegerField(verbose_name=("Максимальное время прохождения опроса")) #: Длительность опроса.
    publicationDate = models.DateTimeField(default=timezone.now, verbose_name=("Дата публикации")) #: Крайняя дата прохождения опроса.
    created_dttm = models.DateTimeField(auto_now_add=True, verbose_name=("Дата создания")) #: Дата создания опроса.
    update_dttm = models.DateTimeField(auto_now=True, verbose_name=("Дата изменения")) #: Дата изменения опроса.

    def __str__(self):
        """Строкое представление объекта опроса"""
        return self.title

    class Meta:
        """Настройки для отображения в стандартной админке django"""
        verbose_name='Опрос'
        verbose_name_plural='Опросы'
        ordering =['publicationDate']

class Question(models.Model):
    """Модель вопросов"""
    text = models.CharField(max_length=500, null=True, verbose_name=("Вопрос")) #: Содержание вопроса
    typeQuestion = models.IntegerField(choices=TYPE_Q, default=1, verbose_name='Тип вопроса') #: Тип вопроса - chose поле
    timer = models.IntegerField(verbose_name=("Время ответа на вопрос (в секундах)")) #: Время ответа на вопрос (в секундах)
    polls = models.ManyToManyField(
        Poll,
        through='QuestionInPoll', # through - имя связующей модели
        through_fields=('question', 'poll'),
        related_name='polls',
        verbose_name='Опросы'
    ) #: Связ ManyToMany с опросами
    picture = models.ImageField(upload_to='imgquestion/', verbose_name='Изображение', null=True,  blank=True) #: Изображение для вопроса

    def get_parents(self):
        return ",".join([str(p) for p in self.polls.all()])
    """Строкое представление объекта вопроса"""
    def __str__(self):
        """Строкое представление объекта вопроса"""
        return f'{self.text}'
    
    def get_absolute_url(self):
        return reverse('q_create', kwargs={'pk': self.pk})

    class Meta:
        """Настройки для отображения в стандартной админке django"""
        verbose_name='Вопрос'
        verbose_name_plural='Вопросы'
        ordering =['text']

class QuestionInPoll(models.Model):
    """Таблица для связи вопросов и опросов (связь многие ко многим)"""
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, verbose_name="Вопрос") #: Вопрос
    poll = models.ForeignKey(Poll, on_delete=models.SET_NULL, null=True, verbose_name="Опрос") #: Опрос
    score = models.SmallIntegerField(null=True, verbose_name="Количество баллов") # удалить поле
    
    def __str__(self):
        return f'Вопрос: "{str(self.question)}" опроса "{self.poll}"'
    
    class Meta:
        """Настройки для отображения в стандартной админке django"""
        verbose_name='Связь вопроса и опроса'
        verbose_name_plural='Связь вопросов с опросами'
class Answer(models.Model):
    """Варианты ответа на вопрос.
    Каждый ответ может быть привязан только к одному вопросу.
    """
    textAnswer = models.CharField(max_length=150, verbose_name=("Вариант ответа")) #: Текст ответа
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name=("Вопрос")) #: Вопрос

    def __str__(self):
        return f'{self.textAnswer}'
# отображение в админке
    class Meta:
        verbose_name='Ответ'
        verbose_name_plural='Ответы'
        ordering =['textAnswer']
class AnswerUser(models.Model):
    """Ответы пользователя"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=("Пользователь")) #: Пользователь
    questionPoll = models.ForeignKey(QuestionInPoll, on_delete=models.CASCADE, verbose_name=("Вопрос из опроса")) #: Ссылка на QuestionInPoll - вопрос в конкретном опросе
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name=("Вопрос")) #: Вопрос (вспомогательное поле для вывода в __str__ )
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name=("Ответ")) #: Ссылка на QuestionInPoll - вопрос в конкретном опросе
    score = models.SmallIntegerField(null=True, verbose_name="Количество баллов") #: Количество баллов, заработанное пользователем
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, verbose_name=("Опрос")) #: Опрос

    def __str__(self):
        return f'{self.owner} {self.question} {self.answer}'
    
    class Meta:
        verbose_name='Ответ пользователя'
        verbose_name_plural='Ответы пользователя'
        ordering =['owner']

class AnswerPoll(models.Model):
    """Баллы за ответы в опросах
    Каждый ответ в зависимости от опроса, к которому относится вопрос, имеет разное количество баллов
    """
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name=("Ответ")) #: Ссылка на модель Ответ
    score = models.SmallIntegerField(null=True, verbose_name="Количество баллов") #: Количество баллов в рамках опроса
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, verbose_name=("Опрос")) #: Опрос

    def __str__(self):
        return f'{self.answer} ({str(self.score)})'

    class Meta:
        verbose_name='Ответ в опросах'
        verbose_name_plural='Ответы в опросах'
        ordering =['poll']