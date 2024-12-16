<template>
  <div class="movie-detail-container">
    <!-- 영화 제목 -->
    <h1>{{ movie?.title || '영화 상세 정보' }}</h1>
    <div v-if="movie" class="movie-detail">
      <!-- 포스터 및 영화 정보 -->
      <div class="movie-content">
        <div class="movie-poster">
          <img :src="movie.poster_path" alt="Movie Poster" />
        </div>
        <div class="movie-info">
          <h2>{{ movie.title }}</h2>
          <p><strong>내용:</strong> {{ movie.content }}</p>
          <hr>
          <p><strong>연령 제한:</strong> {{ movie.age }}</p>
          <hr>
          <p><strong>상영 시간:</strong> {{ movie.runtime }} 분</p>
          <hr>
          <p><strong>평점:</strong> ⭐ {{ movie.rates }}</p>
          <hr>
          <!-- <p><strong>감독:</strong> {{ movie.director }}</p> -->
          <p><strong>감독:</strong> <DirectorFilmography :director="movie.director" /></p>
          <hr>
          <!-- 배우들 출력 -->
          <p><strong>배우:</strong>
            <!-- <span v-for="actor in movie.actors" :key="actor.id">{{ actor }}</span> -->
            <ActorFilmography
              v-for="(actor, index) in movie.actors.split(',').map((a) => a.trim())"
              :key="index"
              :actor="actor"
              :isLast="index === movie.actors.split(',').map((a) => a.trim()).length - 1"
            />
          </p>
        </div>
      </div>

      <!-- 댓글 섹션 -->
      <div class="movie-comments">
        <h3>댓글</h3>
        <div v-if="store.token">
          <CommentSystem 
            :movieId="route.params.id"
            :currentUsername="store.currentUser"
          />
        </div>
        <div v-else class="login-prompt">
          <p>댓글을 작성하려면 로그인이 필요합니다.</p>
          <router-link to="/login" class="login-button">로그인하기</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import { useAuthStore } from '../stores/auth';
import CommentSystem from '@/components/CommentSystem.vue';
import { useCounterStore } from '@/stores/counter';
import ActorFilmography from '@/components/ActorFilmography.vue';
import DirectorFilmography from '@/components/DirectorFilmography.vue'

// 현재 경로에서 ID 가져오기
const route = useRoute();
const movie = ref(null); // API에서 가져온 영화 정보를 저장
const authStore = useAuthStore();
const store = useCounterStore();
const movieId = ref(null); // 영화 ID 가져오기
const newComment = ref('');

// TMDb에서 프로필 사진을 가져올 URL 생성하는 함수
const getProfileImageUrl = (profilePath) => {
  const baseUrl = "https://image.tmdb.org/t/p/w500"; // TMDb 이미지 기본 URL
  return profilePath ? baseUrl + profilePath : '';
}

// API 호출로 영화 정보 가져오기
onMounted(() => {
  authStore.initializeAuth();
  axios.get(`http://localhost:8000/movies/${route.params.id}`)
    .then(response => {
      movie.value = response.data;
      // 영화 기록 추가
      store.addMovieRecord({
      id: movie.value.tmdb_id,
      genre: movie.value.genre,
      actors: movie.value.actors, // 영화의 장르 배열
      });
    })
    .catch(error => {
      console.error("영화 데이터를 가져오는 중 오류가 발생했습니다:", error);
    });
});
const addComment = () => {
  const comment = { id: Date.now(), text: newComment.value }; // 간단한 댓글 객체 생성
  store.saveComment(movieId.value, comment);
  const movie = store.movies.find((m) => m.tmdb_id === movieId.value);
  if (movie) {
    movie.review_count += 1; // 리뷰 개수 증가
  }
  newComment.value = '';
};

const deleteComment = (commentId) => {
  store.deleteComment(movieId.value, commentId);
  const movie = store.movies.find((m) => m.tmdb_id === movieId.value);
  if (movie) {
    movie.review_count -= 1; // 리뷰 개수 감소
  }
};


</script>

<style scoped>
.movie-detail-container {
  padding: 20px 20px;
  max-width: 1200px;
  margin: 0 auto;
  font-family: 'Arial', sans-serif;
  color: #333;
}

h1 {
  font-size: 3.5rem; /* 제목 크기 증가 */
  font-weight: bold;
  text-transform: uppercase;
  text-align: center;
  margin: 30px 0; /* 상하 여백 증가 */
  color: #e92964;
  position: relative;
}

