import Vue from 'vue'
import Router from 'vue-router'
import NewUser from "@/views/users/NewUser";
import FillerArchive from "@/views/filler/FillerArchive.vue";
import Filler from "@/views/filler/Filler.vue";
import Register from "@/views/Register.vue";
import Auth from "@/services/Auth.vue";
import UsersDashboard from "@/views/users/UsersDashboard.vue";

// Containers
const TheContainer = () => import('@/containers/TheContainer')

// Views
const Dashboard = () => import('@/views/filler/Filler')

// Views - Pages
const Page404 = () => import('@/views/Page404')
const Page500 = () => import('@/views/Page500')
const Login = () => import('@/views/Login')

// Users
const Users = () => import('@/views/users/Users');

// Settings
const About = () => import('@/views/about/About');

Vue.use(Router);

export default new Router({
    mode: 'hash', // https://router.vuejs.org/api/#mode
    linkActiveClass: 'active',
    scrollBehavior: () => ({y: 0}),
    routes: configRoutes()
})

function configRoutes() {
    return [
        {
            path: '/',
            name: 'Главная',
            component: TheContainer,
            children: [
                {
                    path: '',
                    component: Dashboard
                },
                {
                    path: 'fill',
                    name: 'Наполнение',
                    component: Filler
                },
                {
                    path: 'ontologies',
                    name: 'Архив',
                    component: FillerArchive
                },
                {
                    path: 'users',
                    name: 'Пользователи',
                    component: {
                        render(c) {
                            return c('router-view');
                        }
                    },
                    children: [
                        {
                            path: '',
                            name: "",
                            component: UsersDashboard
                        },
                        {
                            path: 'add',
                            name: "Добавить пользователя",
                            component: NewUser
                        },
                    ]
                },
                {
                    path: 'about',
                    name: 'О программе',
                    component: About
                }
            ]
        },
        {
            path: '/404',
            name: 'Page404',
            component: Page404
        },
        {
            path: '/500',
            name: 'Page500',
            component: Page500
        },
        {
            path: '/login',
            name: 'Login',
            component: Login
        },
        {
            path: '/register',
            name: 'Register',
            component: Register
        },
        {
            path: '/logout',
            name: 'Logout',
            beforeEnter: (to, from, next) => {
                console.log('logout');
                Auth.credentialsLogout();
                next('/login');
            }
        }
    ]
}

