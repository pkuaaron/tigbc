from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages
from accountapp.forms import SignupForm
from accountapp.token import AccountAppToken
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import send_mail
from django.conf import settings
import datetime
import pdb


def home(request):
    lang = request.LANGUAGE_CODE
    return render(request, "home.html", {'about': '/'.join([lang, "about.txt"])})


def calendar(request):
    return render(request, "calendar.html")


def announcement(request):
    return render(request, "announcement.html")


def sentMessage(request):
    subject = '[TIGBC]Email from visitor %s' % request.GET['name']
    message = '\n'.join(['Name:'+request.GET['name'], 'Email: '+request.GET['email'], 'Phone:'+request.GET['phone'], 'Message:'+request.GET['message']])
    email_from = request.GET['email']
    recipient_list = ['pkuaaron@gmail.com']
    send_mail(subject, message, email_from, recipient_list)
    return render(request, 'message.html', {'message': 'Thank you for your message, we will contact you soon.'})


def faith(request):
    lang = request.LANGUAGE_CODE

    try:
        return render(request, '/'.join([lang, "faith.html"]))
    except Exception as e:
        return render(request, '/'.join(["zh-hant", "faith.html"]))


def children_ministry(request):
    return render(request, "children_ministry.html")


def signup(request):
    # 不需要激活的注册
    form = SignupForm()

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            auth_login(request, authenticate(request, username=username, password=password))
            return profile(request)
        else:
            # pdb.set_trace()
            return HttpResponse("<html><body><h1>注册失败！</h1></body></html>")
    return render(request, 'signup.html', {'form': form})

# 需要激活的注册


def signup_activate(request):
    form = SignupForm()

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_active = False

            user.save()

            uid = user.pk
            token = AccountAppToken().make_token(user)

            domain = get_current_site(request).domain
            message = render_to_string('activate_account_email.html', context={'domain': domain, 'uid': uid, 'token': token}, request=request)

            email = EmailMessage(subject='激活用户名', body=message, from_email="admin@ejile.com", to=[form.cleaned_data['email']])
            email.send()

            # auth_login(request,authenticate(request,username=username,password=password))
            return profile(request)
        else:
            # pdb.set_trace()
            return HttpResponse("<html><body><h1>注册失败！</h1></body></html>")
    return render(request, 'signup.html', {'form': form})


def activate_account(request, uid, token):
    try:
        user = User.objects.get(pk=uid)
        # check_token to be implemented
        # token should be exactly the same as the one generated during signup
        token_checked = AccountAppToken().check_token(user, token)
        if user and token_checked is True:
            user.is_active = True
            user.save()
            auth_login(request, user)
            return redirect('accountapp:home')
    except User.DoesNotExist:
        return render(HttpResponse('<html><body><h1>用户不存在</h1></html></body>'))
    return render(HttpResponse('<html><body><h1>激活失败</h1></html></body>'))


def display_error(errors):
    return list(errors.values)[0]


def reset_password_done(request):
    return render(request, 'message.html', {'message': '密码设置成功！'})


def change_password_done(request):
    return render(request, 'message.html', {'message': '密码修改成功！'})


def forget_password(request):
    form = PasswordResetForm()
    if request.method == 'POST':
        form = PasswordResetForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            # 不用get是因为django的一个邮箱可以有多个用户，我们会在后面讲道如何使用邮箱作为用户名。
            users = User.objects.filter(email=email)
            if users:
                user = users[0]

                uidb64 = force_text(urlsafe_base64_encode(force_bytes(user.pk)).encode())
                # urlsafe_base64_decode(uidb64).decode()
                token = AccountAppToken().make_token(user)
                domain = get_current_site(request).domain
                # 使用了参数是uidb64而不是uid
                message = render_to_string('reset_password_email.html', context={'domain': domain, 'uidb64': uidb64, 'token': token}, request=request)

                email = EmailMessage(subject='重设用户密码', body=message, from_email="admin@ejile.com", to=[email])
                email.send()
                return render(request, 'message.html', {'message': '重新设置密码的邮件已经发到您的邮箱%s' % form.cleaned_data['email']})
            else:
                return render(request, 'message.html', {'message': '没有找到相应的用户 %s ' % email})
        else:
            return render(request, 'forget_password.html', {'form': form, 'warning_message': display_error(form.errors)})
    return render(request, 'forget_password.html', {'form': form})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('accountapp:home')
        else:
            return render(request, 'login.html', {'error_message': '登录失败!用户名和密码组合错误'})
    return render(request, 'login.html')


def logout(request):
    auth_logout(request)
    return redirect('accountapp:home')


@login_required(login_url="accountapp:signup")
def profile(request):
    return render(request, 'profile.html')
