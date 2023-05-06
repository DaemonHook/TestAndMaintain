import { createRouter, createWebHashHistory } from 'vue-router'
import Q1View from "../views/question1-view"
import Q2View from "../views/question2-view"
import Q3View from "../views/question3-view"

const routes = [
    {
        path:"/",
        component:Q1View
    },
    {
        path:"/question2",
        component:Q2View
    },
    {
        path:"/question3",
        component:Q3View
    }
]

const router = createRouter({
    history:createWebHashHistory(),
    routes
})

export default router;