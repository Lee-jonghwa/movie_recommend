
<template>
  <!-- 네브바에 stick-top을 넣을지 말지 결정 : 고정 버튼 없다면 있는게 나을 듯 함-->
    <nav class="navbar navbar-expand-md stick-top navbar-light sticky-top py-2">
      <div class="container-fluid">
        <!-- 이미지 연결 
        <router-link class="navbar-brand" to="/" style="margin-left: 15px; margin-right: 10px;padding-bottom: 15px;">
          <img id="navbar-logo" src="@/assets/logo2.png" alt="netflix_logo" width="60px" height="50px">
        </router-link>-->
        <!--햄버거 버튼-->
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse justify-content-between" id="navbarSupportedContent">
          <ul class="navbar-nav pe-3">
            <li class="nav-item">
              <RouterLink class="nav-link" aria-current="page" to="/" style="color:black">Home</RouterLink>
            </li>
            <li class="nav-item" v-if="store.currentUser">
              <RouterLink class="nav-link" aria-current="page" :to="{ name : 'ProfileView', params : {username: store.currentUser} }" style="color:black">Profile</RouterLink>
            </li>
            <li class="nav-item">
              <!--<a href="#" class="nav-link" aria-current="page" :to="{ name : 'ProfileView', params: {userId:userId}}" style="color:black">Profile</a>
               <RouterLink class="nav-link" to="/profile" style="color:black">Profile</RouterLink> -->
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" :to="{ name : 'SignUpView'}" style="color:black">SignUp</RouterLink>
            </li>
            <li class="nav-item" v-if="!store.currentUser">
              <RouterLink class="nav-link" :to="{ name : 'LoginView'}" style="color:black">Login</RouterLink>
            </li>
            <li class="nav-item" v-if="store.currentUser">
              <button class="nav-link" @click.prevent="logOut" style="color:black">Logout</button>
            </li>
            
          </ul>
          <form class="d-flex" role="search" @submit.prevent="onSearch">
            <input 
              class="form-control me-2" 
              type="search" 
              placeholder="Search" 
              aria-label="Search" 
              v-model="searchQuery"
            >
        <button class="btn btn-outline-secondary" type="submit">Search</button>
      </form>
        </div>
      </div>
    </nav>
</template>

<script setup>
  import { computed, ref,onMounted } from 'vue'
  import { RouterView } from 'vue-router';
  import { useCounterStore } from '@/stores/counter'  ;
  import { useRouter } from 'vue-router';
  const store = useCounterStore()
  const router = useRouter();
  const searchQuery = ref(''); // 검색어를 저장할 변수
// 검색 폼이 제출되면, 검색어를 쿼리 파라미터로 홈 페이지로 전달
  const onSearch = () => {
    if (searchQuery.value.trim()) {
      router.push({ path: '/', query: { search: searchQuery.value } });
    }
  };
  const userId = ref(1)
  const username = store.currentUser

  const loginState = computed(() => {
    return this.isLoggedIn ? "Logout" : "Login"
  })

  const logOut = function () {
    store.logOut()
  }



</script>

<style scoped>

.navbar {
  background-color: #000000; /* 네브바 배경색을 검은색으로 설정 */
}

.navbar-nav .nav-link {
  text-align: center;
  padding: 8px 12px;
  margin: 5px;
  background: none;
  border: none;
  color: rgb(255, 255, 255) !important; /* 텍스트 색을 검은색으로 설정 */
  font-weight: bold; /* 글씨 굵게 */
  text-transform: uppercase;
  letter-spacing: 2px;
  cursor: pointer;
  outline: none;
  box-shadow: none;
  font-size: 14px;
  transition: color 0.3s ease, transform 0.3s ease;
}

.navbar-nav .nav-link:hover {
  color: white; /* hover 시 글자 색을 흰색으로 변경 */
  transform: scale(1.1); /* hover 시 확대 효과 */
}
.btn-outline-secondary {
  color: white !important;
}


</style>