import {api} from "@/api";
import FormData from "form-data";

export default {

    fetchTasks: (context) => {
        api.defaults.headers.common.Authorization = `Token ${localStorage.getItem('token')}`;
        return api.get('tasks')
            .then((res) => {
                context.commit('fetchTasks', res)
            })
    },
    updateTask: (context, payload) => {
        api.defaults.headers.common.Authorization = `Token ${localStorage.getItem('token')}`;
        return api.put(`tasks/${payload.id}/update`, {
            status: payload.status
        })
            .then((res) => {
                context.commit('updateTask', res)
            })
    },
    cancelTask: (context, payload) => {
        api.defaults.headers.common.Authorization = `Token ${localStorage.getItem('token')}`;
        return api.delete(`tasks/${payload}/delete`)
            .then((res) => {
                context.commit('cancelTask', res)
            })
    },
    createTask: (context, payload) => {
        api.defaults.headers.common.Authorization = `Token ${localStorage.getItem('token')}`;
        let formData = new FormData()
        formData.append('template_id', payload.template_id)
        formData.append('file', payload.file)
        return api.post(`tasks/create`, formData)
            .then((res) => {
                context.commit('createTask', res)
            })
    }
}
