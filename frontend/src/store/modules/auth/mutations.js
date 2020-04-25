export default {
    submit: state => {
        state.status = 'SUBMITTING'
    },
    resetStatus: state => {
        state.status = ''
    },
    signIn: (state, payload) => {
        let code = payload.data.statusCode;
        if (code) {
            state.status = 'FAILED';
        } else {
            localStorage.setItem('token', payload.data.token);
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
    }
}