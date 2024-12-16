import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useCounterStore = defineStore('counter', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(null)
  // const movies = ref([])
  const movies = ref([])
  const username = ref(null)
  const currentUser = ref(null)
  const profile = ref({
    username: null,
    followers: null,
    followings: null,
    id: null,
    img : null,
  })
  const comments = ref({}) // 각 영화 ID별 댓글을 저장하는 객체

  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })
  const router = useRouter()

  // // axios 인스턴스 생성
  // const api = axios.create({
  //   baseURL: API_URL,
  //   headers: {
  //     'Content-Type': 'application/json',
  //   }
  // })
  
  // // 요청 인터셉터 추가
  // api.interceptors.request.use(
  //   (config) => {
  //     const token = localStorage.getItem('access_token')
  //     if (token) {
  //       config.headers.Authorization = `Bearer ${token}`
  //     }
  //     return config
  //   },
  //   (error) => Promise.reject(error)
  // )
  // 댓글 추가
  
  const saveComment = (movieId, comment) => {
    if (!comments.value[movieId]) {
      comments.value[movieId] = [];
    }
    comments.value[movieId].unshift(comment); // 새로운 댓글을 맨 앞에 추가
  };
  // 댓글 삭제
  const deleteComment = (movieId, commentId) => {
    if (comments.value[movieId]) {
      comments.value[movieId] = comments.value[movieId].filter(comment => comment.id !== commentId)
    }
  };

  const editComment = (movieId, updatedComment) => {
    if (comments.value[movieId]) {
      const targetIndex = comments.value[movieId].findIndex(c => c.id === updatedComment.id);
      if (targetIndex !== -1) {
        comments.value[movieId][targetIndex] = updatedComment;
      }
    }
  };
  const getCommentsByMovieId = (movieId) => {
    return comments.value[movieId] || [];
  };
  // 영화 데이터 받아와서 movies에 저장
  const getMovies = function () {
    axios({
      method: 'get',
      url: `${API_URL}/movies/`,
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    }) .then((res) => {
      movies.value=res.data
    }) .catch((err) => {
      console.error('Error fetching movies:', err)
      if (err.response?.status === 503) {
        console.error('Service unavailable. Please try again later.')
      }
    })
  }

  
  

  // signup
  const signUp = function (payload) {
    const { username, password1, password2 } = payload

    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username, password1, password2
      }
    }).then((res) => {
      router.push({ name: 'HomeView'})
    }) .catch((err) => {
      console.log(err)
    })
  }
  const records = ref([])
  const logIn = function (payload) {
    const { username, password } = payload

    axios({
      method:'post',
      url:`${API_URL}/accounts/login/`,
      data: { username, password }
    }) .then((res) => {
      token.value = res.data.key
      currentUser.value = payload.username
      records.value = [];
      localStorage.setItem('records', JSON.stringify(records.value))
      localStorage.setItem('token', res.data.key)
      localStorage.setItem('username', payload.username)
      profile.value.username = payload.username
      router.push({ name: 'HomeView'})
    }) .catch(err => {
      console.error('Login error:', err)
      return Promise.reject(err)
    })
  }


  // logout
  const logOut = function () {
    axios({
      method : 'post',
      url : `${API_URL}/accounts/logout/`
    })
    .then((res) => {
      token.value = null
      localStorage.removeItem('token')
      localStorage.removeItem('username')
      localStorage.removeItem('records')
      router.push({ name: 'HomeView'})
    })
    .catch((err) => {
      console.log(err)
    })
  }


  const findMovieById = (movies,id) => {
    return movies.find(movie => movie.tmdb_id === id)
  }

    // 영화 기록 추가 함수
    const addMovieRecord = (movie) => {
      // 중복 체크 방지
      if (!records.value.some((record) => record.id === movie.id)) {
        records.value.push({
          tmdb_id: movie.id,
          genre: movie.genre.split(',').map((g) => g.trim()), // 영화의 장르 배열
          actors: movie.actors.split(',').map((a) => a.trim()), // 영화의 장르 배열
        })
        localStorage.setItem('records', JSON.stringify(records.value))
        ;
      }
    };
  
    // 추천 장르 계산 함수
    const getTopGenre = () => {
      const genreCount = {};
      // console.log('getTopActor',records.value)
      // 각 기록의 장르를 카운트
      records.value.forEach((record) => {
        record.genre.forEach((genre) => {
          // console.log('actor',actor)
          genreCount[genre] = (genreCount[genre] || 0) + 1;
          // console.log('actorCount',actorCount)
        });
      });
  
      // 가장 빈도가 높은 장르 반환
      const topGenre = Object.entries(genreCount).reduce(
        (top, current) => (current[1] > top[1] ? current : top),
        ['', 0]
      );
      return topGenre[0]; // 장르 이름만 반환
    };


    // 추천 배우 계산 함수
    const getTopActor = () => {
      const actorCount = {};
      // console.log('getTopActor',records.value)
      // 각 기록의 배우를 카운트
      records.value.forEach((record) => {
        record.actors.forEach((actor) => {
          // console.log('actor',actor)
          actorCount[actor] = (actorCount[actor] || 0) + 1;
          // console.log('actorCount',actorCount)
        });
      });
  
      // 가장 빈도가 높은 배우 반환
      const topActor = Object.entries(actorCount).reduce(
        (top, current) => (current[1] > top[1] ? current : top),
        ['', 0]
      );
      // console.log('topActor',topActor)
      return topActor[0]; // 배우 이름만 반환
    };

  

  return { profile, movies, API_URL, token, isLogin, logOut, logIn, getMovies, signUp , currentUser, comments,
    saveComment, deleteComment, editComment,getCommentsByMovieId, records, findMovieById, addMovieRecord, getTopActor, getTopGenre}
}, { persist: true, })
