# Generated by Django 2.1.3 on 2018-12-10 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20181203_2038'),
    ]

    operations = [
        migrations.RenameField(
            model_name='banner',
            old_name='image_url',
            new_name='link_url',
        ),
        migrations.RemoveField(
            model_name='banner',
            name='image',
        ),
        migrations.AddField(
            model_name='banner',
            name='img_url',
            field=models.CharField(default='', max_length=100, verbose_name='轮播图'),
        ),
    ]
