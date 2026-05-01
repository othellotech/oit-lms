from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('lesson/<int:id>/', views.lesson_detail, name='lesson_detail'),
    path('complete/<int:id>/', views.mark_complete, name='mark_complete'),
    path('playlist/<int:id>/', views.playlist_detail, name='playlist_detail'),
    path('lesson/<int:id>/', views.lesson_detail, name='lesson_detail'),
    path('complete/<int:id>/', views.mark_complete, name='mark_complete'),
    path('logout/', views.logout_view, name='logout'),
    path('run-migrations/', views.run_migrations),
]

