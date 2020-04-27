export default {
    submit: state => {
        state.status = 'SUBMITTING'
    },
    resetStatus: state => {
        state.status = ''
    },
    signIn: (state, payload) => {
        let code = payload.data.statusCode;
        if (code === '600') {
            state.status = 'FAILED';
        } else {
            localStorage.setItem('token', payload.data.token);
            state.user = payload.data.user;
            state.status = '';
        }
    },
    signUp: (state, payload) => {
        let code = payload.data.statusCode;
        if (code) {
            state.status = 'FAILED';
        } else {
            state.status = '';
        }
    },
    changeInitPassword: (state, payload) => {
        let code = payload.data.statusCode;
        if (code === '600' || code === '602') {
            state.status = 'FAILED';
        } else {
            state.status = '';
        }
    },
    requestResetPassword: (state, payload) => {
        state.status = '';
    },
    resetPassword: (state, payload) => {
        let code = payload.data.statusCode;
        if (code) {
            state.status = 'FAILED';
        } else {
            state.status = '';
        }
    }
}