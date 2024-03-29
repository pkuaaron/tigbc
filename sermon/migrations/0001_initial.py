# Generated by Django 2.2.6 on 2019-10-09 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SermonSundaySchool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('mp3', models.CharField(max_length=100)),
                ('bible_verses', models.CharField(max_length=200)),
                ('sermon_dt', models.DateField(verbose_name='Sermon Date')),
                ('speaker', models.CharField(default='Pastor Kevin Wang', max_length=200)),
                ('upload_dt', models.DateTimeField(verbose_name='Upload Time')),
            ],
        ),
    ]
