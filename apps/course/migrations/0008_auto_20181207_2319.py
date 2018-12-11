# Generated by Django 2.1.3 on 2018-12-07 15:19

import DjangoUeditor.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_auto_20181117_0911'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='type',
            field=models.CharField(default='course', max_length=10, verbose_name='类型'),
        ),
        migrations.AlterField(
            model_name='course',
            name='detail',
            field=DjangoUeditor.models.UEditorField(default='', verbose_name='课程详情'),
        ),
    ]