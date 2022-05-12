import { createRouter, createWebHashHistory } from 'vue-router'

const index = {
  '/': () => import('./views/Home.vue'),
  '/login': () => import('./views/Login.vue'),
  '/register': () => import('./views/Register.vue'),
  '/friend': () => import('./views/Friend.vue'),
  '/chat': () => import('./views/Chat.vue'),
  '/test': () => import('./views/test.vue'),
  '/about': () => import('./views/About.vue'),
  '/forum': () => import('./views/Forum.vue'),
  '/homePage': () => import('./views/HomePage.vue')
}

const routes = []
for (const r in index) routes.push({ path: r, component: index[r] })
export default createRouter({ history: createWebHashHistory(), routes })
