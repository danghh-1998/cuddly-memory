import api from "@/api";

export default {
    resetStatus: context => {
        context.commit('resetStatus');
    },
    signIn: (context, payload) => {
        context.commit('submit');
        return api.post('auth/sign_in', payload)
            .then((res) => {
                context.commit('signIn', res);
            })
    },
    signUp: (context, payload) => {
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
        context.commit('submit');
        return api.post('users/req_reset_password', payload)
            .then((res) => {
                context.commit('requestResetPassword', res)
            })
    },
    resetPassword: (context, payload) => {
        context.commit('submit');
        return api.put('users/reset_password', payload)
            .then((res) => {
                context.commit('resetPassword', res)
            })
    },
    signOut: context => {
        context.commit('signOut')
    },
    updateProfile: (context, payload) => {
        context.commit('submit');
        api.defaults.headers.common.Authorization = `Token ${localStorage.getItem('token')}`;
        return api.put(`users/update`, payload)
            .then((res) => {
                context.commit('updateProfile', res)
            })
    }
}
