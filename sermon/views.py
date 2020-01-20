from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
from sermon.models import SermonSundaySchool, DailyBible
from sermon.forms import SermonForm
from django.utils import translation
from django.utils.translation import gettext as _
from dateutil import relativedelta
import datetime
# Create your views here.


def get_title(s):
    lang = translation.get_language()
    if lang == 'zh-hans':
        title = ' '.join([s.sermon_dt.strftime('%m/%d/%Y'), s.simplified_chinese_title, '('+s.simplified_bible_verses+')'])
    elif lang == 'zh-hant':
        title = ' '.join([s.sermon_dt.strftime('%m/%d/%Y'), s.tradition_chinese_title, '('+s.tradition_bible_verses+')'])
    else:
        title = ' '.join([s.sermon_dt.strftime('%m/%d/%Y'), s.english_title, '('+s.bible_verses+')'])
    return title


def view_sermon_list(request):
    latest_sermons = SermonSundaySchool.objects.filter(file_type='Sermon').order_by('-sermon_dt')[:5]
    latest_sundayschool = SermonSundaySchool.objects.filter(file_type='Sunday School').order_by('-sermon_dt')[:5]
    today = datetime.datetime.now()
    start = today - datetime.timedelta((today.weekday() + 1) % 7)
    sat = start + relativedelta.relativedelta(weekday=relativedelta.SA(-1))
    sunday = sat + relativedelta.relativedelta(weekday=relativedelta.SU(-1))
    lang = translation.get_language()
    days_of_bible = 8
    if lang == 'zh-hans':
        biblereading_plan = DailyBible.objects.filter(language='SimpleChinese', plan_name='Chapter', date__gte=sunday).order_by('date')[:days_of_bible]
        biblereading_plan2 = DailyBible.objects.filter(language='SimpleChinese', plan_name='Chronology', date__gte=sunday).order_by('date')[:days_of_bible]

    elif lang == 'zh-hant':
        biblereading_plan = DailyBible.objects.filter(language='TraditionChinese', plan_name='Chapter', date__gte=sunday).order_by('date')[:days_of_bible]
        biblereading_plan2 = DailyBible.objects.filter(language='TraditionChinese', plan_name='Chronology', date__gte=sunday).order_by('date')[:days_of_bible]

    else:
        biblereading_plan = DailyBible.objects.filter(language='English', plan_name='Chapter', date__gte=sunday).order_by('date')[:days_of_bible]
        biblereading_plan2 = DailyBible.objects.filter(language='English', plan_name='Chronology', date__gte=sunday).order_by('date')[:days_of_bible]
    sermon_title_list = []
    for s in latest_sermons:
        sermon_title_list.append(get_title(s))
    ss_title_list = []
    for s in latest_sundayschool:
        ss_title_list.append(s.sermon_dt.strftime('%d/%m/%Y ')+_('主日学校'))
    # import pdb
    # pdb.set_trace()
    context = {'sermon_list': [[x, y] for x, y in zip(latest_sermons, sermon_title_list)],
               'sundayschool_list': [[x, y] for x, y in zip(latest_sundayschool, ss_title_list)],
               'biblereading_plan': biblereading_plan, 'biblereading_plan2': biblereading_plan2}
    return render(request, 'sermon.html', context)


def upload_sermon(request):
    sermon_form = SermonForm()
    return render(request, 'sermon_editor.html', {'sermon': sermon_form})


def view_sermon(request, sermon_id):
    # load_bible_reading_plan()
    try:
        sermon = SermonSundaySchool.objects.get(pk=sermon_id)
    except sermon.DoesNotExist:
        raise Http404(_("Sermon does not exist"))
    return render(request, 'sermon_details.html', {'sermon': sermon})


def edit_sermon(request, sermon_id=None):
    if sermon_id:
        sermon = SermonSundaySchool.objects.get(pk=sermon_id)
        message = _('记录已经更新')
    else:
        sermon = SermonSundaySchool.objects.create()
        message = _('记录已经添加')
    sermon_form = SermonForm(instance=sermon)

    if request.method == 'POST':
        sermon_form = SermonForm(request.POST or None, instance=sermon)
        if sermon_form.is_valid():
            sermon_form.save()
    return render(request, 'sermon_editor.html', {'sermon': sermon_form, 'message': message})


def load_bible_reading_plan():
    import pandas as pd
    from dateutil import parser
    for lang in ['English', 'SimpleChinese', 'TraditionChinese']:
        sc = pd.read_excel(r"/home/aaron/ml/2020_bible_reading_plan_by_chapters.xlsx", sheet_name=lang)
        dicts = sc.to_dict(orient='row')
        for d1 in dicts:
            # import pdb
            # pdb.set_trace()
            db = DailyBible.objects.create(plan_name='Chapter', language=lang,
                                           date=d1['Date'],  # bible_verses=d1['BibleVerses'],
                                           weekday=d1['Weekday'], html=d1['link'], book=d1['Book'])

            db.save()
