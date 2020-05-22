export default {
    uploadTemplate: (state, payload) => {
        state.image = payload.data
        state.template.name = payload.templateName
    },
    fetchTemplate: (state, payload) => {
        state.image = payload.image
        state.boundingBoxes = payload.template.boundingBoxes
        state.folder = payload.template.folder
        state.template.id = payload.template.id
        state.template.name = payload.template.name
    }
}
