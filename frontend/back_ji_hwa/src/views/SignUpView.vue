<template>
  <div class="page">
  <div class="container">
    <div class="left">
      <div class="login">Sign Up</div>
      <div class="eula">By logging in you agree to the ridiculously long terms that you didn't bother to read</div>
    </div>
    <div class="right">
      <svg viewBox="0 0 320 300">
        <defs>
          <linearGradient
                          inkscape:collect="always"
                          id="linearGradient"
                          x1="13"
                          y1="193.49992"
                          x2="307"
                          y2="193.49992"
                          gradientUnits="userSpaceOnUse">
            <stop
                  style="stop-color:#ff00ff;"
                  offset="0"
                  id="stop876" />
            <stop
                  style="stop-color:#ff0000;"
                  offset="1"
                  id="stop878" />
          </linearGradient>
        </defs>
        <path d="m 40,120.00016 239.99984,-3.2e-4 c 0,0 24.99263,0.79932 25.00016,35.00016 0.008,34.20084 -25.00016,35 -25.00016,35 h -239.99984 c 0,-0.0205 -25,4.01348 -25,38.5 0,34.48652 25,38.5 25,38.5 h 215 c 0,0 20,-0.99604 20,-25 0,-24.00396 -20,-25 -20,-25 h -190 c 0,0 -20,1.71033 -20,25 0,24.00396 20,25 20,25 h 168.57143" />
      </svg>
      <form class="form" @submit.prevent="signUp">
        <label for="username">username</label>
        <input type="text" id="username" v-model.trim="username">
        <label for="password1">Password1</label>
        <input type="password" id="password1" v-model.trim="password1">
        <label for="password2">Password2</label>
        <input type="password" id="password2" v-model.trim="password2">
        <input type="submit" id="submit" value="Sign Up">
      </form>
    </div>
  </div>
</div>


</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter';
import anime from 'animejs/lib/anime.es.js'; // anime.js 임포트

const username = ref(null)
const password1 = ref(null)
const password2 = ref(null)
const email = ref(null)

const store = useCounterStore()

const signUp = function () {
  if (password1.value === password2.value) {
    const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
  }
  console.log(payload)
  store.signUp(payload)
  } else {
    console.log('불일치')
  }
}

onMounted(() => {
  let current = null;

  const usernameElement = document.querySelector('#username');
  const emailElement = document.querySelector('#email');
  const password1Element = document.querySelector('#password1');
  const password2Element = document.querySelector('#password2');
  const submitElement = document.querySelector('#submit');

  if (usernameElement) {
    usernameElement.addEventListener('focus', () => {
      if (current) current.pause();
      current = anime({
        targets: 'path',
        strokeDashoffset: {
          value: 0,
          duration: 700,
          easing: 'easeOutQuart',
        },
        strokeDasharray: {
          value: '240 1386',
          duration: 700,
          easing: 'easeOutQuart',
        },
      });
    });
  }

  if (password1Element) {
    password1Element.addEventListener('focus', () => {
      if (current) current.pause();
      current = anime({
        targets: 'path',
        strokeDashoffset: {
          value: -336,
          duration: 700,
          easing: 'easeOutQuart',
        },
        strokeDasharray: {
          value: '240 1386',
          duration: 700,
          easing: 'easeOutQuart',
        },
      });
    });
  }

  if (password2Element) {
    password2Element.addEventListener('focus', () => {
      if (current) current.pause();
      current = anime({
        targets: 'path',
        strokeDashoffset: {
          value: -672,
          duration: 700,
          easing: 'easeOutQuart',
        },
        strokeDasharray: {
          value: '240 1386',
          duration: 700,
          easing: 'easeOutQuart',
        },
      });
    });
  }

  if (emailElement) {
    emailElement.addEventListener('focus', () => {
      if (current) current.pause();
      current = anime({
        targets: 'path',
        strokeDashoffset: {
          value: -1008,
          duration: 700,
          easing: 'easeOutQuart',
        },
        strokeDasharray: {
          value: '240 1386',
          duration: 700,
          easing: 'easeOutQuart',
        },
      });
    });
  }

  if (submitElement) {
    submitElement.addEventListener('focus', () => {
      if (current) current.pause();
      current = anime({
        targets: 'path',
        strokeDashoffset: {
          value: -1344,
          duration: 700,
          easing: 'easeOutQuart',
        },
        strokeDasharray: {
          value: '530 1386',
          duration: 700,
          easing: 'easeOutQuart',
        },
      });
    });
  }
});
</script>

<style scoped>
@import url('https://rsms.me/inter/inter-ui.css');
::selection {
  background: #2D2F36;
}
::-webkit-selection {
  background: #2D2F36;
}
::-moz-selection {
  background: #2D2F36;
}
body {
  background: white;
  font-family: 'Inter UI', sans-serif;
  margin: 0;
  padding: 20px;
}
.page {
  background: #e2e2e5;
  display: flex;
  flex-direction: column;
  height: calc(100% - 40px);
  position: absolute;
  place-content: center;
  width: calc(100% - 40px);
}
@media (max-width: 767px) {
  .page {
    height: auto;
    margin-bottom: 20px;
    padding-bottom: 20px;
  }
}
.container {
  display: flex;
  height: 320px;
  margin: 0 auto;
  width: 640px;
}
@media (max-width: 767px) {
  .container {
    flex-direction: column;
    height: 630px;
    width: 320px;
  }
}
.left {
  background: white;
  height: calc(100% - 40px);
  top: 20px;
  position: relative;
  width: 50%;
}
@media (max-width: 767px) {
  .left {
    height: 100%;
    left: 20px;
    width: calc(100% - 40px);
    max-height: 270px;
  }
}
.login {
  font-size: 50px;
  font-weight: 900;
  margin: 50px 40px 40px;
}
.eula {
  color: #999;
  font-size: 14px;
  line-height: 1.5;
  margin: 40px;
}
.right {
  background: #474A59;
  box-shadow: 0px 0px 40px 16px rgba(0,0,0,0.22);
  color: #F1F1F2;
  position: relative;
  width: 50%;
}
@media (max-width: 767px) {
  .right {
    flex-shrink: 0;
    height: 100%;
    width: 100%;
    max-height: 350px;
  }
}
svg {
  position: absolute;
  width: 320px;
}
path {
  fill: none;
  stroke: url(#linearGradient);;
  stroke-width: 4;
  stroke-dasharray: 240 1386;
}
.form {
  margin: 40px;
  position: absolute;
}
label {
  color:  #c2c2c5;
  display: block;
  font-size: 14px;
  height: 16px;
  margin-top: 20px;
  margin-bottom: 5px;
}
input {
  background: transparent;
  border: 0;
  color: #f2f2f2 ;
  font-size: 20px;
  height: 30px;
  line-height: 30px;
  outline: none !important;
  width: 100%;
}
input::-moz-focus-inner { 
  border: 0; 
}

/* password2 배경색 추가 */
#password2 {
  background: #E8F0FE; /* 밝은 파란색 */
  color: black;
  padding: 5px; /* 약간의 안쪽 여백 */
}

#submit {
  color: #707075;
  margin-top: 20px; /* 기존 40px에서 줄임 */
  transition: color 300ms;
  cursor: pointer; /* 클릭 가능하게 시각적 표시 */
}
#submit:focus {
  color: #f2f2f2;
}
#submit:active {
  color: #d0d0d2;
}

</style>