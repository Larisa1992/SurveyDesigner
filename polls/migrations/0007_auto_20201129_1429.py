# Generated by Django 3.1.3 on 2020-11-29 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20201129_1041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='picture',
            field=models.ImageField(null=True, upload_to='imgquestion/', verbose_name='Изображение'),
        ),
    ]
