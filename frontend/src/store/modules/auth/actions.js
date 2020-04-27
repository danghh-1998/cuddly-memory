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
    changeInitPassword: (context, payload) => {
        context.commit('submit');
        api.defaults.headers.common.Authorization = `Token ${localStorage.getItem('token')}`;
        return api.put('users/change_password', payload)
            .then((res) => {
                context.commit('changeInitPassword', res)
            })
    }
}
