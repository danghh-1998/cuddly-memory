<template>
    <folder-layout>
        <template
            #folder-group
        >
            <b-row>
                <b-col
                    v-for="folder in subFolders"
                    :key="folder.id"
                    xl="2"
                    lg="2"
                    md="4"
                    sm="4"
                    cols="6"
                    class="folder-item"
                >
                    <grid-folder
                        ref="folders"
                        v-contextmenu:contextmenufolder
                        :folder="folder"
                    />
                </b-col>
            </b-row>
            <v-contextmenu
                ref="contextmenufolder"
                class="context-menu"
                @contextmenu="handleContextMenu"
            >
                <v-contextmenu-item
                    @click="openFolder"
                >
                    <font-awesome-icon
                        :icon="['fas', 'folder-open']"
                        class="content-menu-icon"
                    />
                    <span class="content-menu-text">Open</span>
                </v-contextmenu-item>
                <div
                    :class="{hidden: $store.getters['auth/role'] !== 'admin'}"
                >
                    <v-contextmenu-item divider />
                    <v-contextmenu-item
                        @click="copyFolder"
                    >
                        <font-awesome-icon
                            :icon="['fas', 'copy']"
                            class="content-menu-icon"
                        />
                        <span class="content-menu-text">Copy</span>
                    </v-contextmenu-item>
                    <v-contextmenu-item divider />
                    <v-contextmenu-item
                        @click="renameFolder"
                    >
                        <font-awesome-icon
                            :icon="['fas', 'pen']"
                            class="content-menu-icon"
                        />
                        <span class="content-menu-text">Rename</span>
                    </v-contextmenu-item>
                    <v-contextmenu-item divider />
                    <v-contextmenu-item
                        @click="duplicateFolder"
                    >
                        <font-awesome-icon
                            :icon="['fas', 'clone']"
                            class="content-menu-icon"
                        />
                        <span class="content-menu-text">Duplicate folder</span>
                    </v-contextmenu-item>
                    <v-contextmenu-item divider />
                    <v-contextmenu-item
                        @click="deleteFolder"
                    >
                        <font-awesome-icon
                            :icon="['fas', 'trash-alt']"
                            class="content-menu-icon"
                        />
                        <span class="content-menu-text">Delete</span>
                    </v-contextmenu-item>
                </div>
            </v-contextmenu>
        </template>
        <template
            #template-group
        >
            <b-row>
                <b-col
                    v-for="template in templates"
                    :key="template.id"
                    xl="2"
                    lg="2"
                    md="4"
                    sm="4"
                    cols="6"
                >
                    <grid-template
                        ref="templates"
                        v-contextmenu:contextmenutemplate
                        :template="template"
                    />
                </b-col>
            </b-row>
            <v-contextmenu
                ref="contextmenutemplate"
                @contextmenu="handleContextMenu"
            >
                <v-contextmenu-item
                    @click="openTemplate"
                >
                    <font-awesome-icon
                        :icon="['fas', 'folder-open']"
                        class="content-menu-icon"
                    />
                    <span class="content-menu-text">Open</span>
                </v-contextmenu-item>
                <div
                    :class="{hidden: $store.getters['auth/role'] !== 'user'}"
                >
                    <v-contextmenu-item divider />
                    <v-contextmenu-item
                        @click="$bvModal.show('create-task')"
                    >
                        <font-awesome-icon
                            :icon="['fas', 'file-invoice']"
                            class="content-menu-icon"
                        />
                        <span class="content-menu-text">Create task</span>
                    </v-contextmenu-item>
                </div>
                <div
                    :class="{hidden: $store.getters['auth/role'] !== 'admin'}"
                >
                    <v-contextmenu-item divider />
                    <v-contextmenu-item
                        @click="copyTemplate"
                    >
                        <font-awesome-icon
                            :icon="['fas', 'copy']"
                            class="content-menu-icon"
                        />
                        <span class="content-menu-text">Copy</span>
                    </v-contextmenu-item>
                    <v-contextmenu-item divider />
                    <v-contextmenu-item
                        @click="renameTemplate"
                    >
                        <font-awesome-icon
                            :icon="['fas', 'pen']"
                            class="content-menu-icon"
                        />
                        <span class="content-menu-text">Rename</span>
                    </v-contextmenu-item>
                    <v-contextmenu-item divider />
                    <v-contextmenu-item
                        @click="duplicateTemplate"
                    >
                        <font-awesome-icon
                            :icon="['fas', 'clone']"
                            class="content-menu-icon"
                        />
                        <span class="content-menu-text">Duplicate template</span>
                    </v-contextmenu-item>
                    <v-contextmenu-item divider />
                    <v-contextmenu-item
                        @click="deleteTemplate"
                    >
                        <font-awesome-icon
                            :icon="['fas', 'trash-alt']"
                            class="content-menu-icon"
                        />
                        <span class="content-menu-text">Delete</span>
                    </v-contextmenu-item>
                </div>
            </v-contextmenu>
            <b-modal
                id="create-task"
                hide-footer
                centered
            >
                <template
                    #modal-title
                >
                    Create task
                </template>
                <div>
                    <span>Upload images</span>
                    <b-form-file
                        v-model="taskFile"
                        :state="Boolean(taskFile)"
                        class="mt-4"
                        placeholder="Upload images"
                        drop-placeholder="Drop file here"
                        accept=".jpg .png .jpeg .zip"
                    />
                </div>
                <b-button
                    class="mt-3 mr-3"
                    variant="primary"
                    @click="createTask"
                >
                    OK
                </b-button>
                <b-button
                    class="mt-3"
                    variant="light"
                    @click="$bvModal.hide('create-task')"
                >
                    Cancel
                </b-button>
            </b-modal>
        </template>
    </folder-layout>
