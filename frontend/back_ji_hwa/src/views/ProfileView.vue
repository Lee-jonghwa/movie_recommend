
<template>
  <!-- USERNAME 프로필 제목 -->
  <div class="profile-header">
    <h1>{{ profile.username }}의 프로필</h1>
  </div>
  <!-- 메인 프로필 섹션 -->
  <div class="profile-container">
      <div class="profile-picture-container">
        <!-- 프로필 이미지 -->
        <img
          v-if="profileImage"
          :src="profileImage"
          alt="프로필 사진"
          class="profile-picture"
          @click="triggerImageUpload"
          ref="fileInput"
          />
        <div v-else class="placeholder"><label for="upload">사진 없음</label></div>
        <input
          type="file"
          accept="image/*"
          id="upload"
          class="hidden-input"
          @change="handleImageUpload"
        />
        <label for="upload" class="upload-button" @click="triggerImageUpload">프로필 이미지 수정</label>
      </div>
    <div class="profile-info">
      <p class="info-text"><strong>회원 이름 :</strong>  {{ profile.username }}</p>
      <p class="info-text"><strong>최애 배우 :</strong>  {{ topActor }}</p>
      <p class="info-text"><strong>최애 장르 :</strong>  {{ topGenre }}</p>
    </div>
  </div>
  <hr>
    <div class="profile-movies-container">
      <h2 class="favorite-movies responsive-text">내가 사랑하는 배우 <strong>"{{ topActor }}"</strong> 이/가 출연한 영화</h2>
      <v-sheet v-if="recommendedGenreMovies.length"
        class="mx-auto movie-sheets"
        elevation="8"
        max-width="100%"
        style="width: 100%; padding: 16px; margin: 0; box-sizing: border-box;"
      >
        <v-slide-group
          width="100%"
          center-active
        >
          <v-slide-group-item
            v-for="movie in recommendedActorMovies"
            :key="movie.id"
            v-slot="{ isSelected, toggle, selectedClass }"
          >
          <router-link :to="`/movies/${movie.id}`">
            <v-card
              :color="isSelected ? 'primary' : 'grey-lighten-1'"
              class="ma-4"
              height= "auto"
              width="330"
              box-sizing="border-box"
              @click="toggle"
            >
              <div class="d-flex fill-height align-center justify-center">
                <v-scale-transition>
                  <img 
                :src="movie.poster_path" 
                :alt="movie.title" 
                class="movie-poster"
              />
                </v-scale-transition>
              </div>
            </v-card>
          </router-link>
          </v-slide-group-item>
        </v-slide-group>
      </v-sheet>
      <p v-else>추천 영화가 없습니다.</p>
      <hr>
      <h2 class="favorite-movies responsive-text"> 내가 사랑하는 장르 <strong>"{{ topGenre }}"</strong> 영화</h2>
      <v-sheet v-if="recommendedGenreMovies.length"
        class="mx-auto movie-sheets"
        elevation="8"
        max-width="100%"
        style="width: 100%; padding: 16px; margin: 0; box-sizing: border-box;"
      >
        <v-slide-group
          width="100%"
          center-active
        >
          <v-slide-group-item
            v-for="movie in recommendedGenreMovies"
            :key="movie.id"
            v-slot="{ isSelected, toggle, selectedClass }"
          >
          <router-link :to="`/movies/${movie.id}`">
            <v-card
              :color="isSelected ? 'primary' : 'grey-lighten-1'"
              class="ma-4"
              height= "auto"
              width="330"
              box-sizing="border-box"
              @click="toggle"
            >
              <div class="d-flex fill-height align-center justify-center">
                <v-scale-transition>
                  <img 
                :src="movie.poster_path" 
                :alt="movie.title" 
                class="movie-poster"
              />
                </v-scale-transition>
              </div>
            </v-card>
          </router-link>
          </v-slide-group-item>
        </v-slide-group>
      </v-sheet>
      <p v-else>추천 영화가 없습니다.</p>
    </div>

</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useCounterStore } from '@/stores/counter';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const store = useCounterStore();
const profile = store.profile; // 사용자 프로필 정보


