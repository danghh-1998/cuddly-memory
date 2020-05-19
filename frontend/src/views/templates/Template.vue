<template>
    <div class="page">
        <app-nav-bar />
        <p class="page-title">
            Template
        </p>
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
                    <b-button-group
                        class="template-group-button"
                    >
                        <b-button-group
                            class="template-group-button-left"
                        >
                            <b-button
                                variant="primary"
                                class="mr-2 template-button"
                                @click="addBoundingBox"
                            >
                                Add
                            </b-button>
                            <b-button
                                v-if="boundingBoxes.length > 0"
                                variant="primary"
                                class="mr-2 template-button"
                                @click="updateBoundingBox"
                            >
                                Update
                            </b-button>
                        </b-button-group>
                        <b-button-group
                            class="template-group-button-right"
                        >
                            <b-button
                                v-if="boundingBoxes.length > 0"
                                variant="primary"
                                class="mr-2 w-25 template-button"
                            >
                                Create template
                            </b-button>
                        </b-button-group>
                    </b-button-group>
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
                            @showBoundingBox="showBoundingBox"
                            @updateType="updateType"
                        />
                    </vuescroll>
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
        name: "Template",
        components: {
            CroppedImg,
            VueCropper,
            AppNavBar,
            vuescroll
        },
        data: function () {
            return {
                imgSrc: 'http://127.0.0.1:8000/api/templates/14/image/1?token=06ca17b51b5f4a540cd80f08fa7f2b856a2479a5',
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
                focusedId: 0
            };
        },
        computed: {
            isNoContent: function () {
                return this.boundingBoxes.length === 0;
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
                    image: this.getImage(),
                    type: 0
                })
                this.$refs.cropper.reset()
                this.focusedId = this.boundingBoxes.length - 1
            },
            updateBoundingBox: function () {
                let boundingBox = this.boundingBoxes[this.boundingBoxes.length - this.focusedId - 1]
                boundingBox.data = this.getData()
                boundingBox.image = this.getImage()
            },
            showBoundingBox: function (data, boundingBoxId) {
                this.focusedId = boundingBoxId
                this.$refs.cropper.setData(JSON.parse(data))
            },
            updateType: function (imgId, type) {
                this.boundingBoxes[imgId].type = type
                console.log(this.boundingBoxes)
            }
        }
    }
</script>

<style scoped>
    .page {
        height: 100vh;
    }

    .page-title {
        display: inline-block;
        font-size: 1.5rem;
        margin-top: 5.25rem;
    }

    .page-container {
        height: calc(100% - 8.5rem);
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

    .tabs {
        height: calc(50% - 1rem);
    }

    .tabs-card {
        height: 100%;
    }

    .template-group-button {
        width: 99%;
        margin-bottom: 0.75rem;
    }

    .template-group-button-left {
        width: 50%;
    }

    .template-group-button-right {
        width: 50%;
        display: inline-flex;
        justify-content: flex-end;
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

</style>