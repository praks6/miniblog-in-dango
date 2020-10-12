from django.contrib import admin
from .models import Post,Categories,Author,Subscribe,Contact,profile,Comment,SubComment

# Register your models here.
admin.site.register(Post)
admin.site.register(Categories)
admin.site.register(Author)
admin.site.register(Subscribe)
admin.site.register(Contact)
admin.site.register(profile)
admin.site.register(Comment)
admin.site.register(SubComment)