h1::before {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  bottom: -12px;
  height: 5px;
  background: linear-gradient(to right, #e92964, #fcb045);
  transform: scaleX(1);
  transform-origin: left;
}

.movie-detail {
  display: flex;
  flex-direction: column;
  gap: 60px;
}

.movie-content {
  display: flex;
  gap: 40px;
  align-items: stretch; /* 높이를 맞추기 위해 stretch 사용 */
  border-bottom: 2px solid #eee;
  padding-bottom: 40px;
}

.movie-poster {
  flex: 0 0 400px; /* 포스터의 너비를 고정 (400px로 설정) */
}

.movie-poster img {
  width: 100%; /* 포스터가 div에 꽉 차도록 설정 */
  height: 100%; /* movie-info의 높이에 맞춰 크기 자동 조정 */
  border-radius: 15px;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.movie-info {
  flex: 1; /* movie-info는 남은 공간을 차지 */
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 15px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* 내용이 위 아래로 맞춰지도록 */
  line-height :1;
  font-size: 18px;
  font-family: 'Arial', sans-serif; /* 또는 'Pretendard', 'Noto Sans' 등 사용 가능 */

}


/* 제목은 굵게, 가운데 정렬 */
.movie-info h2 {
  font-size: 32px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 15px;
  color: white; /* 글자색 흰색으로 변경 */
  background-color: black; /* 배경색 검은색 추가 */
  padding: 10px; /* 텍스트 주변 여백 추가 */
  border-radius: 10px; /* 모서리를 둥글게 */
}

/* 나머지 텍스트에 고딕체 적용 */
.movie-info p {
  font-size: 18px;
  line-height: 1.4; /* 줄 간격 좁힘 */
  margin-bottom: 10px;
  font-family: 'Arial', sans-serif; /* 고딕체 적용 */
}

.movie-comments {
  padding: 40px;
  background-color: #ffffff;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  margin-top: 50px;
  border: 1px solid #f0f0f0;
}

/* 댓글 섹션 헤더 */
.movie-comments h3 {
  font-size: 32px;
  margin-bottom: 30px;
  color: #1a1a1a;
  font-weight: 600;
  text-align: center;
  position: relative;
  padding-bottom: 15px;
}

.movie-comments h3::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100px;
  height: 3px;
  background: linear-gradient(90deg, #1a1a1a, #4a4a4a);
  border-radius: 3px;
}

/* 댓글 시스템 컴포넌트 스타일링 */
/* 댓글과 대댓글 공통 컨테이너 */
:deep(.comment-item), :deep(.reply-item) {
  margin-bottom: 20px;
}

/* 대댓글 컨테이너 - 들여쓰기만 적용 */
:deep(.reply-item) {
  margin-left: 40px;
}

/* 댓글/대댓글 콘텐츠 공통 스타일 */
:deep(.comment-content) {
  padding: 24px;
  background-color: #1a1a1a;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  position: relative;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  border: 1px solid #2a2a2a;
  margin-bottom: 10px;
}
:deep(.reply-content) {
  padding: 24px;
  background-color: #1a1a1a;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  position: relative;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  border: 1px solid #2a2a2a;
  margin-bottom: 10px;
}

:deep(.comment-content:hover), :deep(.reply-content:hover) {
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.15);
}

/* 사용자명 스타일 */
:deep(.username) {
  color: #ffffff !important;
  font-weight: 600;
}

/* 댓글 작성자 스타일 */
:deep(.comment-author) {
  font-weight: 600;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 댓글 텍스트 */
:deep(.comment-text) {
  font-size: 15px;
  line-height: 1.6;
  color: #e0e0e0;
  margin-bottom: 12px;
}

/* 댓글 액션 버튼 컨테이너 */
:deep(.comment-actions) {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
  margin-top: 8px;
}

/* 수정/삭제 버튼 공통 스타일 */
:deep(.edit-button), :deep(.delete-button) {
  background-color: transparent;
  border: 1px solid #3a3a3a;
  padding: 4px 12px;
  font-size: 12px;
  font-weight: 500;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  height: 24px;
  line-height: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

/* 수정 버튼 */
:deep(.edit-button) {
  color: #ffffff;
}

:deep(.edit-button:hover) {
  background-color: #3a3a3a;
}

/* 삭제 버튼 */
:deep(.delete-button) {
  color: #ff4444;
}

:deep(.delete-button:hover) {
  background-color: #3a3a3a;
  color: #ff6666;
}

:deep(.comment-textarea), 
:deep(.reply-textarea) {
  background-color: #1a1a1a;
  color: #ffffff;  /* 텍스트 색상을 흰색으로 설정 */
  border: 1px solid #3a3a3a;
  border-radius: 8px;
  padding: 12px;
  width: 100%;
  min-height: 80px;
  margin-bottom: 12px;
  resize: vertical;
}

:deep(.comment-textarea:focus),
:deep(.reply-textarea:focus) {
  outline: none;
  border-color: #4a4a4a;
  box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.1);
}

:deep(.comment-textarea::placeholder),
:deep(.reply-textarea::placeholder) {
  color: #808080;  /* placeholder 텍스트 색상 설정 */
}

/* 답글 버튼 */
:deep(.reply-button) {
  background-color: transparent;
  color: #ffffff;
  border: 1px solid #3a3a3a;
  padding: 4px 12px;
  font-size: 12px;
  font-weight: 500;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  height: 24px;
  line-height: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

:deep(.reply-button:hover) {
  background-color: #3a3a3a;
}

/* 댓글 작성 버튼 */
:deep(.submit-button) {
  background-color: #1a1a1a;
  color: #ffffff;
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 500;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

:deep(.submit-button:hover) {
  background-color: #333333;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

:deep(.reply-input){
  color : white;
}
:deep(.action-button){
  padding : 10px;
  font-size : 13px;
}
/* 반응형 디자인 */
@media (max-width: 640px) {
  :deep(.comment-content), :deep(.reply-content) {
    padding: 16px;
  }
  
  :deep(.reply-item) {
    margin-left: 20px;
  }
  
  :deep(.comment-actions) {
    flex-wrap: wrap;
  }
  
  :deep(.reply-button),
  :deep(.edit-button),
  :deep(.delete-button) {
    flex: 0 1 auto;
    min-width: 60px;
  }
}
/* 감독 이미지 스타일 */
.director-img {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 10px;
  object-fit: cover;
}

/* 배우 이미지 스타일 */
.actor-img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 8px;
  object-fit: cover;
}
</style>
