<template>
    <div class="comments-section">
      <!-- 댓글 작성 폼 -->
      <div class="comment-form">
        <textarea 
          v-model="newComment" 
          placeholder="댓글을 작성해주세요" 
          class="comment-input"
        ></textarea>
        <button @click="addComment" class="submit-button">댓글 작성</button>
      </div>
  
      <!-- 댓글 목록 -->
      <div class="comments-list">
        <div v-for="comment in comments" :key="comment.id" class="comment-item">
          <!-- 댓글 내용 -->
          <div class="comment-content">
            <div class="comment-header">
              <span class="username">{{ comment.username }}</span>
              <span class="timestamp">{{ formatDate(comment.timestamp) }}</span>
            </div>
            
            <div v-if="editingComment?.id === comment.id">
              <textarea 
                v-model="editingComment.content" 
                class="edit-input"
              ></textarea>
              <div class="edit-buttons">
                <button @click="saveEdit(comment)" class="save-button">저장</button>
                <button @click="cancelEdit" class="cancel-button">취소</button>
              </div>
            </div>
            <div v-else>
              <p class="comment-text">{{ comment.content }}</p>
              <div class="comment-actions" v-if="comment.userId === currentUserId">
                <button @click="startEdit(comment)" class="action-button">수정</button>
                <button @click="deleteComment(comment.id)" class="action-button delete">삭제</button>
              </div>
            </div>
  
            <!-- 대댓글 토글 버튼 -->
            <button 
              @click="toggleReply(comment.id)" 
              class="reply-toggle"
            >
              답글 달기
            </button>
  
            <!-- 대댓글 작성 폼 -->
            <div v-if="replyingTo === comment.id" class="reply-form">
              <textarea 
                v-model="newReply" 
                placeholder="답글을 작성해주세요" 
                class="reply-input"
              ></textarea>
              <div class="reply-buttons">
                <button @click="addReply(comment.id)" class="submit-button">답글 작성</button>
                <button @click="cancelReply" class="cancel-button">취소</button>
              </div>
            </div>
  
            <!-- 대댓글 목록 -->
            <div class="replies" v-if="comment.replies && comment.replies.length > 0">
              <div v-for="reply in comment.replies" :key="reply.id" class="reply-item">
                <div class="reply-content">
                  <div class="comment-header">
                    <span class="username">{{ reply.username }}</span>
                    <span class="timestamp">{{ formatDate(reply.timestamp) }}</span>
                  </div>
                  
                  <div v-if="editingComment?.id === reply.id">
                    <textarea 
                      v-model="editingComment.content" 
                      class="edit-input"
                    ></textarea>
                    <div class="edit-buttons">
                      <button @click="saveEdit(reply)" class="save-button">저장</button>
                      <button @click="cancelEdit" class="cancel-button">취소</button>
                    </div>
                  </div>
                  <div v-else>
                    <p class="comment-text">{{ reply.content }}</p>
                    <div class="comment-actions" v-if="reply.userId === currentUserId">
                      <button @click="startEdit(reply)" class="action-button">수정</button>
                      <button @click="deleteReply(comment.id, reply.id)" class="action-button delete">삭제</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, computed } from 'vue';
  import { useCounterStore } from '@/stores/counter'
  
  
  const props = defineProps({
  movieId: {
    type: String,
    required: true
  },
//   currentUserId: {
//     type: String,
//     required: true
//   },
  currentUsername: {
    type: String,
    required: true
  }
});
 // 댓글 작성
 const addComment = () => {
  if (!newComment.value.trim()) return;
  
  const comment = {
    id: Date.now().toString(),
    content: newComment.value,
    username: props.currentUsername, // 실제 사용자 이름 사용
    timestamp: new Date().toISOString(),
    replies: []
  };
  
  store.saveComment(props.movieId, comment); // store에 댓글 저장
  newComment.value = '';
};
//   comments.value.unshift(comment);
//   newComment.value = '';
// };




  
  // 상태 관리
  const store = useCounterStore()
  const comments = computed(() => store.getCommentsByMovieId(props.movieId));
  const newComment = ref('');
  const newReply = ref('');
  const replyingTo = ref(null);
  const editingComment = ref(null);
  
  // 날짜 포맷팅 함수
  const formatDate = (timestamp) => {
    return new Date(timestamp).toLocaleString();
  };
  
 
  
  // 댓글 수정 시작
  const startEdit = (comment) => {
    editingComment.value = {
      id: comment.id,
      content: comment.content
    };
  };
 // 댓글 수정 저장
  const saveEdit = (comment) => {
  const updatedComment = { ...comment, content: editingComment.value.content };
  store.editComment(props.movieId, updatedComment); // store에서 댓글 수정
  cancelEdit();
};
  
  // 댓글 수정 취소
  const cancelEdit = () => {
    editingComment.value = null;
  };
  
  // 댓글 삭제
