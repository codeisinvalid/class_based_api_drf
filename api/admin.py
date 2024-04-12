from django.contrib import admin
from .models import Student

class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'grade', 'roll', 'city')
    list_display_links = ('name',)

admin.site.register(Student, StudentAdmin)