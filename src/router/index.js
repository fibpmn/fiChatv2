import Vue from 'vue'
import VueRouter from 'vue-router'


Vue.use(VueRouter)

  const routes = [
  {
    path: '/',
    name: 'Chat',
    component: () => import('../components/Chat.vue')
  },
  {
    path: '/prijavateme',
    name: 'PrijavaTeme',
    component: () => import('../views/PrijavaTeme.vue')
  },
  {
    path: '/startproces',
    name: 'StartProces',
    component: () => import('../views/StartProces.vue')
  },
  {
    path: '/odluci',
    name: 'Odluci',
    component: () => import('../views/Odluci.vue')
  },
  {
    path: '/zadnjaverzija',
    name: 'ZadnjaVerzija',
    component: () => import('../views/ZadnjaVerzija.vue')
  },
  {
    path: '/zavrsi',
    name: 'Zavrsi',
    component: () => import('../views/Zavrsi.vue')
  },
  {
    path: '/usertaskForm',
    name: 'UserTaskForm',
    component: () => import('../views/UserTaskForm.vue')
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
