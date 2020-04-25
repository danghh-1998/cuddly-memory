import VueRouter from "vue-router"
import SignIn from "@/views/SignIn";
import SignUp from "@/views/SignUp";

let routes = [
    {path: '/', name: 'sign-in', component: SignIn},
    {path: '/sign-up', name: 'sign-up', component: SignUp},
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
