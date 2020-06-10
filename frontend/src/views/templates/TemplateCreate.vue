<template>
    <div class="page">
        <app-nav-bar />
        <div class="page-header ml-2 pb-1">
            <div class="page-header-wrapper">
                <span class="d-inline-block">Template {{ $store.getters['templates/name'] }}</span>
                <b-button
                    variant="primary"
                    class="d-inline-block mr-2 template-button"
                    :disabled="!canCreate"
                    @click="createTemplate"
                >
                    Create template
                </b-button>
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
                        :auto-crop="true"
                        :auto-crop-size="0"
                        class="cropper"
                        :responsive="true"
                        :restore="false"
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
                    class="col-scroll col"
                >
                    <vuescroll :ops="ops">
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
                            @show-bounding-box="showBoundingBox"
                            @update-type="updateType"
                            @update-context="updateContext"
                            @delete-bounding-box="deleteBoundingBox"
                        />
                    </vuescroll>
                    <b-button-group
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
    import dataUrlToBlob from "@/utils/dataUrlToBlob";

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
                boundingBoxes: [],
                ops: {
                    vuescroll: {},
                    scrollPanel: {},
                    rail: {},
                    bar: {
                        background: '#888888',
                        keepShow: false,
                    }
                },
                focusedId: 0,
                emptyImage: 'data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=='
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
                if (!(this.boundingBoxes.length === 0 || this.focusedId === null)) {
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
            updateContext: function (imgId, context) {
                let index = this.boundingBoxes.findIndex(boundingBox => {
                    return boundingBox.id === imgId
                })
                this.boundingBoxes[index].context = context
            },
            deleteBoundingBox: function (boundingBox) {
                this.boundingBoxes.splice(this.boundingBoxes.length - boundingBox.id - 1, 1)
                this.$refs.cropper.reset()
            },
            createTemplate: function () {
                let convertedBoundingBoxes = []
                let blobImage = dataUrlToBlob.dataURItoBlob(this.$store.getters['templates/image'])
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
                        },
                    ]
                    convertedBoundingBoxes.push(
                        {
                            metadata: convertedData,
                            recognize_type: boundingBox.type,
                            context: boundingBox.context
                        }
                    )
                })
                this.$store.dispatch('templates/createTemplate', {
                    image: blobImage,
                    name: this.$store.getters['templates/name'],
                    folder_id: this.$store.getters['folders/id'],
                    bounding_boxes: convertedBoundingBoxes
                })
                    .then(() => {
                        this.$router.push(`/folders/${this.$store.getters['folders/id']}`)
                    })
            },
            cropend: function () {
                this.updateBoundingBox()
            },
            zoom: function () {
                this.updateBoundingBox()
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