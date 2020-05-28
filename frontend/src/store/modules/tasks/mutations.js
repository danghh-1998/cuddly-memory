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
    },
    fetchImages: (state, payload) => {
        state.images = payload.data.images
    },
    fetchTask: (state, payload) => {
        state.task = payload
    },
    confirmResult: (state, payload) => {
        let image = state.images.find(image => {
            return image.id === payload.data.result.image.id
        })
        let result = image.results.find(result => {
            return result.id === payload.data.result.id
        })
        result.result = payload.data.result.result
    }
}
