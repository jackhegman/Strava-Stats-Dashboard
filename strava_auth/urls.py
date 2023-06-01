from django.urls import path

from strava_auth import views

urlpatterns = [
    path(r'', views.UserView.as_view(), name='authorized'),
    path(r'login/', views.StravaAuthView.as_view(), name='login'),
    path(r'logout/', views.UserLogoutView.as_view(), name='logout'),
]
