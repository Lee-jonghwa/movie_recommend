<template>
  <span 
    @click="getDirectorFilmography" 
    class="director-name cursor-pointer hover:text-blue-500 director-title-name"
  >
    {{ director }}
  </span>
  <!-- 모달 -->
  <div v-if="showModal" class="modal-overlay">
    <div class="modal-content">
      <div class="modal-header">
        <h3 class="modal-title"><span class="director-title-name">{{ director }}</span> 감독의 대표작</h3>
        <button @click="showModal = false" class="close-button">&times;</button>
      </div>
      <div class="modal-body">
        <div v-if="loading" class="loading">
          로딩중...
        </div>
        <div v-else-if="filmography" v-html="formattedFilmography"></div>
        <div v-else-if="error" class="error">
          {{ error }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
<script type ="text/javascript" src="/frontend/back_ji_hwa/src/apikey.js"></scirpt>
import { ref, computed } from 'vue';
import axios from 'axios';

const props = defineProps({
  director: {
    type: String,
    required: true
  }
});

const showModal = ref(false);
const loading = ref(false);
const filmography = ref(null);
const error = ref(null);
const API_KEY = config.API_KEY

const formattedFilmography = computed(() => {
  if (!filmography.value) return '';
  return filmography.value.split('\n').join('<br>');
});

const getDirectorFilmography = async () => {
  showModal.value = true;
  loading.value = true;
  error.value = null;
  
  try {
    const prompt = `${props.director} 감독의 대표작 3개를 아래 형식으로 알려주세요:
1. 영화 제목(제작년도)
2. 감독
3. 주요 배우들

각 영화는 위 세 가지 정보를 포함해야 하며, 총 3개의 영화를 알려주세요.
최신작 순서로 정렬해주세요.`;

    const response = await axios.post(
      'https://api.openai.com/v1/chat/completions',
      {
        model: 'gpt-4-turbo',
        messages: [{ role: 'user', content: prompt }],
        max_tokens: 1000,
        temperature: 0.7,
      },
      {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${API_KEY}`,
        },
      }
    );
    
    filmography.value = response.data.choices[0].message.content.trim();
  } catch (err) {
    error.value = '정보를 가져오는 데 실패했습니다.';
    console.error('Error:', err);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  max-width: 500px;
  width: 90%;
  animation: modalFadeIn 0.3s ease;
}

/* 감독 이름을 굵게 스타일링 */
.director-title-name {
  font-weight: bold; /* 굵게 설정 */
}

/* 모달 제목 스타일 */
.modal-title {
  background-color: #000; /* 배경색: 검정 */
  color: #fff;            /* 글자색: 흰색 */
  padding: 10px 15px;     /* 내부 여백 */
  border-radius: 8px;     /* 둥근 테두리 */
  font-size: 1.5rem;      /* 글자 크기 */
  text-align: center;     /* 가운데 정렬 */
  flex-grow: 1;           /* 제목을 가운데 배치하기 위해 확장 */
}

/* 모달 헤더 스타일 */
.modal-header {
  display: flex;
  justify-content: space-between; /* 양쪽 끝 정렬 */
  align-items: center;
  width: 100%;
  margin-bottom: 15px;
  border-bottom: 1px solid #ccc;
  padding-bottom: 10px;
}

/* 닫기 버튼 */
.close-button {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #34495e;
  transition: color 0.3s;
}

.close-button:hover {
  color: #e74c3c;
}

/* 로딩 및 에러 메시지 스타일 */
.loading {
  text-align: center;
  padding: 20px;
  color: #666;
}

.error {
  color: #dc3545;
  text-align: center;
  padding: 10px;
  background-color: #f8d7da;
  border-radius: 4px;
}

/* 영화 필모그래피 출력 스타일 */
.modal-body {
  margin-top: 20px;
}

/* 애니메이션 효과 */
@keyframes modalFadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .modal-content {
    width: 95%;
    padding: 15px;
  }
}
</style>
