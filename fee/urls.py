from django.urls import path
from . import views

app_name = 'fee'
urlpatterns = [
    path('select-class/', views.selectClass, name='selectClass'),
    path('select-month/<int:class_id>', views.selectMonth, name='selectMonth'),
    path('feeEdit/<int:clas_id>/<int:month_id>', views.feeEdit, name='feeEdit'),
    path('structUpdate/', views.structUpdate, name='structUpdate'),
    path('submit/', views.feeSubmit, name='feeSubmit'),
    path('api/student_details/', views.studentDetailsAPI, name='studentDetailsAPI'),
    path('concession/', views.feeConcession, name='feeConcession'),
    path('misc/', views.misc, name='misc'),
    path('misc/delete/', views.miscDelete, name='miscDelete'),
    path('delete/', views.feeDelete, name='feeDelete'),
    # path('dashboard', views.dashboard, name='dashboard')
]
