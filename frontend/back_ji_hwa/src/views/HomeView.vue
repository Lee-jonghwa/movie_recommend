<template>
  <div>
    <h3 class ="logo1">당신이 찾던 영화,</h3><h1 class="logo">CINE FOR YOU</h1>
    
    <div>
        <div class="drop d-flex justify-content-evenly align-items-center" style="font-weight:bold; margin-top:20px; margin-bottom:20px; border: 1px solid ;">
          <button class="cta" @click="sortBtn(1, '인기순')">인기순</button>
          <button class="cta" @click="sortBtn(2, '최신순')">최신순</button>
          <button class="cta" @click="sortByReviews">리뷰 많은순</button>
          <button class="cta " @click="sortBtn(4, '평점순')">평점순</button>
          <div class="btn-group" >
            <button type="button" class="dropdown-toggle cta" data-bs-toggle="dropdown" aria-expanded="false">
              장르별
            </button>
            <ul style="border: 1px solid #e92964;" class="dropdown-menu">
              <li><a class="dropdown-item" @click="sortBtn(12, '모험')">모험</a></li>
              <li><a class="dropdown-item" @click="sortBtn(14, '판타지')">판타지</a></li>
              <li><a class="dropdown-item" @click="sortBtn(16, '애니메이션')">애니메이션</a></li>
              <li><a class="dropdown-item" @click="sortBtn(18, '드라마')">드라마</a></li>
              <li><a class="dropdown-item" @click="sortBtn(27, '공포')">공포</a></li>
              <li><a class="dropdown-item" @click="sortBtn(28, '액션')">액션</a></li>
              <li><a class="dropdown-item" @click="sortBtn(35, '코미디')">코미디</a></li>
              <li><a class="dropdown-item" @click="sortBtn(36, '역사')">역사</a></li>
              <li><a class="dropdown-item" @click="sortBtn(37, '서부')">서부</a></li>
              <li><a class="dropdown-item" @click="sortBtn(53, '스릴러')">스릴러</a></li>
              <li><a class="dropdown-item" @click="sortBtn(80, '범죄')">범죄</a></li>
              <li><a class="dropdown-item" @click="sortBtn(99, '다큐멘터리')">다큐멘터리</a></li>
              <li><a class="dropdown-item" @click="sortBtn(878, 'SF')">SF</a></li>
              <li><a class="dropdown-item" @click="sortBtn(9648, '미스터리')">미스터리</a></li>
              <li><a class="dropdown-item" @click="sortBtn(10402, '음악')">음악</a></li>
              <li><a class="dropdown-item" @click="sortBtn(10749, '로맨스')">로맨스</a></li>
              <li><a class="dropdown-item" @click="sortBtn(10751, '가족')">가족</a></li>
              <li><a class="dropdown-item" @click="sortBtn(10752, '전쟁')">전쟁</a></li>
              <li><a class="dropdown-item" @click="sortBtn(10770, 'TV 영화')">TV 영화</a></li>
            </ul>
            
          </div>
        </div>
      </div>
    
    
  <!-- 영화 리스트 렌더링 -->
  <div class="movie-list">
      <div v-for="movie in filteredMovies" :key="movie.id" class="movie-item">
        <!-- 영화 포스터 및 제목을 클릭하면 상세 페이지로 이동 -->
        <router-link :to="`/movies/${movie.id}`">
          <img 
            :src="movie.poster_path" 
            :alt="movie.title" 
            class="movie-poster" 
          />
        </router-link>
        <router-link :to="`/movies/${movie.id}`">
          <h3>{{ movie.title }}</h3>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import MovieList from '@/components/MovieList.vue';
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'; // URL 쿼리 파라미터를 가져오기 위해 사용

import axios from 'axios'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const route = useRoute(); // 현재 URL의 쿼리 파라미터를 읽어오는 데 사용

const movies = ref([]) // 영화 목록을 저장할 변수
const currentSort = ref('') // 현재 정렬 기준
const searchQuery = computed(() => route.query.search || ''); // URL 쿼리에서 검색어 가져오기
const selectedGenre = ref(""); // 선택된 장르

