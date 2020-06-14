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
        state.filteredFolders = state.subFolders;
        state.templates = payload.folder.templates;
        state.filteredTemplates = state.templates
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
            state.clipboard = null
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
    },
    deleteTemplate: (state, payload) => {
        state.templates = state.templates.filter(template => template.id !== payload.data.template.id)
    },
    renameTemplate: (state, payload) => {
        let targetTemplate = state.templates.find(template => template.id === payload.data.template.id)
        targetTemplate.displayName = payload.data.template.displayName
    },
    copyTemplate: (state, payload) => {
        state.clipboard = payload
    },
    pasteTemplate: (state, payload) => {
        let code = payload.data.statusCode;
        if (code === '606') {
            state.status = 'DUPLICATED'
        } else {
            state.status = ''
            state.templates.push(payload.data.template)
            state.clipboard = null
        }
    },
    duplicateTemplate: (state, payload) => {
        let code = payload.data.statusCode;
        if (code === '606') {
            state.status = 'DUPLICATED'
        } else {
            state.status = ''
            state.templates.push(payload.data.template)
        }
    },
    handleSearch: (state, payload) => {
        state.filteredFolders = state.subFolders.filter(item => {
            return item.name.includes(payload)
        })
        state.filteredTemplates = state.templates.filter(item => {
            return item.displayName.includes(payload)
        })
    }
}