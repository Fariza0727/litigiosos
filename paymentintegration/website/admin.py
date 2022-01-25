from django.contrib import admin

# Register your models here.
from paymentintegration.website.models import Content, ContentView, Rating, Commit

class ContentAdmin(admin.ModelAdmin):
    fields = ['title', 'description', 'voting', 'approved', 'category', 'username', 'surname']

admin.site.register(Content, ContentAdmin)