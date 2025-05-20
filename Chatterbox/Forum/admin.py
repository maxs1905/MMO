from django.contrib import admin
from .models import Category, User, Ads, Response

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_display_links = ('name',)
    search_fields = ('name',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Ads)
admin.site.register(Response)