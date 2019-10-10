from django.forms import ModelForm
from sermon.models import SermonSundaySchool

class SermonForm(ModelForm):
    class Meta:
        model=SermonSundaySchool
        fields=["file_type",
                "english_title",
                "simplified_chinese_title",
                "tradition_chinese_title",
                "mp3",
                "bible_verses",
                "simplified_bible_verses",
                "tradition_bible_verses",
                "sermon_dt",
                "speaker",
                "tradition_chinese_speaker",
                "simplified_chinese_speaker"]
