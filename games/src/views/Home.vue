<script setup>
</script>

<template>
  <div class="home">
    <h1 class="home__title">小游戏合集</h1>
    <p class="home__subtitle">基于 Vue 3 + Vite 的练习用小游戏</p>
    <div class="grid">
      <router-link :to="{ name: 'snake' }" class="card">
        <div class="card__title">贪吃蛇</div>
        <div class="card__desc">方向键 / WASD 控制,吃食物长大</div>
      </router-link>
      <div class="card card--placeholder">
        <div class="card__title">2048</div>
        <div class="card__desc">敬请期待</div>
      </div>
      <div class="card card--placeholder">
        <div class="card__title">扫雷</div>
        <div class="card__desc">敬请期待</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home {
  max-width: 900px;
  margin: 0 auto;
  padding: 48px 24px;
  text-align: center;
}
.home__title {
  margin: 0 0 8px;
  font-size: 32px;
}
.home__subtitle {
  margin: 0 0 40px;
  color: #6b7280;
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}
.card {
  display: block;
  padding: 32px 20px;
  border-radius: 12px;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  text-decoration: none;
  color: inherit;
  transition: transform 0.15s, box-shadow 0.15s;
}
.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
}
.card--placeholder {
  opacity: 0.5;
  cursor: not-allowed;
}
.card__title {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 8px;
}
.card__desc {
  font-size: 14px;
  color: #6b7280;
}
</style>
