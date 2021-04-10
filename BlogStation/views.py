from django.shortcuts import render, redirect
from AuthenticationAndVerification.models import User
from .models import TagModel, BlogModel, CommentModel
from django.http import JsonResponse, HttpResponse
from django.utils import timezone


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

def blog_view(request, id_):
        context = {}
        if "log_key" in request.session:
                context["authenticated"] = True

        blog = BlogModel.objects.all().filter(id=int(id_)).first()
        context["blog"] = blog
        return render(request, 'BlogStation/blog_view.html', context)

def blog_writers_dashboard(request):
        context = {}
        context["dashboard"] = True
        if "log_key" in request.session:
                if "delete_this" in request.GET:
                        print("deletion called")
                        data = {"deleted": True}
                        blog = BlogModel.objects.filter(id=request.GET["delete_this"]).first()
                        blog.delete()
                        return JsonResponse(data)
                context["loggedin"] = True
                user = User.objects.filter(username=request.session["log_key"]).first()
                context["id"] = user.id
                written_by = user.username
                blogs = BlogModel.objects.filter(written_by=written_by, draft=False)
                drafts = BlogModel.objects.filter(written_by=written_by, draft=True)
                context["user_email"] = user.email
                context["blogs"] = blogs
                context["drafts"] = drafts
                if not user.email_verified:
                        context["email_not_verified"] = True
        else:
                return redirect('login')
        return render(request, 'BlogStation/blog_writers_dashboard.html', context)

def create_blog(request):
        context = {}
        if "log_key" in request.session:
                context["loggedin"] = True
                user = User.objects.all().filter(username=request.session['log_key']).first()
                context["id"] = user.id
                if request.method == 'GET':
                        tags = TagModel.objects.all()
                        context["tags"] = tags
                        context["languages"] = ['']
                        if not user.email_verified:
                                context["email_not_verified"] = True
                
                if request.method == 'POST':
                        image_url = request.POST["banner_image_url"]
                        heading = request.POST["blog_heading"]
                        body = request.POST["editor"]
                        description_came = request.POST["description"]
                        written_by = user.username
                        tags_came = tags_came = request.POST["tags"].split(',')
                        tags = [tag.name for tag in TagModel.objects.all()]

                        blog_model = BlogModel.objects.create(description=description_came, draft=False, heading=heading, body=body, date=timezone.now(), written_by=written_by, banner_image_url=image_url)

                        for tag_came in tags_came:
                                if tag_came not in tags and tag_came is not '':
                                        tag_obj = TagModel.objects.create(name=tag_came)
                                        blog_model.tag_model.add(tag_obj)
                                else:
                                        tag_obj = TagModel.objects.filter(name=tag_came).first()
                                        blog_model.tag_model.add(tag_obj)


        return render(request, 'BlogStation/create_blog.html', context)

def save_draft(request):
        user = User.objects.all().filter(username=request.session['log_key']).first()
        tags_came = request.GET["tags"].split(',')
        content_came = request.GET["editor"]
        heading_came = request.GET["heading"]
        img_url = request.GET['img_url']
        description_came = request.GET["description"]

        tags = [tag.name for tag in TagModel.objects.all()]

        written_by = user.username

        if "existing_blog" in request.GET:
                id_ = int(request.GET["blog_id"])
                blog_model = BlogModel.objects.filter(id=id_).first()
                blog_model.heading = heading_came
                blog_model.body = content_came
                blog_model.date = timezone.now()
                blog_model.written_by = written_by
                blog_model.description = description_came
                blog_model.banner_image_url = img_url
                blog_model.tag_model.clear()
        else:
                blog_model = BlogModel.objects.create(description=description_came,heading=heading_came, body=content_came, date=timezone.now(), written_by=written_by, banner_image_url=img_url)

        for tag_came in tags_came:
                if tag_came not in tags and tag_came is not '':
                        tag_obj = TagModel.objects.create(name=tag_came)
                        blog_model.tag_model.add(tag_obj)
                else:
                        tag_obj = TagModel.objects.filter(name=tag_came).first()
                        blog_model.tag_model.add(tag_obj)

        blog_model.save()
        return JsonResponse({"saved": True, "id": blog_model.id})

def edit_blog(request, id_):
        context = {}
        if "log_key" in request.session:
                user = User.objects.all().filter(username=request.session['log_key']).first()
                context["authenticated"] = True
                if request.method == "GET":
                        tags = TagModel.objects.all()
                        context["tags"] = tags
                        written_by = user.username
                        blog = BlogModel.objects.all().filter(id=id_).first()
                        if blog.written_by == written_by:
                                context["blog"] = blog

                if request.method == 'POST':
                        image_url = request.POST["banner_image_url"]
                        heading = request.POST["blog_heading"]
                        body = request.POST["editor"]
                        description_came = request.POST["description"]
                        written_by = user.username
                        tags_came = tags_came = request.POST["tags"].split(',')
                        tags = [tag.name for tag in TagModel.objects.all()]

                        blog_model = BlogModel.objects.filter(id=id_).first()
                        blog_model.heading = heading
                        blog_model.body = body
                        blog_model.description = description_came
                        blog_model.date = timezone.now()
                        blog_model.written_by = written_by
                        blog_model.banner_image_url = image_url
                        blog_model.tag_model.clear()
                        blog_model.draft = False

                        for tag_came in tags_came:
                                if tag_came not in tags and tag_came is not '':
                                        tag_obj = TagModel.objects.create(name=tag_came)
                                        blog_model.tag_model.add(tag_obj)
                                else:
                                        tag_obj = TagModel.objects.filter(name=tag_came).first()
                                        blog_model.tag_model.add(tag_obj)
                        blog_model.save()
                        return redirect('writers_dashboard')

        return render(request, 'BlogStation/edit_blog.html', context)

def blog_preview(request, id_):
        context = {}
        if "log_key" in request.session:
                context["authenticated"] = True

        blog = BlogModel.objects.all().filter(id=int(id_)).first()
        context["blog"] = blog
        return render(request, 'BlogStation/blog_preview.html', context)



def blog_search_bar(request):
        pass

def tag_blogs(request, name):
        context = {}
        return render(request, 'BlogStation/blog_tag_page.html', context)

from blogthat import firebase

def upload_image(request):
        image = 'static/images/guide.png'
        url = firebase.upload_to_firebase(image)
        return HttpResponse(url)

