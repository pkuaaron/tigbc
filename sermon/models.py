from django.db import models
import datetime


class SermonSundaySchool(models.Model):
    file_type=models.CharField(max_length=50,choices=[('Sermon','Sermon'),('Sunday School','Sunday School')],default='Sermon')
    english_title=models.CharField(max_length=200,default='')
    simplified_chinese_title=models.CharField(max_length=200,default='')
    tradition_chinese_title=models.CharField(max_length=200,default='')
    mp3=models.FileField()
    bible_verses=models.CharField(max_length=200,default='')
    simplified_bible_verses=models.CharField(max_length=200,default='')
    tradition_bible_verses=models.CharField(max_length=200,default='')
    today = datetime.date.today()
    idx = (today.weekday() + 1) % 7
    sun = today - datetime.timedelta(idx)

    sermon_dt=models.DateField('Sermon Date', default=sun)
    speaker=models.CharField(max_length=200, default='Pastor Kevin Wang')
    tradition_chinese_speaker=models.CharField(max_length=200, default='王宇輝傳道')
    simplified_chinese_speaker=models.CharField(max_length=200, default='王宇辉传道')
    # upload_dt=models.DateTimeField('Upload Time')

    def __str__(self):
        return ' '.join([self.sermon_dt.strftime('%m/%d/%Y'),self.english_title,'('+self.bible_verses+')'])
