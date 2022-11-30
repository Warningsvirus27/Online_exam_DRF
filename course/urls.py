from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('test/', views.TestView.as_view()),
    path('test/<int:test_id>/', views.TestView.as_view()),
    path('mcq/', views.MCQView.as_view()),
    path('mcq/<int:mcq_id>/', views.MCQView.as_view()),
    path('get_course/', views.CourseGeneric.as_view()),
    path('get_test/<str:course_id>/', views.TestGeneric.as_view()),
    path('get_mcq/<str:test_id>/', views.MCQGeneric.as_view()),
    path('subscription/', views.SubscribedView.as_view()),
    path('subscription/<str:email>/', views.SubscribedView.as_view()),
    path('user_data/', views.user_data),
    path('evaluate/<str:test_id>/', views.evaluate),
    path('test_history/', views.TestHistoryGeneric.as_view()),
]