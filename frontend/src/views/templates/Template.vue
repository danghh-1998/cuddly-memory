<template>
    <div class="page">
        <app-nav-bar />
        <div class="page-header ml-2 pb-1">
            <div class="page-header-wrapper">
                <span class="d-inline-block">Template {{ $store.getters['templates/name'] }}</span>
                <b-button
                    v-if="$store.getters['auth/role'] === 'admin'"
                    variant="primary"
                    class="d-inline-block mr-2 template-button"
                    :disabled="canEdite"
                    @click="updateTemplate"
                >
                    Save
                </b-button>
                <b-button
                    v-if="!canEdit"
                    variant="primary"
                    class="d-inline-block mr-2 template-button"
                    :disabled="!canCreate"
                    @click="$bvModal.show('create-task')"
                >
                    Create task
                </b-button>
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
            </div>
        </div>
        <b-container
            :fluid="true"
            class="page-container"
        >
            <b-row>
                <b-col
                    lg="6"
                    md="6"
                    sm="12"
                    xs="12"
                    cols="12"
                    class="col mb-2 mb-md-0"
                >
                    <vue-cropper
                        ref="cropper"
                        :aspect-ratio="NaN"
                        :src="imgSrc"
                        preview=".preview"
                        :view-mode="1"
                        :guides="false"
                        :center="false"
                        :min-container-height="600"
                        :auto-crop-size="0"
                        class="cropper"
                        :responsive="true"
                        :restore="false"
                        @ready="ready"
                        @cropend="cropend"
                        @zoom="zoom"
                    />
                </b-col>
                <b-col
                    lg="6"
                    md="6"
                    sm="12"
                    xs="12"
                    cols="12"
                    :class="{'col-scroll': true, 'col': true, 'col-scroll-view': !canEdit}"
                >
                    <vuescroll
                        :key="forceUpdate"
                        :ops="ops"
                    >
                        <div
                            v-if="isNoContent"
                            class="no-content"
                        >
                            <div class="illistration">
                                <img
                                    src="../../assets/images/no-download.png"
                                    class="no-content-background"
                                    alt="background"
                                >
                            </div>
                            <p>No bounding box selected</p>
                        </div>
                        <cropped-img
                            v-for="boundingBox in boundingBoxes"
                            :key="boundingBox.id"
                            :bounding-box="boundingBox"
                            :focused="boundingBox.id === focusedId"
                            @showBoundingBox="showBoundingBox"
                            @updateType="updateType"
                            @deleteBoundingBox="deleteBoundingBox"
                        />
                    </vuescroll>
                    <b-button-group
                        v-if="canEdit"
                        class="template-group-button"
                    >
                        <b-button
                            variant="primary"
                            size="sm"
                            :disabled="!canAdd"
                            :class="{'mr-2': true, 'd-inline-block': true, 'template-button': true}"
                            @click="addBoundingBox"
                        >
                            Add
                        </b-button>
                    </b-button-group>
                </b-col>
            </b-row>
        </b-container>
    </div>
</template>

