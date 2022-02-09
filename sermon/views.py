import pdb

from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
from sermon.models import SermonSundaySchool, DailyBible
from sermon.forms import SermonForm
from django.utils import translation
from django.utils.translation import gettext as _
from dateutil import relativedelta
import datetime
import pandas as pd
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


def edit_sermon(request):
    return view_sermon_list(request, edit=True)


def view_sermon_list(request,edit=False):
    latest_sermons = SermonSundaySchool.objects.filter(file_type='Sermon').order_by('-sermon_dt')[:5]
    latest_sundayschool = SermonSundaySchool.objects.filter(file_type='Sunday School').order_by('-sermon_dt')[:5]
    today = datetime.date.today()
    idx = (today.weekday() + 1) % 7
    sunday = today - datetime.timedelta(idx)
    lang = translation.get_language()
    days_of_bible = 5
    # path= r'/home/aaron/projects_other/website/BibleReadingplan2021.xlsx'
    #
    # df = pd.read_excel(path,'SimpleChinese')
    # for idx, row in df.iterrows():
    #     obj = DailyBible.objects.create(plan_name='Plan 2022', language='SimpleChinese', date=row['Date'], weekday=row['WeekDay'], bible_verses=row['BookVerses'], html=row['Htmls'])
    #     obj.save()
    # df = pd.read_excel(path,'English')
    # for idx, row in df.iterrows():
    #     obj = DailyBible.objects.create(plan_name='Plan 2022', language='English', date=row['Date'], weekday=row['WeekDay'], bible_verses=row['BookVerses'], html=row['Htmls'])
    #     obj.save()
    #     # pdb.set_trace()
    if lang == 'zh-hans':
        biblereading_plan = DailyBible.objects.filter(language='SimpleChinese', plan_name='Plan 2022', date__gte=sunday).order_by('date')[:days_of_bible]

    elif lang == 'zh-hant':
        biblereading_plan = DailyBible.objects.filter(language='TraditionChinese', plan_name='Plan 2022', date__gte=sunday).order_by('date')[:days_of_bible]

    else:
        biblereading_plan = DailyBible.objects.filter(language='English', plan_name='Plan 2022', date__gte=sunday).order_by('date')[:days_of_bible]
    sermon_title_list = []
    for s in latest_sermons:
        sermon_title_list.append(get_title(s))
    ss_title_list = []
    for s in latest_sundayschool:
        ss_title_list.append(s.sermon_dt.strftime('%m/%d/%Y ')+_('主日学'))
    # import pdb
    # pdb.set_trace()
    context = {'sermon_list': [[x, y] for x, y in zip(latest_sermons, sermon_title_list)],
               'sundayschool_list': [[x, y] for x, y in zip(latest_sundayschool, ss_title_list)],
               'biblereading_plan': biblereading_plan,
               'edit': edit}
    return render(request, 'sermon.html', context)


def upload_sermon(request):
    if request.method == 'POST':
        # pdb.set_trace()
        form = SermonForm(request.POST, request.FILES)
        if form.is_valid():
            # instance = SermonSundaySchool(file_field=request.FILES['file'])
            form.save()
    sermon_form = SermonForm()
    return render(request, 'sermon_editor.html', {'sermon': sermon_form})


def view_sermon(request, sermon_id):
    # load_bible_reading_plan()
    try:
        sermon = SermonSundaySchool.objects.get(pk=sermon_id)
    except sermon.DoesNotExist:
        raise Http404(_("Sermon does not exist"))
    return render(request, 'sermon_details.html', {'sermon': sermon})


def delete_sermon(request, sermon_id):
    try:
        sermon = SermonSundaySchool.objects.get(pk=sermon_id)
        sermon.delete()
    except sermon.DoesNotExist:
        raise Http404(_("Sermon does not exist"))
    return render(request, 'sermon_details.html', {'sermon': sermon})


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
