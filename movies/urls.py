from django.urls import path
from . import views

urlpatterns =[
    path('',views.home_page, name='home_page'),
    path('about', views.about, name='about'),
    path('create/', views.create, name='create'),
    path('edit/<str:movie_id>', views.edit, name="edit")
]