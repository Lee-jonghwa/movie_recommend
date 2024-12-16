<!-- Movie List에서 보여줄 ITEM들의 모임이자 DETAIL 뷰로 가능 길목 -->

<template>
  <div>
    <h1>MovieListItem</h1>
    <p>이미지</p>
    <p>제목 {{ movie.title}}</p>
    <p>내용 {{ movie.content }}</p>
    <RouterLink :to="{name:'MovieDetailView', params: { title: movie.title}}">Detail</RouterLink>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router';

defineProps({
  movie: Object
})

</script>

<style scoped>

</style>