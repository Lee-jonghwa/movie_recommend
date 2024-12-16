import { createRouter, createWebHistory } from 'vue-router'
import { useCounterStore } from '@/stores/counter'

// 메인 페이지
import HomeView from '@/views/HomeView.vue'

// 영화
import MovieDetailView from '@/views/MovieDetailView.vue'
import MovieCommentView from '@/views/MovieCommentView.vue'

// 프로필, 로그인
import ProfileView from '@/views/ProfileView.vue'
import LoginView from '@/views/LoginView.vue'
import SignUpView from '@/views/SignUpView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomeView',
      component: HomeView,
    },
    {
      path: '/movies/:id',
      name: 'MovieDetailView',
      component: MovieDetailView,
    },
    {
      path: '/movies/:id/comments',
      name: 'MovieCommentView',
      component: MovieCommentView,
    },
    {
      path: '/profile/:username',
      name: 'ProfileView',
      component: ProfileView,
    },
    {
      path: '/login',
      name: 'LoginView',
      component: LoginView,
    },
    {
      path: '/signup',
      name: 'SignUpView',
      component: SignUpView,
    },
  
],
})

router.beforeEach((to, from) => {
  const store = useCounterStore()
  if (to.name === 'HomeView' && !store.isLogin) {
    window.alert('로그인이 필요합니다.')
    return { name : 'LoginView'}
  }
  if ((to.name === 'SignUpView' || to.name === 'LogInView') && (store.isLogin)) {
    window.alert('이미 로그인 되어 있습니다.')
    return { name: 'HomeView' }
  } 
})

router.beforeEach((to, from, next) => {
  const store = useCounterStore();

  if (to.name === 'ProfileView' && !store.currentUser) {
    alert('로그인된 사용자 정보가 없습니다.');
    return { name: 'LoginView' }; // 로그인 페이지로 리다이렉트
  }

  next();
});

export default router
