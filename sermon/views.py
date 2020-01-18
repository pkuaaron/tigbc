from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
from sermon.models import SermonSundaySchool
from sermon.forms import SermonForm
from django.utils import translation
from django.utils.translation import gettext as _
# Create your views here.


def view_sermon_list(request):
    latest_sermons = SermonSundaySchool.objects.order_by('-sermon_dt')[:5]
    template = loader.get_template('sermon.html')
    sermon_title_list = []
    for s in latest_sermons:
        lang = translation.get_language()
        if lang == 'zh-hans':
            title = ' '.join([s.sermon_dt.strftime('%m/%d/%Y'), s.simplified_chinese_title, '('+s.simplified_bible_verses+')', lang])
        elif lang == 'zh-hant':
            title = ' '.join([s.sermon_dt.strftime('%m/%d/%Y'), s.tradition_chinese_title, '('+s.tradition_bible_verses+')', lang])
        else:
            title = ' '.join([s.sermon_dt.strftime('%m/%d/%Y'), s.english_title, '('+s.bible_verses+')', lang])
        sermon_title_list.append(title)
    context = {'sermon_list': zip(latest_sermons, sermon_title_list)}
    return HttpResponse(template.render(context, request))


def upload_sermon(request):
    sermon_form = SermonForm()
    return render(request, 'sermon_upload.html', {'sermon': sermon_form})


def view_sermon(request, sermon_id):
    try:
        sermon = SermonSundaySchool.objects.get(pk=sermon_id)
    except sermon.DoesNotExist:
        raise Http404(_("Sermon does not exist"))
    return render(request, 'sermon_details.html', {'sermon': sermon})


def edit_sermon(request, sermon_id):
    try:
        sermon = SermonSundaySchool.objects.get(pk=sermon_id)
        sermon_form = SermonForm(instance=sermon)
        sermon_title = SermonSundaySchool
    except sermon.DoesNotExist:
        raise Http404(_("Sermon does not exist"))
    return render(request, 'sermon_editor.html', {'sermon': sermon_form})

 # action="{% url 'sermon:details' sermon.id %}"
