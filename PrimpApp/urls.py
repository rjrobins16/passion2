from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('log_out/', views.log_out, name="log_out"),
    path('home/', views.home, name='home'),
    path('log_in/', views.log_in, name="log_in"),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/',views.edit_profile, name = 'edit_profile'),
    path('update_location/',views.update_location, name = 'update_location')
]