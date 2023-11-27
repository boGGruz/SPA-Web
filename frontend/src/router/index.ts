import {createRouter, createWebHistory, RouteRecordRaw} from 'vue-router'
import SignUp from "@/views/SignUp.vue";
import LogIn from "@/views/LogIn.vue";
import Game from "@/views/Game.vue";
import ScreenPlay from "@/views/ScreenPlay.vue";

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
    {
        path: '/screen-play',
        name: 'Play',
        component: ScreenPlay
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router
