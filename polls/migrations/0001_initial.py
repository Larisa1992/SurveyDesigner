# Generated by Django 3.1.3 on 2020-11-25 20:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, null=True, verbose_name='Тема опроса')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('timer', models.IntegerField(verbose_name='Максимальное время прохождения опроса')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, null=True, verbose_name='Вопрос')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionInPoll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timer', models.IntegerField(verbose_name='Время ответа на вопрос')),
                ('poll', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='polls.poll')),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='polls.question')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='polls',
            field=models.ManyToManyField(through='polls.QuestionInPoll', to='polls.Poll'),
        ),
    ]