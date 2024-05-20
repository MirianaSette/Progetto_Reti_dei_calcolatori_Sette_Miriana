from django.contrib import admin
from .models import User, RssFeed, News
# Register your models here.


admin.site.register(User)
admin.site.register(RssFeed)
admin.site.register(News)