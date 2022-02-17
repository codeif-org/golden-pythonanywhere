from django.urls import path
from . import views

app_name = 'school'
urlpatterns = [
    path('', views.login, name='login'),
    path('logout', views.logout, name='logout'), 
    path('dashboard', views.dashboard, name='dashboard'),
    path('students', views.students, name='students'),
    path('sessions', views.sessions, name='sessions'),
    path('sessions/current-update/', views.updateCurrentSession, name='updateCurrentsession'),
    path('sessions/add-new/', views.addSession, name='addSession'),
    path('student/add', views.studentAdd, name='studentAdd'),
    path('student/edit/<int:student_id>', views.studentEdit, name='studentEdit'),
    path('studentoutline/<int:student_id>', views.studentoutline, name='studentoutline'),
    path('student/delete/', views.studentDelete, name='studentDelete'),
]
