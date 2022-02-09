# Generated by Django 2.2.6 on 2022-02-09 03:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sermon', '0006_auto_20200119_0524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sermonsundayschool',
            name='bible_verses',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='sermonsundayschool',
            name='english_title',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='sermonsundayschool',
            name='mp3',
            field=models.FileField(upload_to='static/worship/'),
        ),
        migrations.AlterField(
            model_name='sermonsundayschool',
            name='sermon_dt',
            field=models.DateField(default=datetime.date(2022, 2, 6), verbose_name='Sermon Date'),
        ),
        migrations.AlterField(
            model_name='sermonsundayschool',
            name='simplified_bible_verses',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='sermonsundayschool',
            name='simplified_chinese_title',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='sermonsundayschool',
            name='tradition_bible_verses',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='sermonsundayschool',
            name='tradition_chinese_title',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]
