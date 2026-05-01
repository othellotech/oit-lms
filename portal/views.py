from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .forms import RegisterForm
from .models import (
    Profile,
    Course,
    Playlist,
    Lesson,
    CompletedLesson,
    AccessCode,
    PlaylistAccess
)


# -------------------
# REGISTER
# -------------------
def register_view(request):
    form = RegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        code = data['code_obj']

        user = User.objects.create_user(
            username=data['email'],
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )

        Profile.objects.create(user=user, course=code.course)

        code.is_used = True
        code.save()

        return redirect('login')

    return render(request, 'portal/register.html', {'form': form})


# -------------------
# LOGIN
# -------------------
def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST['email'],
            password=request.POST['password']
        )

        if user:
            login(request, user)
            return redirect('dashboard')

    return render(request, 'portal/login.html')


# -------------------
# DASHBOARD
# -------------------
def dashboard(request):
    profile = request.user.profile

    playlists = Playlist.objects.filter(
        course=profile.course
    ).order_by('order')

    total_lessons = Lesson.objects.filter(
        playlist__course=profile.course
    ).count()

    completed_lessons = CompletedLesson.objects.filter(
        user=request.user,
        lesson__playlist__course=profile.course
    ).count()

    progress = 0
    if total_lessons > 0:
        progress = int((completed_lessons / total_lessons) * 100)

    return render(request, 'portal/dashboard.html', {
        'playlists': playlists,
        'progress': progress
    })

# -------------------
# LESSON DETAIL
# -------------------
def lesson_detail(request, id):
    lesson = get_object_or_404(Lesson, id=id)

    lessons = Lesson.objects.filter(
        playlist=lesson.playlist
    ).order_by('order')

    # ✅ ADD THIS BLOCK (do NOT remove anything else)
    for l in lessons:
        l.completed = CompletedLesson.objects.filter(
            user=request.user,
            lesson=l
        ).exists()

    # current lesson completed?
    completed = CompletedLesson.objects.filter(
        user=request.user,
        lesson=lesson
    ).exists()

    next_lesson = lessons.filter(order__gt=lesson.order).first()
    prev_lesson = lessons.filter(order__lt=lesson.order).last()

    return render(request, 'portal/lesson.html', {
        'lesson': lesson,
        'lessons': lessons,
        'completed': completed,
        'next_lesson': next_lesson,
        'prev_lesson': prev_lesson
    })


# -------------------
# MARK COMPLETE
# -------------------
def mark_complete(request, id):
    lesson = get_object_or_404(Lesson, id=id)

    obj, created = CompletedLesson.objects.get_or_create(
        user=request.user,
        lesson=lesson
    )

    if not created:
        obj.delete()

    return redirect('lesson_detail', id=id)


# -------------------
# PLAYLIST DETAIL
# -------------------
def playlist_detail(request, id):
    playlist = get_object_or_404(Playlist, id=id)

    # CHECK IF USER ALREADY UNLOCKED THIS PLAYLIST
    already_unlocked = PlaylistAccess.objects.filter(
        user=request.user,
        playlist=playlist
    ).exists()

    if not already_unlocked:

        if request.method == "POST":
            code_input = request.POST.get("access_code")

            valid_code = AccessCode.objects.filter(
                code=code_input,
                course=playlist.course,
                is_used=False
            ).first()

            if valid_code:
                # SAVE PERMANENT UNLOCK (NO SESSION)
                PlaylistAccess.objects.create(
                    user=request.user,
                    playlist=playlist
                )

                # optional: keep your “one-time code rule”
                valid_code.is_used = True
                valid_code.save()

            else:
                return render(request, 'portal/access.html', {
                    'playlist': playlist,
                    'error': 'Invalid access code'
                })
        else:
            return render(request, 'portal/access.html', {
                'playlist': playlist
            })

    lessons = Lesson.objects.filter(
        playlist=playlist
    ).order_by('order')

    for l in lessons:
        l.completed = CompletedLesson.objects.filter(
            user=request.user,
            lesson=l
        ).exists()

    return render(request, 'portal/playlist.html', {
        'playlist': playlist,
        'lessons': lessons
    })




def logout_view(request):
    logout(request)
    return redirect('login')