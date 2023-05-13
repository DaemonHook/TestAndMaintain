import { createRouter, createWebHashHistory, createWebHistory } from 'vue-router'
// import HomeView from '../views/HomeView.vue'
import HomePage from '../views/HomePage.vue'
import Question1 from '../views/Question1.vue'
import Question2 from '../views/Question2.vue'
import Question3 from '../views/Question3.vue'

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage,
      redirect: '/q1',
      children: [
        {
          path: 'q1',
          name: 'q1',
          component: Question1
        },
        {
          path: 'q2',
          name: 'q2',
          component: Question2
        },
        {
          path: 'q3',
          name: 'q3',
          component: Question3
        }
      ]
    },
    
  ]
})

export default router
