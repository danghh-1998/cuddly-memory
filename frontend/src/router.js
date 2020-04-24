import VueRouter from "vue-router"

let routes = [];

const router = new VueRouter({mode: 'history', routes});
router.beforeEach((to, from, next) => {
    let token = localStorage.getItem('token');
    const requireAuth = to.matched.some(route => route.meta.requireAuth);
    if (requireAuth && !token) {
        return next('/signin');
    } else if (token && !requireAuth && to.path !== '/') {
        return next('/');
    }
    return next();
});

export default router
