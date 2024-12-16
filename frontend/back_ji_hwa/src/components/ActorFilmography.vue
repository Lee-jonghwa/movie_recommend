<template>
  <span 
    @click="getActorFilmography" 
    class="actor-name cursor-pointer hover:text-blue-500"
  >
    {{ actor }}
    <span v-if="!isLast">, </span>
  </span>
  <!-- 로딩 상태와 결과 표시를 위한 모달 -->
  <div v-if="showModal" class="modal-overlay">
    <div class="modal-content">
      <div class="modal-header">
        <h3 class="modal-title">
          <span class="actor-title-name">{{ actor }}</span>
          <span class="actor-title-suffix">의 대표작</span>
        </h3>
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
  actor: {
    type: String,
    required: true
  },
  isLast: {
    type: Boolean,
    default: false
  }
});

const showModal = ref(false);
const loading = ref(false);
const filmography = ref(null);
const error = ref(null);
const API_KEY = config.API_KEY

// GPT 응답을 포맷팅하는 computed 속성
const formattedFilmography = computed(() => {
  if (!filmography.value) return '';
  return filmography.value.split('\n').join('<br>');
});

const getActorFilmography = async () => {
  showModal.value = true;
  loading.value = true;
  error.value = null;
  
  try {
    const prompt = `${props.actor}의 대표작 3개를 아래 형식으로 알려주세요:
1. 영화 제목(제작년도)
2. 감독
3. 주요 배우들

각 영화는 위 세 가지 정보를 포함해야 하며, 총 3개의 영화를 알려주세요.`;

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
/* 모달 제목 스타일 */
/* 모달 헤더 */
.modal-header {
  display: flex;
  justify-content: space-between; /* 양쪽 끝 정렬 */
  align-items: center;
  width: 100%; /* 전체 너비 차지 */
  margin-bottom: 15px;
  border-bottom: 1px solid #ccc;
  padding-bottom: 10px;
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



/* 배우 이름 부분 스타일링 */
.actor-title-name {
  font-weight: 1000; /* 더 굵은 글씨체 */
  font-size: 30px;
}

/* "의 대표작" 부분 스타일링 */
.actor-title-suffix {
  font-weight: 400; /* 일반 굵기 */
}

/* 모달 컨텐츠 */
.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  max-width: 500px;
  width: 90%;
  animation: fadeIn 0.3s ease-in-out;
}
/* 모달 오버레이 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

/* 모달 컨텐츠 */
.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  max-width: 500px;
  width: 90%;
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
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

/* 로딩 상태 */
.loading {
  text-align: center;
  padding: 20px;
  font-size: 16px;
  color: #34495e;
}

/* 에러 메시지 */
.error {
  color: red;
  text-align: center;
  padding: 10px;
}

/* 영화 데이터 스타일 */
.modal-body strong {
  color: #2c3e50;
  font-weight: bold;
  background-color: #f9f9f9;
  padding: 4px 6px;
  border-radius: 4px;
  display: inline-block;
  margin: 5px 0;
}
</style>