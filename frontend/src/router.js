import VueRouter from "vue-router"
import SignIn from "@/views/auth/SignIn";
import SignUp from "@/views/auth/SignUp";
import ChangeInitPassword from "@/views/auth/ChangeInitPassword";
import RequestResetPassword from "@/views/auth/RequestResetPassword";
import ResetPassword from "@/views/auth/ResetPassword";
import Folder from "@/views/folders/Folder";

let routes = [
    {
        path: '/sign-in',
        name: 'sign-in',
        component: SignIn,
        meta: {
            title: 'Sign in'
        }
    },
    {
        path: '/sign-up',
        name: 'sign-up',
        component: SignUp,
        meta: {
            title: 'Sign up'
        }
    },
    {
        path: '/change-init-password',
        name:'change-init-password',
        component: ChangeInitPassword,
        meta: {
            title: 'Change password'
        }
    },
    {
        path: '/req-reset-password',
        name: 'req-reset-password',
        component: RequestResetPassword,
        meta: {
            title: 'Forgot password'
        }
    },
    {
        path: '/reset-password',
        name: 'reset-password',
        component: ResetPassword,
        meta: {
            title: 'Reset password'
        }
    },
    {
        path: '/folders/:folderId',
        name: 'folders',
        component: Folder,
        meta: {
            requireAuth: true,
            title: 'Template'
        }
    },
];

const router = new VueRouter({mode: 'history', routes});
router.beforeEach((to, from, next) => {
    let token = localStorage.getItem('token');
    const requireAuth = to.matched.some(route => route.meta.requireAuth);
    if (requireAuth && !token) {
        return next('/sign-in');
    } else if (token && !requireAuth && to.path !== '/folders/0') {
        return next('/folders/0');
    }
    document.title = to.meta.title
    return next();
});

export default router
