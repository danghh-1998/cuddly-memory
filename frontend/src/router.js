import VueRouter from "vue-router"
import SignIn from "@/views/auth/SignIn";
import SignUp from "@/views/auth/SignUp";
import ChangeInitPassword from "@/views/auth/ChangeInitPassword";
import Home from "@/views/Home";
import RequestResetPassword from "@/views/auth/RequestResetPassword";
import ResetPassword from "@/views/auth/ResetPassword";
import Folder from "@/views/folders/Folder";

let routes = [
    {path: '/', name: 'home', component: Home},
    {path: '/sign-in', name: 'sign-in', component: SignIn},
    {path: '/sign-up', name: 'sign-up', component: SignUp},
    {path: '/change-init-password', name: 'change-init-password', component: ChangeInitPassword},
    {path: '/req-reset-password', name: 'req-reset-password', component: RequestResetPassword},
    {path: '/reset-password', name: 'reset-password', component: ResetPassword},
    {
        path: '/folders/:folderId',
        name: 'folders',
        component: Folder,
        meta: {
            requireAuth: true
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
    return next();
});

export default router
