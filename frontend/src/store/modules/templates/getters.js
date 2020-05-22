export default {
    status: state => state.status,
    id: state => state.template.id,
    name: state => state.template.name,
    displayName: state => state.template.displayName,
    image: state => state.image,
    folder: state => state.template.folder,
    boundingBoxes: state => state.boundingBoxes,
}