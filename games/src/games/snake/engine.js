export const DIRECTIONS = {
  up: { row: -1, col: 0 },
  down: { row: 1, col: 0 },
  left: { row: 0, col: -1 },
  right: { row: 0, col: 1 },
}

export function createInitialState({ rows = 20, cols = 20 } = {}) {
  const headRow = Math.floor(rows / 2)
  const headCol = Math.floor(cols / 2)
  const snake = [
    { row: headRow, col: headCol },
    { row: headRow, col: headCol - 1 },
    { row: headRow, col: headCol - 2 },
  ]
  const state = {
    rows,
    cols,
    snake,
    direction: { ...DIRECTIONS.right },
    food: null,
    score: 0,
    isOver: false,
  }
  return { ...state, food: placeFood(state) }
}

export function placeFood(state, rng = Math.random) {
  const occupied = new Set(state.snake.map((c) => `${c.row},${c.col}`))
  const free = []
  for (let row = 0; row < state.rows; row++) {
    for (let col = 0; col < state.cols; col++) {
      if (!occupied.has(`${row},${col}`)) {
        free.push({ row, col })
      }
    }
  }
  if (free.length === 0) return null
  return free[Math.floor(rng() * free.length)]
}

function isOpposite(a, b) {
  return a.row === -b.row && a.col === -b.col
}

export function setDirection(state, next) {
  if (isOpposite(next, state.direction)) {
    return { ...state, isOver: true }
  }
  return { ...state, direction: { ...next } }
}

export function tick(state, rng = Math.random) {
  if (state.isOver) return state
  const head = state.snake[0]
  const newHead = {
    row: head.row + state.direction.row,
    col: head.col + state.direction.col,
  }
  if (
    newHead.row < 0 ||
    newHead.row >= state.rows ||
    newHead.col < 0 ||
    newHead.col >= state.cols
  ) {
    return { ...state, isOver: true }
  }
  const ateFood =
    state.food && newHead.row === state.food.row && newHead.col === state.food.col
  const bodyWithoutTail = ateFood ? state.snake : state.snake.slice(0, -1)
  const hitsSelf = bodyWithoutTail.some(
    (c) => c.row === newHead.row && c.col === newHead.col
  )
  if (hitsSelf) {
    return { ...state, isOver: true }
  }
  const newSnake = [newHead, ...bodyWithoutTail]
  let food = state.food
  let score = state.score
  if (ateFood) {
    score += 10
    food = placeFood({ ...state, snake: newSnake }, rng)
  }
  return { ...state, snake: newSnake, food, score }
}
