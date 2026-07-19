import { describe, it, expect } from 'vitest'
import {
  createInitialState,
  placeFood,
  setDirection,
  tick,
  DIRECTIONS,
} from './engine.js'

describe('createInitialState', () => {
  it('creates a 3-segment snake in the middle heading right', () => {
    const state = createInitialState({ rows: 20, cols: 20 })
    expect(state.rows).toBe(20)
    expect(state.cols).toBe(20)
    expect(state.snake).toHaveLength(3)
    expect(state.direction).toEqual(DIRECTIONS.right)
    expect(state.score).toBe(0)
    expect(state.isOver).toBe(false)
    expect(state.food).not.toBeNull()
  })

  it('does not spawn food on the snake', () => {
    const state = createInitialState({ rows: 5, cols: 5 })
    const onSnake = state.snake.some(
      (c) => c.row === state.food.row && c.col === state.food.col
    )
    expect(onSnake).toBe(false)
  })
})

describe('placeFood', () => {
  it('never lands on the snake over many samples', () => {
    const state = createInitialState({ rows: 6, cols: 6 })
    for (let i = 0; i < 50; i++) {
      const food = placeFood(state)
      const onSnake = state.snake.some((c) => c.row === food.row && c.col === food.col)
      expect(onSnake).toBe(false)
    }
  })

  it('returns null when the board is full', () => {
    const fullSnake = []
    for (let row = 0; row < 2; row++) {
      for (let col = 0; col < 2; col++) {
        fullSnake.push({ row, col })
      }
    }
    expect(placeFood({ rows: 2, cols: 2, snake: fullSnake })).toBeNull()
  })
})

describe('tick', () => {
  it('moves the snake forward without growing', () => {
    const state = createInitialState({ rows: 20, cols: 20 })
    const headBefore = state.snake[0]
    const next = tick(state)
    expect(next.snake).toHaveLength(3)
    expect(next.snake[0]).toEqual({
      row: headBefore.row,
      col: headBefore.col + 1,
    })
    expect(next.score).toBe(0)
  })

  it('grows and scores when eating food', () => {
    const state = createInitialState({ rows: 20, cols: 20 })
    const head = state.snake[0]
    const forced = { ...state, food: { row: head.row, col: head.col + 1 } }
    const next = tick(forced)
    expect(next.snake).toHaveLength(4)
    expect(next.score).toBe(10)
    const onSnake = next.snake.some(
      (c) => c.row === next.food.row && c.col === next.food.col
    )
    expect(onSnake).toBe(false)
  })

  it('ends the game when hitting a wall', () => {
    let state = createInitialState({ rows: 20, cols: 20 })
    for (let i = 0; i < 20 && !state.isOver; i++) {
      state = tick(state)
    }
    expect(state.isOver).toBe(true)
  })

  it('ends the game when hitting its own body', () => {
    const state = {
      rows: 10,
      cols: 10,
      snake: [
        { row: 5, col: 5 },
        { row: 5, col: 6 },
        { row: 4, col: 6 },
        { row: 4, col: 5 },
        { row: 4, col: 4 },
      ],
      direction: DIRECTIONS.up,
      food: { row: 0, col: 0 },
      score: 0,
      isOver: false,
    }
    const next = tick(state)
    expect(next.isOver).toBe(true)
  })

  it('does not end the game when moving into the vacating tail cell', () => {
    const state = {
      rows: 10,
      cols: 10,
      snake: [
        { row: 5, col: 5 },
        { row: 5, col: 4 },
        { row: 5, col: 3 },
      ],
      direction: DIRECTIONS.down,
      food: { row: 0, col: 0 },
      score: 0,
      isOver: false,
    }
    const next = tick(state)
    expect(next.isOver).toBe(false)
  })
})

describe('setDirection', () => {
  it('ends the game on a 180-degree reverse', () => {
    const state = createInitialState({ rows: 20, cols: 20 })
    const next = setDirection(state, DIRECTIONS.left)
    expect(next.isOver).toBe(true)
  })

  it('updates direction on a valid turn', () => {
    const state = createInitialState({ rows: 20, cols: 20 })
    const next = setDirection(state, DIRECTIONS.up)
    expect(next.direction).toEqual(DIRECTIONS.up)
    expect(next.isOver).toBe(false)
  })

  it('takes effect on the next tick', () => {
    let state = createInitialState({ rows: 20, cols: 20 })
    const headBefore = state.snake[0]
    state = setDirection(state, DIRECTIONS.up)
    state = tick(state)
    expect(state.snake[0]).toEqual({
      row: headBefore.row - 1,
      col: headBefore.col,
    })
  })
})