<script>
    import VueCropper from 'vue-cropperjs';
    import 'cropperjs/dist/cropper.css';
    import AppNavBar from "@/components/AppNavBar";
    import CroppedImg from "@/components/templates/CroppedImg";
    import vuescroll from 'vuescroll';


    export default {
        name: "TemplateCreate",
        components: {
            CroppedImg,
            VueCropper,
            AppNavBar,
            vuescroll
        },
        data: function () {
            return {
                imgSrc: this.$store.getters['templates/image'],
                boundingBoxes: this.$store.getters['templates/boundingBoxes'],
                ops: {
                    vuescroll: {},
                    scrollPanel: {},
                    rail: {},
                    bar: {
                        background: '#888888',
                        keepShow: false,
                    }
                },
                focusedId: null,
                forceUpdate: 0,
                emptyImage: 'data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==',
                taskFile: null
            };
        },
        computed: {
            isNoContent: function () {
                return this.boundingBoxes.length === 0;
            },
            canCreate: function () {
                if (this.boundingBoxes.length === 0) {
                    return false
                }
                let check = true
                this.boundingBoxes.forEach(boundingBox => {
                    if (boundingBox.image === this.emptyImage) {
                        check = false
                    }
                })
                return check
            },
            canAdd: function () {
                if (this.boundingBoxes.length === 0) {
                    return true
                }
                return this.boundingBoxes[0].image !== this.emptyImage;
            },
            canEdit: function () {
                return this.$store.getters['auth/role'] === 'admin'
            }
        },
        methods: {
            getData: function () {
                return JSON.stringify(this.$refs.cropper.getData(), null, 4)
            },
            getImage: function () {
                return this.$refs.cropper.getCroppedCanvas().toDataURL()
            },
            addBoundingBox: function () {
                this.boundingBoxes.unshift({
                    id: this.boundingBoxes.length,
                    data: this.getData(),
                    image: this.emptyImage,
                    type: 0
                })
                this.$refs.cropper.reset()
                this.focusedId = null
            },
            updateBoundingBox: function () {
                if (this.boundingBoxes.length !== 0) {
                    let boundingBox = this.boundingBoxes[this.boundingBoxes.length - this.focusedId - 1]
                    boundingBox.data = this.getData()
                    boundingBox.image = this.getImage()
                }
            },
            showBoundingBox: function (boundingBox) {
                this.focusedId = boundingBox.id
                if (boundingBox.image === this.emptyImage) {
                    boundingBox.image = this.getImage()
                }
                this.$refs.cropper.setData(JSON.parse(boundingBox.data))
            },
            updateType: function (imgId, type) {
                let index = this.boundingBoxes.findIndex(boundingBox => {
                    return boundingBox.id === imgId
                })
                this.boundingBoxes[index].type = type
            },
            deleteBoundingBox: function (boundingBox) {
                this.boundingBoxes.splice(this.boundingBoxes.length - boundingBox.id - 1, 1)
                this.$refs.cropper.reset()
            },
            updateTemplate: function () {
                let convertedBoundingBoxes = []
                this.boundingBoxes.forEach(boundingBox => {
                    let data = JSON.parse(boundingBox.data)
                    let convertedData = [
                        {
                            x: data.x,
                            y: data.y
                        },
                        {
                            x: data.x + data.width,
                            y: data.y + data.height
                        }
                    ]
                    convertedBoundingBoxes.unshift(
                        {
                            "metadata": convertedData,
                            recognize_type: boundingBox.type
                        }
                    )
                })
                this.$store.dispatch('templates/updateTemplate', {
                    bounding_boxes: convertedBoundingBoxes,
                    templateId: this.$store.getters['templates/id']
                })
                    .then(() => {
                        this.$router.push(`/folders/${this.$store.getters['folders/id']}`)
                    })
            },
            ready: function () {
                this.boundingBoxes.forEach((boundingBox, index) => {
                    this.$refs.cropper.setData(JSON.parse(boundingBox.data))
                    boundingBox.image = this.$refs.cropper.getCroppedCanvas().toDataURL()
                    this.$set(this.boundingBoxes, index, boundingBox)
                })
                this.forceUpdate += 1
                this.$refs.cropper.reset()
            },
            cropend: function () {
                if (this.canEdit) {
                    this.updateBoundingBox()
                }
            },
            zoom: function () {
                if (this.canEdit) {
                    this.updateBoundingBox()
                }
            },
            createTask: function () {
                this.$store.dispatch('tasks/createTask', {
                    template_id: this.$store.getters['templates/id'],
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
    .page {
        height: 100vh;
    }

    .page-header {
        display: inline-block;
        font-size: 1.5rem;
        margin-top: 4.75rem;
        position: relative;
        width: 99%;
    }

    .page-container {
        height: calc(100% - 7.5rem);
    }

    .row {
        height: 100%;
    }

    .col {
        height: 100%;
        padding-left: 0
    }

    .cropper {
        height: 100%;
    }

    .col-scroll {
        padding-right: 0 !important;
        height: calc(100% - 3.25rem);
    }

    .col-scroll-view {
        height: 100%;
        margin-bottom: 0;
    }

    .template-group-button {
        width: 99%;
        margin-top: 0.75rem;
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
        text-align: center;
    }

    .no-content-background {
        visibility: hidden;
        width: 150px;
        height: auto;
    }

    .illistration {
        background-image: url('../../assets/images/no-download.png');
        background-position: center;
        background-repeat: no-repeat;
        background-size: contain;
        margin-bottom: 40px;
    }

    .page-header-wrapper {
        display: flex;
        justify-content: space-between;
    }

</style>
