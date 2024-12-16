<template>
  <footer>
    <!-- 3. 본인 이름 작성 -->
    <div style="background-color: rgb(230, 230, 230); font-size: 13px;">
      <div
        style="text-align: center; margin-top: 20px; color: grey;"
        class="d-flex justify-content-center align-items-center"
      >
        <span style="padding: 2px 10px;">SSAFY 12기</span>
        <span class="name" style="padding: 2px 10px;">Seongwook Baek | Jonghwa Lee</span>
        <span style="padding: 2px 10px;">© 2024 All Rights Reserved.</span>
      </div>
    </div>
  </footer>
</template>

<script setup>
</script>

<style scoped>
.name {
  background: linear-gradient(45deg, #9a9ae3, #ba68ed);
  animation: hue-rotate 2s linear infinite alternate;
  color: rgb(26, 26, 26);
  border-radius: 5px;
  display: inline-block;
}

@keyframes hue-rotate {
  to {
    filter: hue-rotate(90deg);
  }
}
</style>
