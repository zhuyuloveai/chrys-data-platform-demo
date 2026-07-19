<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
})
defineEmits(['back'])
</script>

<template>
  <div class="shell">
    <header class="shell__bar">
      <button class="shell__back" @click="$emit('back')">← 返回首页</button>
      <h1 class="shell__title">{{ title }}</h1>
      <span class="shell__spacer" />
    </header>
    <main class="shell__body">
      <slot />
    </main>
  </div>
</template>

<style scoped>
.shell {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.shell__bar {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 24px;
  background: #ffffff;
  border-bottom: 1px solid #e5e7eb;
}
.shell__back {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  color: #2563eb;
  padding: 6px 10px;
  border-radius: 6px;
}
.shell__back:hover {
  background: #eff6ff;
}
.shell__title {
  margin: 0;
  font-size: 20px;
}
.shell__spacer {
  flex: 1;
}
.shell__body {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 24px;
}
</style>
