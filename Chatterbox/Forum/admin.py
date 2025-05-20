from django.contrib import admin
from .models import Category, User, Ads, Response

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Что отображать в списке
    search_fields = ('name',)  # Поиск по названию

admin.site.register(Category)
admin.site.register(Ads)
admin.site.register(Response)