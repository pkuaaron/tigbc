from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
from sermon.models import SermonSundaySchool
from sermon.forms import SermonForm
from django.utils import translation
from django.utils.translation import gettext as _
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
    sermon_title_list = []
    for s in latest_sermons:
        sermon_title_list.append(get_title(s))
    ss_title_list = []
    for s in latest_sundayschool:
        ss_title_list.append(get_title(s))
    # import pdb
    # pdb.set_trace()
    context = {'sermon_list': [[x,y] for x,y in zip(latest_sermons, sermon_title_list)],
            'sundayschool_list':[[x,y] for x,y in zip(ss_title_list,latest_sundayschool)]}
    return render(request, 'sermon.html', context)


def upload_sermon(request):
    sermon_form = SermonForm()
    return render(request, 'sermon_editor.html', {'sermon': sermon_form})


def view_sermon(request, sermon_id):
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
        sermon = Sermon.objects.create()
        message = _('记录已经添加')
    sermon_form = SermonForm(instance=sermon)

    if request.method=='POST':
        sermon_form = SermonForm(request.POST or None, instance=sermon)
        if sermon_form.is_valid():
            sermon_form.save()
    return render(request, 'sermon_editor.html', {'sermon': sermon_form, 'message':message})

 # action="{% url 'sermon:details' sermon.id %}"
