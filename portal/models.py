from django.db import models
from django.contrib.auth.models import User


# -------------------
# COURSE
# -------------------
class Course(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


# -------------------
# ACCESS CODE
# -------------------
class AccessCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    is_used = models.BooleanField(default=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.code
    
class PlaylistAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist = models.ForeignKey('Playlist', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'playlist')


# -------------------
# USER PROFILE
# -------------------
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username


# -------------------
# PLAYLIST (Course Sections)
# -------------------
class Playlist(models.Model):
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    unlock_code = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.title

#lesson
class Lesson(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    video_url = models.URLField()
    note = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


# -------------------
# COMPLETED LESSONS
# -------------------
class CompletedLesson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'lesson')