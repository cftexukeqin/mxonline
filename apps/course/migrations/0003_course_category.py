# Generated by Django 2.1.3 on 2018-11-15 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_course_course_org'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.CharField(default='', max_length=50, verbose_name='课程分类'),
        ),
    ]