</template>

<script>
    import FolderLayout from "@/components/folders/FolderLayout";
    import GridFolder from "@/components/folders/GridFolder";
    import GridTemplate from "@/components/folders/GridTemplate";

    import {faFolderOpen} from '@fortawesome/free-solid-svg-icons'
    import {faCopy} from '@fortawesome/free-solid-svg-icons'
    import {faPaste} from '@fortawesome/free-solid-svg-icons'
    import {faPen} from '@fortawesome/free-solid-svg-icons'
    import {faClone} from '@fortawesome/free-solid-svg-icons'
    import {faTrashAlt} from '@fortawesome/free-solid-svg-icons'
    import {faFileInvoice} from '@fortawesome/free-solid-svg-icons'
    import {library} from '@fortawesome/fontawesome-svg-core'

    library.add(faFolderOpen)
    library.add(faCopy)
    library.add(faPaste)
    library.add(faPen)
    library.add(faClone)
    library.add(faTrashAlt)
    library.add(faFileInvoice)

    export default {
        name: "Folder",
        components: {
            GridTemplate,
            FolderLayout,
            GridFolder,
        },
        data: function () {
            return {
                targetObject: null,
                taskFile: null
            }
        },
        computed: {
            id: function () {
                return this.$store.getters['folders/id']
            },
            parentFolder: function () {
                return this.$store.getters['folders/parentFolder']
            },
            subFolders: function () {
                return this.$store.getters['folders/filteredFolders']
            },
            templates: function () {
                return this.$store.getters['folders/filteredTemplates']
            },
            clipboard: function () {
                return this.$store.getters['folders/clipboard']
            }
        },
        watch: {
            '$route'() {
                this.$store.dispatch('folders/fetchFolders', this.$route.params.folderId)
            }
        },
        created() {
            this.$store.dispatch('folders/fetchFolders', this.$route.params.folderId)
        },
        methods: {
            openFolder: function () {
                this.$router.push({name: 'folders', params: {folderId: this.targetObject.id}})
            },
            handleContextMenu: function (vm) {
                let instance = vm.componentInstance
                if (instance.folder) {
                    this.targetObject = instance.folder
                } else {
                    this.targetObject = instance.template
                }
            },
            copyFolder: function () {
                this.$store.dispatch('folders/copyFolder', {
                    type: 'FOLDER',
                    object: this.targetObject
                })
            },
            renameFolder: function () {
                this.$refs.folders.find((ref) => ref.folder.id === this.targetObject.id).showRenameModal()
            },
            deleteFolder: function () {
                this.$store.dispatch('folders/deleteFolder', this.targetObject)
            },
            duplicateFolder: function () {
                this.$refs.folders.find((ref) => ref.folder.id === this.targetObject.id).showDuplicateModal()
            },
            openTemplate: function () {
                this.$store.dispatch('templates/fetchTemplate', this.targetObject.id)
                    .then(() => {
                        this.$router.push({name: 'templates', params: {templateId: this.targetObject.id}})
                    })
            },
            deleteTemplate: function () {
                this.$store.dispatch('folders/deleteTemplate', this.targetObject)
            },
            renameTemplate: function () {
                this.$refs.templates.find((ref) => ref.template.id === this.targetObject.id).showRenameModal()
            },
            copyTemplate: function () {
                this.$store.dispatch('folders/copyTemplate', {
                    type: 'TEMPLATE',
                    object: this.targetObject
                })
            },
            duplicateTemplate: function () {
                this.$refs.templates.find((ref) => ref.template.id === this.targetObject.id).showDuplicateModal()
            },
            createTask: function () {
                this.$store.dispatch('tasks/createTask', {
                    template_id: this.targetObject.id,
                    file: this.taskFile
                })
                    .then(() => {
                        this.$router.push('/tasks')
                    })
            }
        }
    }
</script>

<style scoped>
    .folder-item {
        margin-bottom: 20px;
    }

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

    .content-menu {
    }

    .hidden {
        display: none;
    }
</style>
