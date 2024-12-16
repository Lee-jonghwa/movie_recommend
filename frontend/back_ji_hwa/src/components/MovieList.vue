<!-- HOME VIEW에서 가져 올 MOVIE들의 모음 -->

<template>
  <div>
    <h1>MovieList</h1>
    <!-- {{ movies }} -->
    <MovieListItem 
      v-for="movie in movies"
      :key = "movie.title"
      :movie = "movie"

    />
    <!-- movies에 있는 걸 나눠서, 그걸 listitem으로 내림 -->
  </div>
</template>


<script setup>
import MovieListItem from './MovieListItem.vue';
import { useCounterStore } from '@/stores/counter';
import { ref, onMounted } from 'vue';
import axios from 'axios';
const store = useCounterStore()

const movies = ref([
    
  ])

const fetchMovies = async (sortCriteria = '') => {
    try {
        const response = await axios.get(`http://localhost:8000/movies/api/movies/`);
        movies.value = response.data.movies
        // console.log(response.data.movies[1])
    } catch (error) {
        console.error("영화 데이터를 불러오는 중 오류가 발생했습니다:", error)
    }
}

onMounted(() => {
    fetchMovies() // 페이지가 로드될 때 영화 데이터 요청
})


</script>

<style scoped>

</style>