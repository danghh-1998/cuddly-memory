export default {
    fetchTasks: (state, payload) => {
        state.tasks = payload.data.tasks
    },
    cancelTask: (state, payload) => {
        let index = state.tasks.findIndex(task => {
            return task.id === payload.data.task.id
        })
        state.tasks.splice(index, 1)
    },
    createTask: (state, payload) => {
        state.tasks.push(payload.data.task)
    },
    updateTask: (state, payload) => {
        let task = state.tasks.find(task => {
            return task.id === payload.data.task.id
        })
        task.status = payload.data.task.status
    }
}
