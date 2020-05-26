import {api} from "@/api";

export default {
    resetStatus: context => {
        context.commit('resetStatus');
    },
    signIn: (context, payload) => {
        api.defaults.headers.common.Authorization = null
        context.commit('submit');
        return api.post('auth/sign_in', payload)
            .then((res) => {
                context.commit('signIn', res);
            })
    },
    signUp: (context, payload) => {
        api.defaults.headers.common.Authorization = null
        context.commit('submit');
        return api.post('auth/sign_up', payload)
            .then((res) => {
                context.commit('signUp', res)
            })
    },
    changePassword: (context, payload) => {
        context.commit('submit');
        api.defaults.headers.common.Authorization = `Token ${localStorage.getItem('token')}`;
        return api.put('users/change_password', payload)
            .then((res) => {
                context.commit('changePassword', res)
            })
    },
    requestResetPassword: (context, payload) => {
        api.defaults.headers.common.Authorization = null
        context.commit('submit');
        return api.post('users/req_reset_password', payload)
            .then((res) => {
                context.commit('requestResetPassword', res)
            })
    },
    resetPassword: (context, payload) => {
        api.defaults.headers.common.Authorization = null
        context.commit('submit');
        return api.put('users/reset_password', payload)
            .then((res) => {
                context.commit('resetPassword', res)
            })
    },
    signOut: context => {
        api.defaults.headers.common.Authorization = `Token ${localStorage.getItem('token')}`;
        return api.delete('users/sign_out')
            .then(() => {
                context.commit('signOut')
            })
    },
    updateProfile: (context, payload) => {
        context.commit('submit');
        api.defaults.headers.common.Authorization = `Token ${localStorage.getItem('token')}`;
        return api.put(`users/update`, payload)
            .then((res) => {
                context.commit('updateProfile', res)
            })
    },
    listSubUsers: context => {
        api.defaults.headers.common.Authorization = `Token ${localStorage.getItem('token')}`;
        return api.get(`users/sub_users`)
            .then((res) => {
                context.commit('listSubUsers', res)
            })
    },
    deactivateUser: (context, payload) => {
        api.defaults.headers.common.Authorization = `Token ${localStorage.getItem('token')}`;
        return api.delete(`users/${payload}/deactivate`)
            .then((res) => {
                context.commit('deactivateUser', res)
            })
    },
    activateUser: (context, payload) => {
        api.defaults.headers.common.Authorization = `Token ${localStorage.getItem('token')}`;
        return api.put(`users/${payload}/activate`)
            .then((res) => {
                context.commit('activateUser', res)
            })
    },
    createUser: (context, payload) => {
        api.defaults.headers.common.Authorization = `Token ${localStorage.getItem('token')}`;
        context.commit('submit');
        return api.post(`users/create`, payload)
            .then((res) => {
                context.commit('createUser', res)
            })
    }
}
