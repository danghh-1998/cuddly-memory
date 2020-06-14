<template>
    <div class="layout">
        <app-nav-bar class="app-nav-bar" />
        <div class="page-content">
            <global-context-menu
                v-if="this.$store.getters['auth/role'] === 'admin'"
                class="global-context-menu"
            />
            <div class="wrapper">
                <div
                    class="d-flex align-items-center"
                >
                    <b-input
                        v-model:value="keyword"
                        placeholder="Search"
                        class="w-25 ml-auto search-box"
                        @keyup="handleSearch"
                    />
                </div>
                <div
                    v-if="isNoContent"
                    class="no-content"
                >
                    <div class="illistration" />
                    <p>Folders and templates appear here</p>
                </div>
                <div
                    v-else
                    class="wrap"
                >
                    <div
                        v-if="! isNoFolders"
                        class="folder-group"
                    >
                        <p class="folder-group-title">
                            Folder
                        </p>
                        <b-container
                            fluid="true"
                            class="folder-group-content"
                        >
                            <slot name="folder-group" />
                        </b-container>
                    </div>
                    <div
                        v-if="! isNoTemplates"
                        class="template-group"
                    >
                        <p class="template-group-title">
                            Template
                        </p>
                        <b-container
                            fluid="true"
                            class="template-group-content"
                        >
                            <slot name="template-group" />
                        </b-container>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import {faSearch} from '@fortawesome/free-solid-svg-icons'
    import {library} from '@fortawesome/fontawesome-svg-core'

    import AppNavBar from "@/components/AppNavBar";
    import GlobalContextMenu from "@/components/folders/GlobalContextMenu";

    library.add(faSearch)

    export default {
        name: "FolderLayout",
        components: {
            AppNavBar,
            GlobalContextMenu
        },
        data: function () {
            return {
                keyword: ''
            }
        },
        computed: {
            isNoFolders: function () {
                return this.$store.getters['folders/filteredFolders'].length === 0
            },
            isNoTemplates: function () {
                return this.$store.getters['folders/filteredTemplates'].length === 0
            },
            isNoContent: function () {
                return this.isNoFolders && this.isNoTemplates
            }
        },
        methods: {
            handleSearch: function () {
                console.log(this.keyword);
                this.$store.dispatch('folders/handleSearch', this.keyword);
            }
        }
    }
</script>

<style scoped>
    .layout {
        height: 100%;
    }

    .app-nav-bar {
        max-height: 65px;
    }

    .page-content {
        height: calc(100vh - 65px);
        position: relative;
        box-sizing: border-box;
    }

    .global-context-menu {
        height: 100%;
        width: 100%;
        position: fixed;
        top: 0;
        left: 0;
        z-index: 2;
    }

    .wrapper {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        box-sizing: border-box;
        padding: 100px 60px 60px;
    }

    .no-content {
        font-size: 14px;
        width: 250px;
        height: 300px;
        position: absolute;
        top: 0;
        bottom: 0;
        right: 0;
        left: 0;
        margin: auto;
    }

    .illistration {
        width: 237px;
        height: 290px;
        background: url('../../assets/images/no-download.png') center center no-repeat;
        margin-bottom: 40px;
    }


    .folder-group-title {
        font-size: 24px;
    }

    .template-group-title {
        font-size: 24px;
    }

    .search-box {
        z-index: 3;
    }
</style>