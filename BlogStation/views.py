from django.shortcuts import render, redirect
from AuthenticationAndVerification.models import *
from .models import TagModel, BlogModel, CommentModel

# Create your views here.

def index(request):
        context = {}
        context["index"] = True
        if "log_key" in request.session:
                context["loggedin"] = True
                user = User.objects.filter(username=request.session["log_key"]).first()
                context["id"] = user.id
                context["username"] = user.username
        return render(request, 'BlogStation/index.html', context)

def main_blog_page(request):
        context = {}
        context["index"] = True
        if "log_key" in request.session:
                context["loggedin"] = True
                user = User.objects.filter(username=request.session["log_key"]).first()
                context["id"] = user.id
        return render(request, 'BlogStation/main_blog_page.html', context)

def blog_view(request, id):
        context = {}
        return render(request, 'BlogStation/blog_view.html', context)

def blog_writers_dashboard(request):
        context = {}
        context["dashboard"] = True
        if "log_key" in request.session:
                context["loggedin"] = True
                user = User.objects.filter(username=request.session["log_key"]).first()
                context["id"] = user.id
        else:
                return redirect('login')
        return render(request, 'BlogStation/blog_writers_dashboard.html', context)

def create_blog(request):
        context = {}
        if "log_key" in request.session:
                context["authenticated"] = True
                user = User.objects.all().filter(username=request.session['log_key']).first()
                if request.method == 'GET':
                        tags = TagModel.objects.all()
                        context["tags"] = tags
                        context["languages"] = ['']

        return render(request, 'BlogStation/create_blog.html', context)

def edit_blog(request, id):
        context = {}
        return render(request, 'BlogStation/edit_blog.html', context)

def blog_preview(request):
        context = {}
        return render(request, 'BlogStation/blog_preview.html', context)

def save_draft(request):
        context = {}
        return render(request, 'BlogStation/save_draft.html', context)

def blog_search_bar(request):
        pass

def tag_blogs(request, name):
        context = {}
        return render(request, 'BlogStation/blog_tag_page.html', context)


