# Generated by Django 2.0.5 on 2018-11-17 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0006_auto_20181117_0818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseorg',
            name='add_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='添加日期'),
        ),
    ]
