import imp
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_post, name="search_post"),
    path('all-posts/', views.all_posts, name="all_posts"),
    path('create-post/', views.create_post, name="create_posts"),
    path('show-post/<str:id>/', views.show_post, name="show_post"),
    path('update-post/<str:id>/', views.update_post, name="update_post"),
    path('delete-post/<str:id>/', views.delete_post, name="delete_post"),
    path('bitcoin-usd/', views.bitcoin_USD, name="bitcoin-usd"),
]