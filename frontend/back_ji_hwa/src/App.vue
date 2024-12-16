
<template>
  <div>
    <nav-bar></nav-bar>
    <RouterView />
    <foot-bar></foot-bar>
  </div>

</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'
import NavBar from '@/NavBar.vue'
import FootBar from '@/FootBar.vue'

const store = useCounterStore()

const userId = ref(1)

const logOut = function () {
  store.logOut()
}

</script>


<style scoped>
  * {
    font-family: 'IBM Plex Sans KR', sans-serif;
  }

  *::selection{
    background-color: #e92964;
    color : #fff
  }

  #btn-back-to-top {
    position: fixed;
    bottom: 60px;
    right: 90px;
    background-color: #e92964;
    color:#fff;
  }
</style>
