import VueRouter from "vue-router"
import SignIn from "@/views/SignIn";
import SignUp from "@/views/SignUp";
import ChangeInitPassword from "@/views/ChangeInitPassword";
import Home from "@/views/Home";

let routes = [
    {path: '/', name: 'home', component: Home},
    {path: '/sign-in', name: 'sign-in', component: SignIn},
    {path: '/sign-up', name: 'sign-up', component: SignUp},
    {path: '/change-init-password', name: 'change-init-password', component: ChangeInitPassword}
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
