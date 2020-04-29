import VueRouter from "vue-router"
import SignIn from "@/views/SignIn";
import SignUp from "@/views/SignUp";
import ChangeInitPassword from "@/views/ChangeInitPassword";
import Home from "@/views/Home";
import RequestResetPassword from "@/views/RequestResetPassword";
import ResetPassword from "@/views/ResetPassword";

let routes = [
    {
        path: '/',
        name: 'home',
        component: Home,
        meta: {
            requireAuth: true
        }
    },
    {
        path: '/sign-in',
        name: 'sign-in',
        component: SignIn
    },
    {
        path: '/sign-up',
        name: 'sign-up',
        component: SignUp
    },
    {
        path: '/change-init-password',
        name: 'change-init-password',
        component: ChangeInitPassword
    },
    {
        path: '/req-reset-password',
        name: 'req-reset-password',
        component: RequestResetPassword
    },
    {
        path: '/reset-password',
        name: 'reset-password',
        component: ResetPassword
    }
];

const router = new VueRouter({mode: 'history', routes});
router.beforeEach((to, from, next) => {
    let token = localStorage.getItem('token');
    const requireAuth = to.matched.some(route => route.meta.requireAuth);
    if (requireAuth && !token) {
        return next('/sign-in');
    } else if (token && !requireAuth && to.path !== '/') {
        return next('/');
    }
    return next();
});

export default router
