from django.urls import path
from . import views

app_name = 'reports'
urlpatterns = [
    path('generate', views.generate, name='generate'),
    path('api/day/generate/', views.dayReportAPI, name='dayReportAPI'), 
    path('api/date/generate/', views.dateReportAPI, name='dateReportAPI'),
    path('api/date-with-detail/generate/', views.dateWithDReportAPI, name='dateWithDReportAPI'),  
    path('defaulters', views.defaulters, name='defaulters'), 
    path('defaulters-notice', views.defaultersNotice, name='defaultersNotice'), 
    path('api/student-cumulative/', views.studCumulative, name='studCumulative'),
    path('backup/', views.backup, name='backup'), 
]