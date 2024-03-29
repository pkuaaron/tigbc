# Generated by Django 3.0.2 on 2020-01-19 05:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sermon', '0004_auto_20191009_0033'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyBible',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_name', models.CharField(max_length=100)),
                ('language', models.CharField(max_length=32)),
                ('date', models.DateField(verbose_name='Bible Date')),
                ('weekday', models.CharField(max_length=100)),
                ('book', models.CharField(max_length=100)),
                ('chapter', models.IntegerField()),
                ('start_verse', models.IntegerField()),
                ('end_verse', models.IntegerField()),
                ('bible_verses', models.CharField(max_length=1000)),
                ('html', models.CharField(max_length=1000)),
            ],
        ),
        migrations.AlterField(
            model_name='sermonsundayschool',
            name='sermon_dt',
            field=models.DateField(default=datetime.date(2020, 1, 19), verbose_name='Sermon Date'),
        ),
    ]
