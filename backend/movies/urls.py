from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('',views.movie_list,name = 'movie_list'),
    path('api/movies/', views.fetch_movies, name='fetch_movies'),
    path('<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('<int:movie_id>/comments/', views.manage_comment, name='add_comment'),
    path('<int:movie_id>/comments/<int:comment_id>/', 
         views.manage_comment, name='delete_comment'),
    path('<int:movie_id>/ratings/', views.manage_rating, name='manage_rating'),
    path('<int:movie_id>/likes/', views.movie_likes, name='movie_likes'),
    path('origin_movies/',views.get_tmdb_data, name = 'origin_movies'),
   
]