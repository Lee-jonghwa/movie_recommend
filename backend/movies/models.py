from django.db import models
from django.conf import settings  # settings.AUTH_USER_MODEL 사용을 위해 추가

class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True, null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    director = models.CharField(max_length=100)
    actors = models.CharField(max_length=200)
    age = models.CharField(max_length=50)
    genre = models.CharField(max_length=100)
    runtime = models.IntegerField()
    rates = models.FloatField(default=0)
    is_prized = models.BooleanField(default=False)
    poster_path = models.URLField(max_length=500, null=True, blank=True)  # 포스터 URL 필드 추가

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.content[:50]

class MovieComment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

class MovieLike(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

# 평점 중개 테이블 직접 작성 : 평점 필드가 필요함
class Rate(models.Model):
    rate_user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='user_rated')
    rate_movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    # 사용자가 준 평점 : 추가 필드
    rate_score = models.FloatField()

class Genre(models.Model):
    id = models.IntegerField(primary_key=True) # 장르 id
    name = models.CharField(max_length=50) # 장르 name
