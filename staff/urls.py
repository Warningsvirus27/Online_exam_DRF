from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('login/', views.staff_login),
    path('staff_register/', views.register),
    path('disable_std/', views.DisableStudentView.as_view()),
    path('course/', views.CourseView.as_view()),
    path('course/<int:course_id>/', views.CourseView.as_view()),
    path('subscription_number/', views.subscription_number),
    path('search/', views.search),
]
