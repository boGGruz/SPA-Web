import {createRouter, createWebHistory, RouteRecordRaw} from 'vue-router'
import SignUp from "@/views/SignUp.vue";
import LogIn from "@/views/LogIn.vue";
import Game from "@/views/Game.vue";

const routes: Array<RouteRecordRaw> = [
    {
        path: '/sign-up',
        name: 'SignUp',
        component: SignUp
    },
    {
        path: '/',
        name: 'LogIn',
        component: LogIn
    },
    {
        path: '/samurai-way',
        name: 'Game',
        component: Game
    },
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router
