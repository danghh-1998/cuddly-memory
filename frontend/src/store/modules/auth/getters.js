export default {
    submit: state => state.status,
    user: state => state.user,
    subUsers: state => state.user.subUsers,
    role: state => state.user.role
}