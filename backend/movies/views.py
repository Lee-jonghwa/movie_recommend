from rest_framework import status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import render

from django.shortcuts import get_object_or_404
from django.db.models import Avg
from .models import Movie, Comment, Rate, MovieLike, MovieComment
from .serializers import (
    MovieListSerializer, MovieDetailSerializer, CommentSerializer,
    MovieRatingSerializer, MovieLikeSerializer
)
from django.contrib.auth import get_user_model  # 추가

from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from django.contrib.auth.decorators import login_required
from django.conf import settings
import requests
from django.core.cache import cache
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import time
from django.http import JsonResponse


User = get_user_model()
logger = logging.getLogger(__name__)

TMDB_API_KEY = settings.TMDB_API_KEY
TMDB_BASE_URL = "https://api.themoviedb.org/3"

def fetch_movies(request):
    sort = request.GET.get('sort', None)  # 정렬 기준 쿼리 파라미터 가져오기
    movies = Movie.objects.all()  # DB에서 모든 영화 가져오기

    # 정렬 적용
    if sort == 'latest':  # 최신순 정렬
        movies = movies.order_by('-release_date')
    elif sort == 'old':  # 과거순 정렬
        movies = movies.order_by('release_date')
    elif sort == 'rating':  # 평점순 정렬
        movies = movies.order_by('-rates')
    elif sort == 'title':  # 제목순 정렬
        movies = movies.order_by('title')

    # 필요한 데이터를 JSON으로 변환
    movies_data = [
        {
            "id": movie.tmdb_id,
            "title": movie.title,
            "poster_path": movie.poster_path,
            "content": movie.content,
            "runtime" : movie.runtime,
            "age" : movie.age,
            "actors" : movie.actors,
            "genre" : movie.genre,
        }
        for movie in movies
    ]

    return JsonResponse({"movies": movies_data})

