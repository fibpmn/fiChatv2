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
    path: '/startproces',
    name: 'StartProces',
    component: () => import('../views/StartProces.vue')
  },
  {
    path: '/usertaskForm',
    name: 'UserTaskForm',
    component: () => import('../views/UserTaskForm.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
