export default {
    id: state => state.folder.id,
    name: state => state.folder.name,
    parentFolder: state => state.folder.parentFolder,
    subFolders: state => state.subFolders,
    subFolderNames: state => state.subFolders.map(subFolder => subFolder.name),
    templates: state => state.templates,
    clipboard: state => state.clipboard,
    status: state => state.status
}