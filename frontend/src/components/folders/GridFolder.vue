<template>
    <div
        v-click-outside="handleFocusOutside"
        :class="{'folder': true, 'folder-focus': folderFocus}"
        @click="handleFocus"
        @contextmenu="handleFocus"
        @dblclick="handleDoubleClick"
    >
        <div class="folder-content-wrapper">
            <div class="folder-content">
                <div class="folder-icon">
                    <font-awesome-icon
                        :icon="['fas', 'folder']"
                        class="folder-icon-svg"
                    />
                </div>
                <div
                    :id="tooltipFolderId"
                    :class="{'folder-name': true, 'folder-name-focus': folderFocus}"
                >
                    {{ folder.name }}
                </div>
                <b-tooltip
                    :target="tooltipFolderId"
                    triggers="hover"
                >
                    {{ $props.folder.name }}
                </b-tooltip>
            </div>
        </div>
        <b-modal
            :id="renameFolderId"
            hide-footer
            centered
        >
            <template
                #modal-title
            >
                Rename
            </template>
            <div class="d-block text-center">
                <b-form-input
                    v-model="newName"
                    placeholder="Folder name"
                />
            </div>
            <b-button
                class="mt-3 mr-3"
                variant="primary"
                :disabled="newName === '' || $store.getters['folders/subFolderNames'].includes(newName)"
                @click="renameFolder"
            >
                OK
            </b-button>
            <b-button
                class="mt-3"
                variant="light"
                @click="$bvModal.hide(folderId)"
            >
                Cancel
            </b-button>
        </b-modal>
        <b-modal
            :id="duplicateFolderId"
            hide-footer
            centered
        >
            <template
                #modal-title
            >
                Duplicate folder
            </template>
            <div class="d-block text-center">
                <b-form-input
                    v-model="duplicateFolderName"
                    placeholder="Folder name"
                />
            </div>
            <b-button
                class="mt-3 mr-3"
                variant="primary"
                :disabled="duplicateFolderName === '' || $store.getters['folders/subFolderNames'].includes(duplicateFolderName)"
                @click="duplicateFolder"
            >
                OK
            </b-button>
            <b-button
                class="mt-3"
                variant="light"
                @click="$bvModal.hide(duplicateFolderId)"
            >
                Cancel
            </b-button>
        </b-modal>
    </div>
</template>

<script>
    import {faFolder} from '@fortawesome/free-solid-svg-icons'
    import {library} from '@fortawesome/fontawesome-svg-core'
    import ClickOutside from 'vue-click-outside'

    library.add(faFolder)

    export default {
        name: "GridFolder",
        directives: {
            ClickOutside
        },
        props: {
            folder: {
                type: Object,
                required: true
            }
        },
        data: function () {
            return {
                folderFocus: false,
                newName: this.$props.folder.name,
                duplicateFolderName: `${this.$props.folder.name}(Copy)`
            }
        },
        computed: {
            renameFolderId: function () {
                return `modal-rename-folder-${this.$props.folder.id}`
            },
            duplicateFolderId: function () {
                return `modal-duplicate-folder-${this.$props.folder.id}`
            },
            tooltipFolderId: function () {
                return `tooltip-folder-${this.$props.folder.id}`
            }
        },
        watch: {
            '$route'(to, from) {
                this.$store.dispatch('folders/fetchFolders', this.$route.params.folderId)
            }
        },
        methods: {
            handleFocus: function () {
                this.folderFocus = true
            },
            handleFocusOutside: function () {
                this.folderFocus = false
            },
            showRenameModal: function () {
                this.$bvModal.show(this.renameFolderId)
            },
            renameFolder: function () {
                this.$store.dispatch('folders/renameFolder', {
                    'id': this.folder.id,
                    'name': this.newName
                })
                this.$bvModal.hide(this.renameFolderId)
            },
            handleDoubleClick: function () {
                this.$router.push({name: 'folders', params: {folderId: this.folder.id}})
            },
            showDuplicateModal: function () {
                this.$bvModal.show(this.duplicateFolderId)
            },
            duplicateFolder: function () {
                this.$store.dispatch('folders/duplicateFolder', {
                    folderId: this.$props.folder.id,
                    name: this.duplicateFolderName
                })
                this.$bvModal.hide(this.duplicateFolderId)
            }
        },
    }
</script>

<style scoped>
    .folder {
        width: 100%;
        height: 50px;
        border: 1px solid #CCCCCC;
        border-radius: 5px;
        padding: 10px;
        min-width: 100px;
        z-index: 3;
        position: relative;
    }

    .folder-focus {
        background-color: #E8F0FE;
    }

    .folder-content {
        user-select: none;
    }

    .folder-content-wrapper {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .folder-name {
        width: 60%;
        display: inline-block;
        padding-left: 20px;
        color: #565656;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        position: relative;
        top: 5px;
        border-radius: 5px;
    }

    .folder-name-focus {
        color: #1A73E8;
    }

    .folder-icon {
        width: 25px;
        display: inline-block;
    }

    .folder-icon-svg {
        font-size: 24px;
        color: #565656
    }

</style>