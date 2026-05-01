from django.contrib import admin
from .models import Course, AccessCode, Profile, Playlist, Lesson, CompletedLesson

admin.site.register(Course)
admin.site.register(AccessCode)
admin.site.register(Profile)
admin.site.register(Playlist)
admin.site.register(Lesson)
admin.site.register(CompletedLesson)
