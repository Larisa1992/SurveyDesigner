# Generated by Django 3.1.3 on 2020-11-29 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_auto_20201129_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='imgquestion/', verbose_name='Изображение'),
        ),
    ]
