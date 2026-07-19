<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import GameShell from '../../components/GameShell.vue'
import { createInitialState, setDirection, tick, DIRECTIONS } from './engine.js'

const ROWS = 20
const COLS = 20
const CELL = 20
const TICK_MS = 150

const router = useRouter()
const canvas = ref(null)
const state = ref(createInitialState({ rows: ROWS, cols: COLS }))
let timer = null

const KEY_MAP = {
  ArrowUp: DIRECTIONS.up,
  ArrowDown: DIRECTIONS.down,
  ArrowLeft: DIRECTIONS.left,
  ArrowRight: DIRECTIONS.right,
  w: DIRECTIONS.up,
  s: DIRECTIONS.down,
  a: DIRECTIONS.left,
  d: DIRECTIONS.right,
}

function draw() {
  const ctx = canvas.value.getContext('2d')
  const w = COLS * CELL
  const h = ROWS * CELL
  ctx.fillStyle = '#111827'
  ctx.fillRect(0, 0, w, h)
  ctx.strokeStyle = '#1f2937'
  ctx.lineWidth = 1
  for (let i = 0; i <= COLS; i++) {
    ctx.beginPath()
    ctx.moveTo(i * CELL, 0)
    ctx.lineTo(i * CELL, h)
    ctx.stroke()
  }
  for (let i = 0; i <= ROWS; i++) {
    ctx.beginPath()
    ctx.moveTo(0, i * CELL)
    ctx.lineTo(w, i * CELL)
    ctx.stroke()
  }
  if (state.value.food) {
    const { row, col } = state.value.food
    ctx.fillStyle = '#ef4444'
    ctx.fillRect(col * CELL + 1, row * CELL + 1, CELL - 2, CELL - 2)
  }
  state.value.snake.forEach((seg, idx) => {
    ctx.fillStyle = idx === 0 ? '#22c55e' : '#16a34a'
    ctx.fillRect(seg.col * CELL + 1, seg.row * CELL + 1, CELL - 2, CELL - 2)
  })
}

function step() {
  if (state.value.isOver) {
    stop()
    return
  }
  state.value = tick(state.value)
  draw()
  if (state.value.isOver) {
    stop()
  }
}

function start() {
  stop()
  timer = setInterval(step, TICK_MS)
}

function stop() {
  if (timer) {
    clearInterval(timer)
    timer = null
  }
}

function reset() {
  state.value = createInitialState({ rows: ROWS, cols: COLS })
  draw()
  start()
}

function onKey(e) {
  const dir = KEY_MAP[e.key]
  if (!dir) {
    if ((e.key === ' ' || e.key === 'Enter') && state.value.isOver) {
      e.preventDefault()
      reset()
    }
    return
  }
  e.preventDefault()
  if (state.value.isOver) return
  state.value = setDirection(state.value, dir)
}

function goHome() {
  router.push('/')
}

onMounted(() => {
  draw()
  start()
  window.addEventListener('keydown', onKey)
})

onUnmounted(() => {
  stop()
  window.removeEventListener('keydown', onKey)
})
</script>

<template>
  <GameShell title="贪吃蛇" @back="goHome">
    <div class="meta">分数:{{ state.score }}</div>
    <div class="board-wrap">
      <canvas ref="canvas" :width="COLS * CELL" :height="ROWS * CELL" class="board" />
      <div v-if="state.isOver" class="overlay">
        <div class="overlay__box">
          <div class="overlay__title">游戏结束</div>
          <div class="overlay__score">得分 {{ state.score }}</div>
          <button class="overlay__btn" @click="reset">重开一局</button>
        </div>
      </div>
    </div>
    <p class="hint">方向键 / WASD 控制 · 空格重开</p>
  </GameShell>
</template>

<style scoped>
.meta {
  font-size: 18px;
  margin-bottom: 12px;
  font-weight: 600;
}
.board-wrap {
  position: relative;
}
.board {
  border: 2px solid #374151;
  border-radius: 4px;
  display: block;
}
.overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(17, 24, 39, 0.7);
  border-radius: 4px;
}
.overlay__box {
  text-align: center;
  color: #ffffff;
}
.overlay__title {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 8px;
}
.overlay__score {
  font-size: 16px;
  margin-bottom: 16px;
  opacity: 0.9;
}
.overlay__btn {
  padding: 8px 20px;
  font-size: 14px;
  border: none;
  border-radius: 6px;
  background: #22c55e;
  color: #ffffff;
  cursor: pointer;
}
.overlay__btn:hover {
  background: #16a34a;
}
.hint {
  margin-top: 16px;
  font-size: 13px;
  color: #6b7280;
}
</style>
