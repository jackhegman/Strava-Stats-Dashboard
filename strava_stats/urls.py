from django.urls import path

from strava_stats import views

urlpatterns = [
    path('rides/', views.StravaStatsView.as_view(), {'page': None}, name='rides'),
]