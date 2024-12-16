# movies/utils.py
import requests
from django.conf import settings

class TMDBApi:
    def __init__(self):
        self.base_url = settings.TMDB_API_BASE_URL
        self.headers = {
            'Authorization': f'Bearer {settings.TMDB_ACCESS_TOKEN}',
            'accept': 'application/json'
        }

    def get_popular_movies(self, page=1):
        """인기 영화 목록 가져오기"""
        url = f'{self.base_url}/movie/popular'
        params = {'language': 'ko-KR', 'page': page}
        response = requests.get(url, headers=self.headers, params=params)
        return response.json() if response.status_code == 200 else None

    def get_movie_details(self, movie_id):
        """영화 상세 정보 가져오기"""
        url = f'{self.base_url}/movie/{movie_id}'
        params = {'language': 'ko-KR'}
        response = requests.get(url, headers=self.headers, params=params)
        return response.json() if response.status_code == 200 else None

    def search_movies(self, query, page=1):
        """영화 검색"""
        url = f'{self.base_url}/search/movie'
        params = {
            'language': 'ko-KR',
            'query': query,
            'page': page
        }
        response = requests.get(url, headers=self.headers, params=params)
        return response.json() if response.status_code == 200 else None