from django.contrib import admin
from .models import (
    Area, Region, Semester, University, Chapter, College, Member,
    Officer
)

# Register your models here.
admin.site.register(Area)
admin.site.register(Region)
admin.site.register(University)
admin.site.register(Chapter)
admin.site.register(College)
admin.site.register(Member)
admin.site.register(Semester)
admin.site.register(Officer)
