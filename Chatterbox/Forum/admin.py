from django.contrib import admin
from .models import Category, User, Ads, Response


admin.site.register(Category)
admin.site.register(User)
admin.site.register(Ads)
admin.site.register(Response)