// 영화 데이터를 가져오는 함수
const fetchMovies = async (sortCriteria = '') => {
    try {
        const response = await axios.get(`http://localhost:8000/movies/api/movies/`);
        movies.value = response.data.movies
        store.movies = response.data.movies
        // console.log(response.data.movies[1])
    } catch (error) {
        console.error("영화 데이터를 불러오는 중 오류가 발생했습니다:", error)
    }
}
// 검색어에 맞는 영화를 필터링하는 computed 속성
const filteredMovies = computed(() => {
  if (!searchQuery.value) return movies.value;
  return movies.value.filter(movie => 
    movie.title.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});
const sortByReviews = () => {
  store.sortMoviesByReviews(); // 리뷰 정렬 메서드 호출
};
// 정렬 버튼 클릭 시 호출되는 함수
const sortBtn = (criteria, name) => {
    currentSort.value = name // 정렬 기준 저장
    fetchMovies(criteria) // 영화 데이터 다시 요청
}

onMounted(() => {
    fetchMovies() // 페이지가 로드될 때 영화 데이터 요청
})
</script>

<style scoped>

.cta {
  font-size: 22px;
  text-align: center; /* 텍스트를 중앙 정렬 */
  text-decoration: none;
  text-transform: uppercase;
  color: #fff; /* 텍스트 색상: 흰색 */
  background-color: #000; /* 버튼 배경: 검은색 */
  padding: 10px 20px;
  display: inline-flex; /* inline-flex로 크기 설정 */
  justify-content: center; /* 텍스트 수평 중앙 정렬 */
  align-items: center; /* 텍스트 수직 중앙 정렬 */
  width: 200px; /* 버튼 너비를 동일하게 설정 */
  height: 50px; /* 버튼 높이를 동일하게 설정 */
  border-radius: 5px; /* 약간의 둥근 모서리 */
  transition: all 0.3s ease-in-out; /* 부드러운 전환 효과 */
  /* box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); 약간의 그림자 */
}

.cta:hover {
  background-color: #444; /* Hover 시 배경색 변경 */
  transform: translateY(-10px); /* 살짝 위로 이동 */
}


.cta::before{
    content: '';
    position: absolute;
    top: 0;
    left: -20px;
    width: 100%;
    height: 100%;
    background-color: #E92964;
    color:#fff;
    transform: scaleX(0) skewX(35deg);
    transform-origin: left;
    z-index: -1;
    transition: transform 1s;
}

.cta:hover::before{
    transform: scaleX(1.2) skewX(15deg);
} 

.animated-background{
    background: linear-gradient(
        to right, #833ab4,
        #fd1d1d, #fcb045); 
    background-size: 400% 400%;
    animation: animate-background 10s infinite ease-in-out;
}

@keyframes animate-background {
  0%{
    background-position: 0 50%;
    }
    50%{
      background-position: 100% 50%;
    }
    100%{
      background-position: 0 50%;
    }
}

.movie-list {
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
  justify-content: center;
  margin-top: 20px;
}

/* 개별 영화 항목 스타일 */
.movie-item {
  width: 220px;
  text-align: center;
  border-radius: 10px;
  overflow: hidden;
  transition: transform 0.3s ease-in-out;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  background-color: white;
}

.movie-item:hover {
  transform: translateY(-10px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

/* 영화 포스터 스타일 */
.movie-poster {
  width: 100%;
  height: 300px;
  object-fit: cover;
  border-bottom: 2px solid #e92964;
  transition: opacity 0.3s ease;
}

.movie-item:hover .movie-poster {
  opacity: 0.85;
}

/* 영화 제목 스타일 */
.movie-item h3 {
  font-size: 18px;
  font-weight: bold;
  margin: 10px 0;
  color: #333;
  transition: color 0.3s ease;
}

.movie-item:hover h3 {
  color: #e92964;
}

/* 영화 제목 링크 클릭 시 효과 */
.movie-item a {
  text-decoration: none;
  color: inherit;
}

.movie-item a:hover h3 {
  color: #e92964;
}

/* dropdown 버튼의 화살표 색상 변경 */
.dropdown-toggle::after {
  /* content: ' ▼'; 화살표 표시 */
  font-size: 18px; /* 화살표 크기 */
  color: #fff; /* 화살표 색상 흰색 */
  margin-left: 10px; /* 화살표와 텍스트 간격 */
}

.logo {
  font-size: 3rem; /* 로고 크기 */
  font-weight: bold; /* 텍스트 두껍게 */
  text-transform: uppercase; /* 대문자로 변환 */
  text-align: center; /* 가운데 정렬 */
  margin: 20px 0; /* 상하 여백 */
  color: #e92964; /* 기본 텍스트 색상 설정 (사라지는 것 방지) */
  position: relative; /* 밑줄 추가를 위한 상대 위치 설정 */
  margin-top: 0px;
}

.logo::before {
  content: ''; /* 가상 요소 추가 */
  position: absolute;
  left: 0;
  right: 0;
  bottom: -10px; /* 텍스트 아래 배치 */
  height: 4px; /* 밑줄 두께 */
  background: linear-gradient(to right, #e92964, #fcb045); /* 밑줄 그라데이션 */
  transform: scaleX(1); /* 항상 밑줄 표시 */
  transform-origin: left; /* 확장 시작 위치 설정 */
}


.logo:hover::before {
  transform: scaleX(1); /* 호버 시 밑줄 확장 */
}

@keyframes gradient-move {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

#app.homeview{
  padding : 0px;
  margin : 0px;
}
.logo1 {
  color : white;
  text-align: center;
  margin-bottom: 0px;
  margin-top : 10px;
  font-weight: bold;
  }
</style>

