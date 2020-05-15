<template>
    <div class="page-wrapper">
        <div
            v-contextmenu:globalcontextmenu
            class="global-context-menu"
        >
            <v-contextmenu
                ref="globalcontextmenu"
            >
                <v-contextmenu-item
                    @click="$bvModal.show('create-folder')"
                >
                    <font-awesome-icon
                        :icon="['fas', 'folder-open']"
                        class="content-menu-icon"
                    />
                    <span class="content-menu-text">Create new folder</span>
                </v-contextmenu-item>
                <v-contextmenu-item divider />
                <v-contextmenu-item>
                    <font-awesome-icon
                        :icon="['fas', 'copy']"
                        class="content-menu-icon"
                    />
                    <span class="content-menu-text">Create new template</span>
                </v-contextmenu-item>
                <v-contextmenu-item divider />
                <v-contextmenu-item
                    :disabled="clipboard === null"
                    @click="pasteFolder"
                >
                    <font-awesome-icon
                        :icon="['fas', 'paste']"
                        class="content-menu-icon"
                    />
                    <span class="content-menu-text">Paste</span>
                </v-contextmenu-item>
            </v-contextmenu>
        </div>
        <b-modal
            id="create-folder"
            hide-footer
            centered
        >
            <template
                #modal-title
            >
                Create new folder
            </template>
            <div class="d-block text-center">
                <b-form-input
                    v-model="folderName"
                    placeholder="Folder name"
                />
            </div>
            <b-button
                class="mt-3 mr-3"
                variant="primary"
                :disabled="folderName === '' || $store.getters['folders/subFolderNames'].includes(folderName)"
                @click="createFolder"
            >
                OK
            </b-button>
            <b-button
                class="mt-3"
                variant="light"
                @click="$bvModal.hide('create-folder')"
            >
                Cancel
            </b-button>
        </b-modal>
    </div>
</template>

<script>
    import {faPaste} from '@fortawesome/free-solid-svg-icons'
    import {library} from '@fortawesome/fontawesome-svg-core'

    library.add(faPaste)

    export default {
        name: "GlobalContextMenu",
        data: function () {
            return {
                folderName: ''
            }
        },
        computed: {
            clipboard: function () {
                return this.$store.getters['folders/clipboard']
            }
        },
        methods: {
            makeToast: function (message) {
                this.$bvToast.toast(message, {
                    title: 'Copy failed',
                    autoHideDelay: 4000,
                    variant: 'danger'
                })
            },
            createFolder: function () {
                let parentFolder = this.$store.getters['folders/id']
                this.$store.dispatch('folders/createFolder', {
                    'name': this.folderName,
                    'parent_folder_id': parentFolder ? parentFolder : 0
                })
                this.$bvModal.hide('create-folder')
            },
            pasteFolder: function() {
                this.$store.dispatch('folders/pasteFolder', {
                    'folderId': this.$store.getters['folders/id'],
                    'clipboard': this.$store.getters['folders/clipboard']
                })
                    .then(() => {
                        let status = this.$store.getters['folders/status'];
                        if (status === 'DUPLICATED') {
                            this.makeToast('Duplicate folder name')
                        } else if (status === 'ERROR') {
                            this.makeToast('Target folder inside source folder')
                        }
                    })
            },
        }
    }
</script>

<style scoped>
    .v-contextmenu-item {
        padding: 12px;
    }

    .content-menu-icon {
        color: #565656;
        display: inline-block;
        margin-right: 20px;
    }

    .content-menu-text {
        display: inline-block;
        margin-right: 20px;
    }
    .global-context-menu {
        height: 100%;
    }
</style>