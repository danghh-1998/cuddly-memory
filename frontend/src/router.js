import VueRouter from "vue-router"
import SignIn from "@/views/auth/SignIn";
import SignUp from "@/views/auth/SignUp";
import ChangeInitPassword from "@/views/auth/ChangeInitPassword";
import RequestResetPassword from "@/views/auth/RequestResetPassword";
import ResetPassword from "@/views/auth/ResetPassword";
import Folder from "@/views/folders/Folder";
import Profile from "@/views/auth/Profile";
import Template from "@/views/templates/Template";
import TemplateCreate from "@/views/templates/TemplateCreate";
import Management from "@/views/auth/Management";

let routes = [
    {
        path: '/sign-in',
        name: 'sign-in',
        component: SignIn,
        meta: {
            title: 'Sign in',
            requireRoles: ['guest']
        }
    },
    {
        path: '/sign-up',
        name: 'sign-up',
        component: SignUp,
        meta: {
            title: 'Sign up',
            requireRoles: ['guest']
        }
    },
    {
        path: '/change-init-password',
        name: 'change-init-password',
        component: ChangeInitPassword,
        meta: {
            title: 'Change password',
            requireRoles: ['guest']
        }
    },
    {
        path: '/req-reset-password',
        name: 'req-reset-password',
        component: RequestResetPassword,
        meta: {
            title: 'Forgot password',
            requireRoles: ['guest']
        }
    },
    {
        path: '/reset-password',
        name: 'reset-password',
        component: ResetPassword,
        meta: {
            title: 'Reset password',
            requireRoles: ['guest']
        }
    },
    {
        path: '/folders/:folderId',
        name: 'folders',
        component: Folder,
        meta: {
            title: 'Template',
            requireRoles: ['user', 'admin']
        }
    },
    {
        path: '/profile',
        name: 'profile',
        component: Profile,
        meta: {
            title: 'Profile',
            requireRoles: ['user', 'admin', 'superadmin']
        }
    },
    {
        path: '/templates',
        name: 'create-template',
        component: TemplateCreate,
        meta: {
            title: 'Create template',
            requireRoles: ['admin']
        }
    },
    {
        path: '/templates/:templateId',
        name: 'templates',
        component: Template,
        meta: {
            title: 'Template',
            requireRoles: ['user', 'admin']
        }
    },
    {
        path: '/user-management',
        name: 'user-management',
        component: Management,
        meta: {
            title: 'User management',
            requireRoles: ['admin', 'superadmin']
        }
    }
];

const router = new VueRouter({mode: 'history', routes});
router.beforeEach((to, from, next) => {
    let vuex = JSON.parse(localStorage.getItem('vuex'))
    let role = 'guest'
    if (vuex) {
        role = vuex.auth.user.role
    }
    const requireRoles = to.matched.some(route => route.meta.requireRoles.includes(role));
    if (!requireRoles) {
        return next('/sign-in');
    }
    document.title = to.meta.title
    return next();
});

export default router
