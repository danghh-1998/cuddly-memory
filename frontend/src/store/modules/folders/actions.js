import api from "@/api";

export default {
    fetchFolders: (context, payload) => {
        api.defaults.headers.common.Authorization = `Token ${localStorage.getItem('token')}`;
        api.get(`folders/${payload}`)
            .then((response) => {
                context.commit('fetchFolders', response.data);
            })
    },
    copyFolder: (context, payload) => {
        context.commit('copyFolder', payload)
    },
    pasteFolder: (context, payload) => {
        context.commit('submit')
        api.defaults.headers.common.Authorization = `Token ${localStorage.getItem('token')}`;
        let clipboardFolder = payload.clipboard
        return api.post(`folders/${clipboardFolder.id}/duplicate`, {
            'folder_id': payload.folderId,
            'name': payload.clipboard.name
        }).then((response) => {
            context.commit('pasteFolder', response)
        })
    },
    renameFolder: (context, payload) => {
        api.defaults.headers.common.Authorization = `Token ${localStorage.getItem('token')}`;
        api.put(`folders/${payload.id}/update`, {
            name: payload.name
        }).then((response) => {
            context.commit('renameFolder', response)
        })
    },
    createFolder: (context, payload) => {
        api.defaults.headers.common.Authorization = `Token ${localStorage.getItem('token')}`;
        api.post('folders/create', payload)
            .then(response => {
                context.commit('createFolder', response)
            })
    },
    deleteFolder: (context, payload) => {
        api.defaults.headers.common.Authorization = `Token ${localStorage.getItem('token')}`;
        api.delete(`folders/${payload.id}/delete`)
            .then(response => {
                context.commit('deleteFolder', response)
            })
    },
    duplicateFolder: (context, payload) => {
        context.commit('submit')
        api.defaults.headers.common.Authorization = `Token ${localStorage.getItem('token')}`;
        return api.post(`folders/${payload.folderId}/duplicate`, {
            'name': payload.name
        }).then((response) => {
            context.commit('duplicateFolder', response)
        })
    },
}