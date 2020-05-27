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
            switch (payload.data.user.role) {
                case 0:
                    state.user.role = 'user'
                    break;
                case 1:
                    state.user.role = 'admin'
                    break;
                case 2:
                    state.user.role = 'superadmin'
                    break;
                case 3:
                    state.user.role = 'systemadmin'
            }
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
    changePassword: (state, payload) => {
        let code = payload.data.statusCode;
        if (code === '600' || code === '602') {
            state.status = 'FAILED';
        } else {
            state.status = '';
        }
    },
    requestResetPassword: (state) => {
        state.status = '';
    },
    resetPassword: (state, payload) => {
        let code = payload.data.statusCode;
        if (code) {
            state.status = 'FAILED';
        } else {
            state.status = '';
        }
    },
    signOut: state => {
        localStorage.clear()
    },
    updateProfile: () => {
        state.status = '';
    },
    listSubUsers: (state, payload) => {
        state.user.subUsers = payload.data.users
    },
    deactivateUser: (state, payload) => {
        let user = state.user.subUsers.find(item => {
            return item.id === payload.data.user.id
        })
        user.deleted = payload.data.user.deleted
    },
    activateUser: (state, payload) => {
        let user = state.user.subUsers.find(item => {
            return item.id === payload.data.user.id
        })
        user.deleted = payload.data.user.deleted
    },
    createUser: (state, payload) => {
        let code = payload.data.statusCode;
        if (code) {
            state.status = 'FAILED';
        } else {
            state.status = '';
            state.user.subUsers.push(payload.data.user)
        }
    }
}