from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('std_register/', views.std_register),
    path('login/', views.login_, name="login"),
    path('logout/', views.std_logout),
    path('user/', views.UserCRUDView.as_view()),
    path('user/<str:pk>/', views.UserCRUDView.as_view()),
    path('get_csrf/', views.CsrfTokenView.as_view()),
]
