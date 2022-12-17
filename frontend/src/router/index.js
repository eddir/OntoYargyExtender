import Vue from 'vue'
import Router from 'vue-router'
import NewUser from "@/views/users/NewUser";
import OntologiesPanel from "@/views/ontologies/OntologiesPanel.vue";

// Containers
const TheContainer = () => import('@/containers/TheContainer')

// Views
const Dashboard = () => import('@/views/Dashboard')

// Views - Pages
const Page404 = () => import('@/views/Page404')
const Page500 = () => import('@/views/Page500')
const Login = () => import('@/views/Login')

// Users
const Users = () => import('@/views/users/Users');

// Settings
const Settings = () => import('@/views/settings/Settings');

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
                    path: 'dashboard',
                    name: 'Главная',
                    component: Dashboard
                },
                {
                    path: 'ontologies',
                    meta: {
                        label: 'Ontologies'
                    },
                    component: {
                        render(c) {
                            return c('router-view')
                        }
                    },
                    children: [
                        {
                            path: '',
                            name: 'Ontologies List',
                            component: OntologiesPanel
                        },
                    ]
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
                            name: "Users",
                            component: Users
                        },
                        {
                            path: 'add',
                            name: "Add user",
                            component: NewUser
                        },
                    ]
                },
                {
                    path: 'settings',
                    name: 'Настройки',
                    component: Settings
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
    ]
}

