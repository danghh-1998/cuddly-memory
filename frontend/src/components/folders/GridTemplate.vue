<template>
    <div
        v-click-outside="handleFocusOutside"
        class="template"
        @click="handleFocus"
        @dblclick="handleDoubleClick"
    >
        <div class="template-content">
            <div
                class="template-thumbnail"
                :style="thumbnailBackgroundImage"
            />
            <div :class="{'template-footer-wrapper': true, 'template-focus': templateFocus}">
                <div
                    :id="tooltipTemplateId"
                    class="template-footer"
                >
                    <font-awesome-icon
                        :icon="['fas', 'file-alt']"
                        class="template-icon"
                    />
                    <span :class="{'template-name': true, 'template-name-focus': templateFocus}">
                        {{ template.displayName }}
                    </span>
                </div>
                <b-tooltip
                    :target="tooltipTemplateId"
                    triggers="hover"
                >
                    {{ template.displayName }}
                </b-tooltip>
            </div>
        </div>
        <b-modal
            :id="renameTemplateId"
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
                :disabled="newName.trim() === '' || $store.getters['folders/templateNames'].includes(newName.trim())"
                @click="renameTemplate"
            >
                OK
            </b-button>
            <b-button
                class="mt-3"
                variant="light"
                @click="$bvModal.hide(renameTemplateId)"
            >
                Cancel
            </b-button>
        </b-modal>
        <b-modal
            :id="duplicateTemplateId"
            hide-footer
            centered
        >
            <template
                #modal-title
            >
                Duplicate template
            </template>
            <div class="d-block text-center">
                <b-form-input
                    v-model="duplicateTemplateName"
                    placeholder="Folder name"
                />
            </div>
            <b-button
                class="mt-3 mr-3"
                variant="primary"
                :disabled="duplicateTemplateName.trim() === '' || $store.getters['folders/templateNames'].includes(duplicateTemplateName.trim())"
                @click="duplicateTemplate"
            >
                OK
            </b-button>
            <b-button
                class="mt-3"
                variant="light"
                @click="$bvModal.hide(duplicateTemplateId)"
            >
                Cancel
            </b-button>
        </b-modal>
    </div>
</template>

<script>
    import ClickOutside from 'vue-click-outside'
    import {library} from '@fortawesome/fontawesome-svg-core'
    import {faFileAlt} from '@fortawesome/free-solid-svg-icons'

    library.add(faFileAlt)

    export default {
        name: "GridTemplate",
        directives: {
            ClickOutside
        },
        props: {
            template: {
                type: Object,
                required: true
            }
        },
        data: function () {
            return {
                templateFocus: false,
                newName: this.$props.template.displayName,
                duplicateTemplateName: `${this.$props.template.displayName}(Copy)`
            }
        },
        computed: {
            renameTemplateId: function () {
                return `modal-rename-template-${this.$props.template.id}`
            },
            duplicateTemplateId: function () {
                return `modal-duplicate-template-${this.$props.template.id}`
            },
            tooltipTemplateId: function () {
                return `tooltip-template-${this.$props.template.id}`
            },
            token: function () {
                return localStorage.getItem("token");
            },
            thumbnailBackgroundImage: function () {
                return {
                    'background-image': `url(http://127.0.0.1:8000/api/templates/${this.$props.template.id}/image/0?token=${this.token})`,
                    'width': '100%',
                    'height': '190px',
                    'background-position': 'center center',
                    'background-repeat': 'no-repeat',
                    'background-size': 'cover'
                }
            }
        },
        methods: {
            handleFocusOutside: function () {
                this.templateFocus = false
            },
            handleFocus: function () {
                this.templateFocus = true
            },
            showRenameModal: function () {
                this.$bvModal.show(this.renameTemplateId)
            },
            renameTemplate: function () {
                this.$store.dispatch('folders/renameTemplate', {
                    'id': this.template.id,
                    'name': this.newName
                })
                this.$bvModal.hide(this.renameTemplateId)
            },
            showDuplicateModal: function () {
                this.$bvModal.show(this.duplicateTemplateId)
            },
            handleDoubleClick: function () {
                this.$store.dispatch('templates/fetchTemplate', this.template.id)
                    .then(() => {
                        this.$router.push({name: 'templates', params: {templateId: this.template.id}})
                    })
            },
            duplicateTemplate: function () {
                this.$store.dispatch('folders/duplicateTemplate', {
                    templateId: this.$props.template.id,
                    name: this.duplicateTemplateName
                })
                this.$bvModal.hide(this.duplicateTemplateId)
            }
        }
    }
</script>

<style scoped>
    .template {
        height: 240px;
        width: 100%;
        border: 1px solid #CCCCCC;
        border-radius: 5px;
        margin-bottom: 20px;
        min-width: 100px;
        position: relative;
        z-index: 3;
    }

    .template-footer-wrapper {
        display: flex;
        flex-direction: column;
        justify-content: center;
        height: 50px;
    }

    .template-footer {
    }

    .template-icon {
        font-size: 20px;
        color: #565656;
        display: inline-block;
        margin-left: 20px;
    }

    .template-name {
        width: 60%;
        display: inline-block;
        padding-left: 20px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        position: relative;
        top: 5px;
    }

    .template-focus {
        -moz-border-radius-bottomleft: 6px;
        -moz-border-radius-bottomright: 6px;
        border-bottom-left-radius: 6px;
        border-bottom-right-radius: 6px;
        background-color: #E8F0FE;
        border-bottom: 1px solid #CCCCCC;
    }

    .template-name-focus {
        color: #1A73E8;
    }
</style>