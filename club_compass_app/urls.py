from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from club_compass import settings


urlpatterns = [
    path('', views.index, name='index'),
    # Calls a provided logout method to log the user out and returns to the home screen
    # The LOGOUT_REDIRECT_URL is set in club_compass/settings.py at the bottom
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
]