const deleteComment = (commentId) => {
  if (confirm('정말로 이 댓글을 삭제하시겠습니까?')) {
    store.deleteComment(props.movieId, commentId); // store에서 댓글 삭제
  }
};
  
  // 대댓글 토글
  const toggleReply = (commentId) => {
    replyingTo.value = replyingTo.value === commentId ? null : commentId;
    newReply.value = '';
  };
  
  // 대댓글 작성 취소
  const cancelReply = () => {
    replyingTo.value = null;
    newReply.value = '';
  };
  
  // 대댓글 작성
  const addReply = (commentId) => {
  if (!newReply.value.trim()) return;
  
  const reply = {
    id: Date.now().toString(),
    content: newReply.value,
    userId: props.currentUserId,
    username: props.currentUsername, // 실제 사용자 이름 사용
    timestamp: new Date().toISOString()
  };
  
  const comment = comments.value.find(c => c.id === commentId);
  if (comment) {
    if (!comment.replies) comment.replies = [];
    comment.replies.push(reply);
  }
  
  cancelReply();
};
  
  // 대댓글 삭제
  const deleteReply = (commentId, replyId) => {
    if (confirm('정말로 이 답글을 삭제하시겠습니까?')) {
      const comment = comments.value.find(c => c.id === commentId);
      if (comment && comment.replies) {
        comment.replies = comment.replies.filter(reply => reply.id !== replyId);
      }
    }
  };
  </script>
  
  <style scoped>
  .comments-section {
    margin-top: 20px;
    width: 100%;
  }
  
  .comment-form {
    margin-bottom: 20px;
  }
  
  .comment-input, .reply-input, .edit-input {
    width: 100%;
    min-height: 100px;
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    resize: vertical;
  }
  
  .submit-button, .action-button, .save-button, .cancel-button {
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-right: 8px;
  }
  
  .submit-button {
    background-color: #4CAF50;
    color: white;
  }
  
  .action-button {
    background-color: #2196F3;
    color: white;
  }
  
  .action-button.delete {
    background-color: #f44336;
  }
  
  .cancel-button {
    background-color: #9e9e9e;
    color: white;
  }
  
  .comment-item {
    border-bottom: 1px solid #eee;
    padding: 15px 0;
  }
  
  .comment-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
  }
  
  .username {
    font-weight: bold;
  }
  
  .timestamp {
    color: #666;
    font-size: 0.9em;
  }
  
  .comment-text {
    margin: 8px 0;
  }
  
  .comment-actions {
    margin-top: 8px;
  }
  
  .reply-toggle {
    background: none;
    border: none;
    color: #2196F3;
    cursor: pointer;
    padding: 4px 0;
    margin-top: 8px;
  }
  
  .replies {
    margin-left: 20px;
    padding-left: 20px;
    border-left: 2px solid #eee;
  }
  
  .reply-item {
    margin-top: 10px;
  }
  
  .reply-form {
    margin: 10px 0;
    padding-left: 20px;
  }
  
  .edit-buttons {
    margin-top: 8px;
  }
  </style>