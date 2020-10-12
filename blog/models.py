from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify

# Create your models here.
class profile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE,primary_key=True)
	image = models.ImageField(upload_to='profile_pic',null=True)

class Subscribe(models.Model):
    email = models.EmailField()
    def __str__(self):
        return self.email

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.user}'

class Categories(models.Model):
    title = models.CharField(max_length=30)
    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=50)
    overview = models.TextField()
    slug = models.SlugField(null=True,blank=True)
    body_text = RichTextUploadingField(null=True)
    time_upload = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author,on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to = 'thubnails')
    categories = models.ManyToManyField(Categories)
    publish = models.BooleanField()
    read = models.IntegerField(default=0)
    class meta:
        ordering = ['-pk']
    def __str__(self):
        return self.title

    def save(self,*args, **kwargs):
        self.slug = slugify(self.title)
        super(Post,self).save(*args, **kwargs)


class Contact(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField()
	mobile = models.CharField(max_length=12)
	message = models.TextField()
	time = models.DateTimeField(auto_now_add = True)
	def __str__(self):
		return self.name


class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	time = models.DateTimeField(auto_now_add=True)
	comm = models.TextField()

class SubComment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	time = models.DateTimeField(auto_now_add=True)
	comm = models.TextField()
	comment = models.ForeignKey(Comment, on_delete=models.CASCADE)