from django.contrib import admin
from models import ImageResipe, StepResipe, Category, Resipe
# Register your models here.

class ImageResipeInline(admin.StackedInline):
    model = ImageResipe

class StepResipeInline(admin.StackedInline):
    model = StepResipe

class ResipeAdmin(admin.ModelAdmin):
    inlines = [ImageResipeInline, StepResipeInline]
    prepopulated_fields = {'slug': ('title', 'id')} 

admin.register(Resipe, ResipeAdmin)
admin.register(Category)
