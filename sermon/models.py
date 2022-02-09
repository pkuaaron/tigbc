from django.db import models
import datetime


class SermonSundaySchool(models.Model):
    file_type = models.CharField(max_length=50, choices=[('Sermon', 'Sermon'), ('Sunday School', 'Sunday School')], default='Sermon')
    english_title = models.CharField(max_length=200, default='', null=True, blank=True)
    simplified_chinese_title = models.CharField(max_length=200, default='', null=True, blank=True)
    tradition_chinese_title = models.CharField(max_length=200, default='', null=True, blank=True)
    mp3 = models.FileField(upload_to='static/worship/')
    bible_verses = models.CharField(max_length=200, default='', null=True, blank=True)
    simplified_bible_verses = models.CharField(max_length=200, default='', null=True, blank=True)
    tradition_bible_verses = models.CharField(max_length=200, default='', null=True, blank=True)
    today = datetime.date.today()
    idx = (today.weekday() + 1) % 7
    sun = today - datetime.timedelta(idx)

    sermon_dt = models.DateField('Sermon Date', default=sun)
    speaker = models.CharField(max_length=200, default='Pastor Kevin Wang')
    tradition_chinese_speaker = models.CharField(max_length=200, default='王宇輝傳道')
    simplified_chinese_speaker = models.CharField(max_length=200, default='王宇辉传道')
    # upload_dt=models.DateTimeField('Upload Time')

    def __str__(self):
        return ' '.join([self.sermon_dt.strftime('%m/%d/%Y'), self.english_title, '('+self.bible_verses+')'])


class DailyBible(models.Model):
    plan_name = models.CharField(max_length=100, null=True, blank=True)
    language = models.CharField(max_length=32, null=True, blank=True)
    date = models.DateField('Bible Date', null=True, blank=True,)
    weekday = models.CharField(max_length=100, null=True, blank=True,)
    book = models.CharField(max_length=100, null=True, blank=True,)
    chapter = models.IntegerField(null=True, blank=True,)
    start_verse = models.IntegerField(null=True, blank=True,)
    end_verse = models.IntegerField(null=True, blank=True,)
    bible_verses = models.CharField(max_length=1000, null=True, blank=True,)
    html = models.CharField(max_length=1000, null=True, blank=True,)

    def __str__(self):
        return self.html
