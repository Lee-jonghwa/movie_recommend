import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    // 사용자 정보를 저장
    user: null,
    // 로그인 상태
    isAuthenticated: false
  }),

  getters: {
    // 현재 사용자 ID 반환
    currentUserId: (state) => state.user?.id,
    // 현재 사용자 이름 반환
    currentUsername: (state) => state.user?.username,
    // 로그인 상태 확인
    checkAuth: (state) => state.isAuthenticated
  },

  actions: {
    // // 로그인 처리
    // login(userData) {
    //   this.user = userData
    //   this.isAuthenticated = true
    //   // 로컬 스토리지에 사용자 정보 저장
    //   localStorage.setItem('user', JSON.stringify(userData))
    // },

    // // 로그아웃 처리
    // logout() {
    //   this.user = null
    //   this.isAuthenticated = false
    //   // 로컬 스토리지에서 사용자 정보 제거
    //   localStorage.removeItem('user')
    // },

    // 초기화 - 페이지 새로고침 시 로컬 스토리지에서 사용자 정보 복구
    initializeAuth() {
      const storedUser = localStorage.getItem('user')
      if (storedUser) {
        try {
          this.user = JSON.parse(storedUser)
          this.isAuthenticated = true
        } catch (error) {
          console.error('Failed to parse stored user:', error)
          this.logout()
        }
      }
    }
  }
})