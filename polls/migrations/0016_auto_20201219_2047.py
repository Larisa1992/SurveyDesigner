# Generated by Django 3.1.3 on 2020-12-19 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0015_auto_20201216_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='polls',
            field=models.ManyToManyField(related_name='polls', through='polls.QuestionInPoll', to='polls.Poll', verbose_name='Опросы'),
        ),
    ]