const records = store.records;
const recommendedActorMovies = ref([]);
const recommendedGenreMovies = ref([]);

const movies = store.movies;
const topActor = store.getTopActor();
const topGenre = store.getTopGenre();

// 프로필 이미지 상태
const profileImage = ref(store.profile.image || '');
const fileInput = ref(null); // 파일 입력 필드 참조

// 이미지 업로드 처리
const handleImageUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      profileImage.value = e.target.result; // 이미지 URL 저장
      store.profile.image = profileImage.value; // 스토어에 저장
    };
    reader.readAsDataURL(file);
  }
  // 파일 입력 초기화 (같은 파일 재업로드 가능)
  event.target.value = '';
};

// 파일 선택 창 열기
const triggerImageUpload = () => {
  fileInput.value?.click();
};

// 추천 영화를 필터링
const updateRecommendedActorMovies = () => {
  const topActor = store.getTopActor(); // 최다 빈도 배우 가져오기
  // console.log('movie:',movies)
  if (topActor) {
    // actors 데이터가 유효한 영화 필터링
    recommendedActorMovies.value = movies.filter((movie) => {
      // console.log('movie',movie)
      const actors = movie.actors.split(',').map((a) => a.trim()) || []; // actors 필드가 없으면 빈 배열로 처리
      // console.log('actors',actors)
      return actors.some((actor) => actor === topActor); // 배우가 일치하는지 검사
    });

    
  } else {
    recommendedActorMovies.value = [];
  }
};

const updateRecommendedGenreMovies = () => {
  const topGenre = store.getTopGenre(); // 최다 빈도 장르 가져오기
  
  if (topGenre) {
    // actors 데이터가 유효한 영화 필터링
    recommendedGenreMovies.value = movies.filter((movie) => {
      // console.log('movie',movie)
      const genre = movie.genre.split(',').map((a) => a.trim()) || []; // actors 필드가 없으면 빈 배열로 처리
      // console.log('actors',actors)
      return genre.some((actor) => actor === topGenre); // 장르가 일치하는지 검사
    });

    
  } else {
    recommendedGenreMovies.value = [];
  }
};


onMounted(() => {
  updateRecommendedActorMovies(); // 전체 영화 목록 가져오기
  updateRecommendedGenreMovies();
  
});
</script>

<style scoped>
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

h2 {
  font-size: 40px;
  margin: 20px;
}

.info-text {
  font-size: 28px;
}

.profile-container {
  padding: 16px;
  color: white;
  display: flex;
  /* flex-direction: column; */
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 16px;
}


.profile-movies-container {
  display: flex;
  flex-direction: column;
  align-items: left;
  justify-content: center;
  flex-grow: 1;
  text-align: left;
}

.movie-sheets {
  background-color: #00000083;
  overflow: hidden;
  padding: 20px;
  margin-bottom: 20px;
}

.profile-info {
  margin-top: 16px;
  margin-left: 40px;
  color: white;
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.movie-poster {
  width: 100%; /* 가로 크기를 부모 요소에 맞춤 */
  height: auto; /* 비율 유지 */
  max-height: 450px; /* 최대 높이 제한 */
  object-fit: cover; /* 이미지 비율에 맞게 잘라냄 */
  border-radius: 8px; /* 모서리 둥글게 */
}

.profile-picture {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border: 1px solid #ccc;
  border-radius: 2%;
}

.profile-picture-container {
  position: relative;
  width: 300px;
  height: 300px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding : 20px;

}

.placeholder {
  width: 100%;
  height: 100%;
  font-size: 14px;
  color: #505050;
  background-color: #ececec91;
}

.favorite-movies {
  margin-top: 16px;
  color: white;
}

.v-sheet {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 30px;
}

hr {
  margin: 20px;
  border: 1px solid #e9e9e9b2;
}

.hidden-input {
  display: none;
}

.upload-button {
  margin-top: 1px;
  color: #ffffff;
  font-size: 17px;
}

.responsive-text {
  font-size: clamp(30px, 2vw, 35px);
  /* 최소값: 14px, 중간값: 2vw, 최대값: 24px */
}
</style>
