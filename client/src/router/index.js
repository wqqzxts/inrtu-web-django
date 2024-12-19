import CharactersView from '@/views/CharactersView.vue'
import ContentView from '@/views/ContentView.vue'
import TeamsVew from '@/views/TeamsView.vue'
import PositionsVew from '@/views/PositionsView.vue'
import SkillsView from '@/views/SkillsView.vue'
import ContentTypesView from '@/views/ContentTypesView.vue'
import LoginView from '@/views/LoginView.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [  
    {
      path: "/",
      name: "CharactersView",
      component: CharactersView
    },
    {
      path: "/content",
      name: "ContentView.vue",
      component: ContentView
    },
    {
      path: "/teams",
      name: "TeamsView.vue",
      component: TeamsVew
    },
    {
      path: "/positions",
      name: "PositionsView.vue",
      component: PositionsVew
    },
    {
      path: "/skills",
      name: "SkillsView.vue",
      component: SkillsView
    },
    {
      path: "/content_type",
      name: "ContentTypesView.vue",
      component: ContentTypesView
    },
    {
      path: "/users",
      name: "LoginView.vue",
      component: LoginView
    },
  ],
})

export default router
