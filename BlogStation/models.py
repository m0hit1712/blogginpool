from ckeditor.fields import RichTextField
from django.db import models

# Create your models here.

class TagModel(models.Model):
        name = models.TextField(max_length=15)

        def __str__(self):
                return self.name

class BlogModel(models.Model):
        heading = models.TextField(max_length=80)
        description = models.TextField(max_length=500, null=True ,blank=True)
        body = RichTextField(blank=True)
        written_by = models.CharField(max_length=30)
        date = models.DateTimeField(auto_now_add=True)
        last_modified = models.DateTimeField(auto_now=True)
        likes = models.IntegerField(blank=True, default=0)
        liked_by = models.TextField(blank=True)
        views = models.IntegerField(blank=True, default=0)
        comments = models.IntegerField(blank=True, default=0)
        draft = models.BooleanField(default=True, null=True, blank=True)
        banner_image_url = models.TextField(null=True, blank=True)
        language_code = models.CharField(max_length=10, null=True, blank=True)
        tag_model = models.ManyToManyField(TagModel)

        def __str__(self):
                return self.heading

        class Meta:
                ordering = ["date"]


class CommentModel(models.Model):
        content = models.TextField(max_length=200)
        by = models.CharField(max_length=15)
        date = models.DateTimeField(auto_now_add=True)
        likes = models.IntegerField(blank=True, default=0)
        blog_name = models.ForeignKey(BlogModel, on_delete=models.CASCADE)

        def __str__(self):
                return self.blog_name.heading



