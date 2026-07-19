import { createRouter, createWebHistory } from 'vue-router'
import Home from './views/Home.vue'

const routes = [
  { path: '/', name: 'home', component: Home },
  {
    path: '/snake',
    name: 'snake',
    component: () => import('./games/snake/index.vue'),
  },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
