export default {
    submit: state => {
        state.status = 'SUBMITTING'
    },
    fetchFolders: (state, payload) => {
        state.folder = {
            id: payload.folder.id,
            name: payload.folder.name,
            parentFolder: payload.folder.parentFolder,
        };
        state.subFolders = payload.folder.subFolders;
        state.templates = payload.folder.templates;
    },
    copyFolder: (state, payload) => {
        state.clipboard = payload
    },
    pasteFolder: (state, payload) => {
        let code = payload.data.statusCode;
        if (code === '606') {
            state.status = 'DUPLICATED'
        } else if (code === '602') {
            state.status = 'ERROR'
        } else {
            state.status = ''
            state.subFolders.push(payload.data.folder)
        }
    },
    renameFolder: (state, payload) => {
        let targetFolder = state.subFolders.find(subFolder => subFolder.id === payload.data.folder.id)
        targetFolder.name = payload.data.folder.name
    },
    createFolder: (state, payload) => {
        delete payload.data.folder.subFolders
        delete payload.data.folder.templates
        state.subFolders.push(payload.data.folder)
    },
    deleteFolder: (state, payload) => {
        state.subFolders = state.subFolders.filter(subFolder => subFolder.id !== payload.data.folder.id)
    },
    duplicateFolder: (state, payload) => {
        let code = payload.data.statusCode;
        if (code === '606') {
            state.status = 'DUPLICATED'
        } else {
            state.status = ''
            state.subFolders.push(payload.data.folder)
        }
    }
}