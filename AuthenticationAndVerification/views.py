import base64
from datetime import datetime as dt
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMultiAlternatives
from BlogStation.models import BlogModel

from .models import User
#support class and functions

def send_the_mail(request, u, template_path, subject):
    current_site = get_current_site(request)
    email_subject = subject
    t = Token()
    msg_plain = ""
    html_message = render_to_string(template_path, {
        'user': User,
        'domain': current_site.domain,
        'uname': urlsafe_base64_encode(force_bytes(u.username)),
        'token': t.create_token(),
    })
    to_email = u.email
    send_mail(email_subject, msg_plain, 'mohit.djmail@gmail.com', [to_email], html_message=html_message)

class Token:
    def create_token(self):
        time_stamp_bytes = str(dt.now().strftime(
            "%d %H:%M:%S")).encode('ascii')
        base64_ts_bytes = base64.b64encode(time_stamp_bytes)
        base64_time_stamp = base64_ts_bytes.decode('ascii')

        token = base64_time_stamp
        return token

    def check_validity(self, token, time):
        tk1 = token
        tk2 = self.create_token()

        dt_obj_ts1 = dt.strptime(base64.b64decode(
            tk1).decode('ascii'), "%d %H:%M:%S")
        dt_obj_ts2 = dt.strptime(base64.b64decode(
            tk2).decode('ascii'), "%d %H:%M:%S")

        time_delta = dt_obj_ts2 - dt_obj_ts1
        minutes = float(format(time_delta.total_seconds() / 60, '.3f'))

        if minutes < time:
            return True
        else:
            return False


# views
def login(request):
    authenticated = False
    context = {}
    if request.method == "GET":
        if 'email_to_reset' in request.GET:
            not_exist = True
            users = User.objects.all()
            for user in users:
                if user.email == request.GET['email_to_reset']:
                    not_exist = False
                    u = user
                    send_the_mail(
                        request, u, 'AuthenticationAndVerification/reset_password_email.html', "password reset test")
                    return JsonResponse({"matched": True})

            if not_exist:
                return JsonResponse({"not_matched": True})

    elif request.method == "POST":
        users = User.objects.all()
        uname_or_email = request.POST["uname_or_email"]
        password = request.POST["password"]
        u = None

        for user in users:
            if user.username == uname_or_email or user.email == uname_or_email:
                if user.password == password:
                    authenticated = True
                    u = user

        if authenticated:
            request.session["log_key"] = u.username
            return redirect('writers_dashboard')
        else:
            context = {"mismatch": True}

    return render(request, 'AuthenticationAndVerification/login.html', context)


def register(request):
    context = {}
    if request.method == "GET":
        if "uname" in request.GET:
            uname = request.GET["uname"]
            find = User.objects.filter(username=uname).first()
            if find:
                data = {"found": True}
                return JsonResponse(data)
            else:
                data = {"found": False}
                return JsonResponse(data)
        if "email" in request.GET:
            email = request.GET["email"]
            find = User.objects.filter(email=email).first()
            if find:
                data = {"found": True}
                return JsonResponse(data)
            else:
                data = {"found": False}
                return JsonResponse(data)
        return render(request, 'AuthenticationAndVerification/register.html', context)

    elif request.method == "POST":
        u = User()
        u.username = request.POST["username"]
        u.email = request.POST["email"]
        u.password = request.POST["psw"]
        u.first_name = request.POST["firstname"]
        u.last_name = request.POST["lastname"]

        users = User.objects.all()
        save_it = True

        for user in users:
            if u.username == user.username:
                save_it = False
                context["uname_exist"] = True

            if u.email == user.email:
                save_it = False
                context["email_exist"] = True

        if save_it:
            u.datetime = timezone.now()
            u.save()
            send_the_mail(request, u, 'AuthenticationAndVerification/activate_email.html', "account activation test")
            context["verification"] = u.email
        return render(request, 'AuthenticationAndVerification/register.html', context)
    return render(request, 'AuthenticationAndVerification/register.html', context)



def delete_session(request):
    request.session.flush()
    request.session.clear_expired()
    return redirect('/')


def activate(request, uname_b64, token):
    context = {}
    try:
        uname = urlsafe_base64_decode(uname_b64).decode()
        user = User.objects.get(username=uname)
    except():
        user = None

    t = Token()
    if user is None:
        context["msg"] = "invalid activation link"
    elif t.check_validity(token, 40) is False:
        context["msg"] = "this activation is disposed"
    else:
        user.email_verified = True
        user.save()
        context['verified'] = True
        return render(request, 'AuthenticationAndVerification/activate.html', context)

    return HttpResponse(request, 'This link is expired you are later than 40 minutes')

def reset_password(request, uname_b64, token):
    context = {}
    if request.method == "POST":
        uname = urlsafe_base64_decode(uname_b64).decode()
        user = User.objects.get(username=uname)
        password = request.POST['password']
        user.password = password
        user.save()
        context['verified'] = True
        context["updated"] = True
        return render(request, 'AuthenticationAndVerification/reset_password.html', context)
    else:
        try:
            uname = urlsafe_base64_decode(uname_b64).decode()
            user = User.objects.get(username=uname)
        except():
            user = None

        t = Token()
        if user is None:
            context["msg"] = "invalid password reset link"
        elif t.check_validity(token, 40) is False:
            context["msg"] = "this password reset link is disposed"
        else:
            context['uname'] = uname_b64
            context['token'] = token
            context['verified'] = True
            return render(request, 'AuthenticationAndVerification/reset_password.html', context)

    return render(request, 'AuthenticationAndVerification/reset_password.html', context)

def ajax_verify_email(request):
    user = User.objects.all().filter(username=request.session['log_key']).first()
    context = {}
    send_the_mail(request, user, 'AuthenticationAndVerification/activate_email.html', "account activation test")
    context["verification"] = user.email
    return JsonResponse(context)

def blog_writers_profile(request, uname):
    context = {}
    user = User.objects.filter(username=uname).first()
    if user:
        context["fullname"] = user.first_name + " " + user.last_name
        context["username"] = user.username
        if user.profile_image:
            context["image_url"] = user.profile_image
        if user.about:
            context["about"] = user.about.paragraph 
            context["contact_email"] = user.about.contact_email
            context["instagram_profile"] = user.about.instagram_profile
            context["facebook_profile"] = user.about.facebook_profile
            context["website_link"] = user.about.website_link
            context["twitter_profile"] = user.about.twitter_profile

        written_by = user.username
        blogs = BlogModel.objects.filter(written_by=written_by)
        context["blogs"] = blogs
    else:
        context["user_not_found"] = True
    return render(request, 'AuthenticationAndVerification/show_profile.html', context)

def edit_profile(request):
    context = {}
    if "log_key" in request.session:
        user = User.objects.filter(username=request.session['log_key']).first()
        if user:
            context["fullname"] = user.first_name + " " + user.last_name
            context["username"] = user.username
            if user.profile_image:
                context["image_url"] = user.profile_image
            if user.about:
                context["about"] = user.about.paragraph
                context["contact_email"] = user.about.contact_email
                context["instagram_profile"] = user.about.instagram_profile
                context["facebook_profile"] = user.about.facebook_profile
                context["website_link"] = user.about.website_link
                context["twitter_profile"] = user.about.twitter_profile
    else:
        context["user_not_found"] = True
    return render(request, 'AuthenticationAndVerification/edit_profile.html', context)



