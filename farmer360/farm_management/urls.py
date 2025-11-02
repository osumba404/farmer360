from django.urls import path
from . import views
from .views_auth import signup

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('fields/', views.fields, name='fields'),
    path('field/<int:field_id>/', views.field_detail, name='field_detail'),
    path('analytics/', views.analytics, name='analytics'),
    path('advisories/', views.advisories, name='advisories'),
    path('profile/', views.profile, name='profile'),
    path('map/', views.map_view, name='map_view'),
    path('signup/', signup, name='signup'),
]