def get_tmdb_data(endpoint, params=None):
    """TMDB API에서 데이터를 가져오는 헬퍼 함수"""
    if params is None:
        params = {}
    
    params['api_key'] = TMDB_API_KEY
    params['language'] = 'ko-KR'
    
    try:
        response = requests.get(f"{TMDB_BASE_URL}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
       
    except requests.RequestException as e:
        logger.error(f"TMDB API 요청 실패: {str(e)}")
        return None
def fetch_multiple_pages(endpoint, base_params, max_pages=5):
    """여러 페이지의 영화 데이터를 병렬로 가져오는 함수"""
    all_results = []
    first_page = get_tmdb_data(endpoint, {**base_params, 'page': 1})
    
    if not first_page:
        return []
    
    total_pages = min(first_page['total_pages'], max_pages)
    all_results.extend(first_page['results'])

    def fetch_page(page_num):
        page_data = get_tmdb_data(endpoint, {**base_params, 'page': page_num})
        return page_data['results'] if page_data else []

    # 나머지 페이지들을 병렬로 가져오기
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_page = {
            executor.submit(fetch_page, page): page 
            for page in range(2, total_pages + 1)
        }
        
        for future in future_to_page:
            results = future.result()
            all_results.extend(results)
            time.sleep(0.25)  # TMDB API 속도 제한 준수

    return all_results

def get_image_configuration():
    """TMDB API에서 이미지 설정 가져오기"""
    configuration = get_tmdb_data("configuration")
    if configuration and 'images' in configuration:
        base_url = configuration['images']['base_url']
        file_sizes = configuration['images']['poster_sizes']  # 예: w500, w780, original 등
        return base_url, file_sizes
    return None, None


def save_movie_to_db(tmdb_movie):
    """TMDB 영화 데이터를 DB에 저장"""
    try:
        # 이미지 설정 가져오기
        base_url, file_sizes = get_image_configuration()
        if not base_url:
            raise Exception("TMDB 이미지 설정을 가져올 수 없습니다.")

        # 포스터 경로 처리
        poster_path = tmdb_movie.get('poster_path')
        full_poster_url = None
        if poster_path:
            # 기본 이미지 크기(w500)을 사용하여 포스터 URL 생성
            full_poster_url = f"{base_url}t/p/w500{poster_path}"
        # 장르 정보 가져오기
        genres = []
        if 'genre_ids' in tmdb_movie:
            # 장르 ID를 이름으로 변환
            genre_data = get_tmdb_data("genre/movie/list")
            if genre_data:
                genre_map = {g['id']: g['name'] for g in genre_data['genres']}
                genres = [genre_map[gid] for gid in tmdb_movie['genre_ids'] if gid in genre_map]
        elif 'genres' in tmdb_movie:
            genres = [g['name'] for g in tmdb_movie['genres']]

        # 감독 정보 가져오기
        credits = get_tmdb_data(f"movie/{tmdb_movie['id']}/credits")
        director = "알 수 없음"
        actors = "알 수 없음"
        if credits:
            # 감독 찾기
            directors = [crew['name'] for crew in credits.get('crew', []) if crew['job'] == 'Director']
            if directors:
                director = directors[0]

            # 배우 찾기 (상위 3명)
            cast = credits.get('cast', [])
            if cast:
                actors = ', '.join([actor['name'] for actor in cast[:3]])

        # 출시일 처리
        release_date = None
        if tmdb_movie.get('release_date'):
            try:
                release_date = datetime.strptime(tmdb_movie['release_date'], '%Y-%m-%d').date()
            except ValueError:
                pass

        # 연령 등급 정보 가져오기 (한국 기준)
        release_dates = get_tmdb_data(f"movie/{tmdb_movie['id']}/release_dates")
        age = "전체"
        if release_dates:
            results = release_dates.get('results', [])
            for entry in results:
                if entry['iso_3166_1'] == 'KR':  # 한국 연령 등급
                    release_info = entry.get('release_dates', [])
                    if release_info:
                        certification = release_info[0].get('certification', '')
                        if certification:  # 등급이 존재하면 설정
                            age = certification
                            break

        poster_path = tmdb_movie.get('poster_path')
        full_poster_url = None
        if poster_path:
            full_poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
        # 영화 데이터 저장 또는 업데이트
        movie, created = Movie.objects.update_or_create(
            tmdb_id=tmdb_movie['id'],
            defaults={
                'title': tmdb_movie['title'],
                'content': tmdb_movie.get('overview', ''),
                'director': director,
                'actors': actors,
                'age': age,  # 반영된 연령 제한
                'genre': ', '.join(genres) if genres else '기타',
                'runtime': tmdb_movie.get('runtime', 0) or 0,
                'rates': tmdb_movie.get('vote_average', 0),
                'poster_path': full_poster_url,  # 포스터 URL 추가

                'is_prized': False  # 기본값
            }
        )
        return movie
    except Exception as e:
        logger.error(f"영화 저장 중 오류 발생: {str(e)}")
        return None

def convert_tmdb_movie(tmdb_movie):
    """TMDB 영화 데이터를 우리 모델 형식으로 변환"""
    poster_path = tmdb_movie.get('poster_path')
    full_poster_url = None
    if poster_path:
        full_poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
    return {
        'tmdb_id': tmdb_movie['id'],
        'title': tmdb_movie['title'],
        'overview': tmdb_movie['overview'],
        'poster_path': f"https://image.tmdb.org/t/p/w500{tmdb_movie['poster_path']}" if tmdb_movie.get('poster_path') else None,
        'release_date': tmdb_movie.get('release_date'),
        'vote_average': tmdb_movie.get('vote_average', 0),
        'genre_ids': tmdb_movie.get('genre_ids', []),
    }

@api_view(['GET'])
def movie_list(request):
    """향상된 영화 목록 API"""
    genre = request.query_params.get('genre')
    search = request.query_params.get('search')
    sort_by = request.query_params.get('sort_by', 'popularity.desc')
    max_pages = int(request.query_params.get('max_pages', 10))  # 최대 페이지 수 제한
    
    # 기본 매개변수 설정
    if search:
        endpoint = "search/movie"
        base_params = {'query': search}
    else:
        endpoint = "discover/movie"
        base_params = {
            'sort_by': sort_by,
            'with_genres': genre
        }

    # 여러 페이지의 영화 데이터 가져오기
    tmdb_movies = fetch_multiple_pages(endpoint, base_params, max_pages)
    
    if not tmdb_movies:
        return Response(
            {'error': 'Failed to fetch movies'}, 
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

    # 영화 데이터를 DB에 저장하고 응답 데이터 준비
    movies_data = []
    for tmdb_movie in tmdb_movies:
        movie = save_movie_to_db(tmdb_movie)
        if movie:
            serializer = MovieListSerializer(movie)
            movies_data.append(serializer.data)

    response_data = {
        'results': movies_data,
        'total_results': len(movies_data),
        'pages_fetched': min(max_pages, len(movies_data) // 20 + 1)
    }

    return Response(response_data)

@api_view(['GET'])
def movie_detail(request, movie_id):
    """영화 상세 정보를 가져오고 DB에 저장"""
    # TMDB에서 영화 상세 정보 가져오기
    tmdb_data = get_tmdb_data(f"movie/{movie_id}")
    
    if not tmdb_data:
        return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

    # 추가 정보 가져오기
    credits = get_tmdb_data(f"movie/{movie_id}/credits")
    videos = get_tmdb_data(f"movie/{movie_id}/videos")

    # DB에 영화 정보 저장
    movie = save_movie_to_db(tmdb_data)
    
    if not movie:
        return Response({'error': 'Failed to save movie'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 영화 정보에 추가 데이터 포함
    movie_data = MovieDetailSerializer(movie).data
    movie_data.update({
        'cast': credits.get('cast', [])[:5] if credits else [],
        'director': next((crew['name'] for crew in credits.get('crew', []) if crew['job'] == 'Director'), None) if credits else None,
        'videos': videos.get('results', []) if videos else [],
        'likes_count': MovieLike.objects.filter(movie=movie).count(),
        'comments_count': MovieComment.objects.filter(movie=movie).count(),
        'poster_path': movie.poster_path  # 포스터 경로 추가

    })

    return Response(movie_data)

@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated, IsOwnerOrReadOnly])
@login_required
def manage_comment(request, movie_id, comment_id=None):
    """영화 댓글 추가/삭제"""
    # TMDB에서 영화 존재 여부 확인
    tmdb_data = get_tmdb_data(f"movie/{movie_id}")
    if not tmdb_data:
        return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
    poster_path = tmdb_data.get('poster_path')
    full_poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
    # 로컬 DB에 영화 정보가 없다면 생성
    movie, created = Movie.objects.get_or_create(
        tmdb_id=movie_id,
        defaults={
            'title': tmdb_data['title'],
            'overview': tmdb_data['overview'],
            'poster_path': full_poster_url,
            'release_date': tmdb_data.get('release_date')
        }
    )
    
    if request.method == 'POST':
        comment_data = {
            'content': request.data.get('content'),
            'user': request.user.id
        }
        
        comment_serializer = CommentSerializer(data=comment_data)
        if comment_serializer.is_valid():
            comment = comment_serializer.save()
            MovieComment.objects.create(movie=movie, comment=comment)
            return Response(comment_serializer.data, status=status.HTTP_201_CREATED)
        return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(['POST', 'PUT'])
@permission_classes([IsAuthenticated])
@login_required
def manage_rating(request, movie_id):
    """영화 평점 추가/수정"""
    # TMDB에서 영화 존재 여부 확인
    tmdb_data = get_tmdb_data(f"movie/{movie_id}")
    if not tmdb_data:
        return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

    # 로컬 DB에 영화 정보가 없다면 생성
    movie, created = Movie.objects.get_or_create(
        tmdb_id=movie_id,
        defaults={
            'title': tmdb_data['title'],
            'overview': tmdb_data['overview'],
            'poster_path': tmdb_data.get('poster_path'),
            'release_date': tmdb_data.get('release_date')
        }
    )
    
    try:
        rating = Rate.objects.get(movie=movie, user=request.user)
        serializer = MovieRatingSerializer(rating, data={
            'movie': movie.id,
            'user': request.user.id,
            'rate': request.data.get('rate')
        })
    except Rate.DoesNotExist:
        serializer = MovieRatingSerializer(data={
            'movie': movie.id,
            'user': request.user.id,
            'rate': request.data.get('rate')
        })
    
    if serializer.is_valid():
        serializer.save()
        # 영화의 평균 평점 업데이트
        avg_rating = Rate.objects.filter(movie=movie).aggregate(Avg('rate'))['rate__avg']
        movie.rates = round(avg_rating, 1) if avg_rating else 0
        movie.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
@login_required
def movie_likes(request, movie_id):
    """영화 좋아요 관리"""
    # TMDB에서 영화 존재 여부 확인
    tmdb_data = get_tmdb_data(f"movie/{movie_id}")
    if not tmdb_data:
        return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

    # 로컬 DB에 영화 정보가 없다면 생성
    movie, created = Movie.objects.get_or_create(
        tmdb_id=movie_id,
        defaults={
            'title': tmdb_data['title'],
            'overview': tmdb_data['overview'],
            'poster_path': tmdb_data.get('poster_path'),
            'release_date': tmdb_data.get('release_date')
        }
    )
    
    if request.method == 'GET':
        likes_count = MovieLike.objects.filter(movie=movie).count()
        return Response({
            'movie_id': movie_id, 
            'likes': likes_count,
            'user_has_liked': MovieLike.objects.filter(
                user=request.user, 
                movie=movie
            ).exists()
        })
    
    elif request.method == 'POST':
        if MovieLike.objects.filter(user=request.user, movie=movie).exists():
            return Response(
                {'message': 'You already liked this movie!'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        like = MovieLike.objects.create(user=request.user, movie=movie)
        serializer = MovieLikeSerializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    elif request.method == 'DELETE':
        like = MovieLike.objects.filter(user=request.user, movie=movie)
        if like.exists():
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'message': 'You haven\'t liked this movie!'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
# @api_view(['GET'])
# def origin_movies(request):
#     mv_list = get_tmdb_data(3, params=None)
#     return mv_list

def index(request):
    return render(request, 'movies/index.html')