<template>
    <b-container
        :fluid="true"
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
                    :view-mode="1"
                    :guides="false"
                    :center="false"
                    :min-container-height="600"
                    :auto-crop-size="0"
                    class="cropper"
                    :responsive="true"
                    :restore="false"
                    @ready="ready"
                />
            </b-col>
            <b-col
                lg="6"
                md="6"
                sm="12"
                xs="12"
                cols="12"
                :class="{'col-scroll': true, 'col': true}"
            >
                <vuescroll
                    :key="forceUpdate"
                    :ops="ops"
                >
                    <task-confirm-item
                        v-for="boundingBox in boundingBoxes"
                        :key="boundingBox.id"
                        :bounding-box="boundingBox"
                        :focused="boundingBox.id === focusedId"
                        @show-bounding-box="showBoundingBox"
                    />
                </vuescroll>
                <b-button-group
                    class="template-group-button"
                >
                    <b-button
                        variant="primary"
                        size="sm"
                        :class="{'mr-2': true, 'd-inline-block': true, 'template-button': true}"
                        @click="downloadResult"
                    >
                        Download result
                    </b-button>
                </b-button-group>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
    import VueCropper from 'vue-cropperjs';
    import 'cropperjs/dist/cropper.css';
    import vuescroll from 'vuescroll';
    import TaskConfirmItem from "@/components/tasks/TaskConfirmItem";


    export default {
        name: "TaskConfirmImage",
        components: {
            TaskConfirmItem,
            VueCropper,
            vuescroll,
        },
        props: {
            imgSrc: {
                type: String,
                required: true
            },
            results: {
                type: Array,
                required: true
            }
        },
        data: function () {
            return {
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
                focusedId: null,
                forceUpdate: 0,
                emptyImage: 'data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==',
            };
        },
        methods: {
            getData: function () {
                return JSON.stringify(this.$refs.cropper.getData(), null, 4)
            },
            getImage: function () {
                return this.$refs.cropper.getCroppedCanvas().toDataURL()
            },
            showBoundingBox: function (boundingBox) {
                this.$refs.cropper.enable()
                this.focusedId = boundingBox.id
                if (boundingBox.image === this.emptyImage) {
                    boundingBox.image = this.getImage()
                }
                this.$refs.cropper.setData(JSON.parse(boundingBox.data))
                this.$refs.cropper.disable()
            },
            ready: function () {
                this.$store.getters['templates/boundingBoxes'].reverse().forEach((boundingBox, index) => {
                    this.$refs.cropper.setData(JSON.parse(boundingBox.data))
                    this.boundingBoxes.push({
                        id: boundingBox.id,
                        image: this.$refs.cropper.getCroppedCanvas().toDataURL(),
                        result: this.results[index],
                        data: boundingBox.data
                    })
                })
                this.forceUpdate += 1
                this.$refs.cropper.reset()
            },
            downloadResult: function () {
                let images = this.$store.getters['tasks/images']
                let boundingBoxes = this.$store.getters['templates/boundingBoxes']
                let results = []
                images.forEach(image => {
                    let data = []
                    image.results.forEach((result, index) => {
                        data.push({
                            context: boundingBoxes[index].context,
                            result: result.result
                        })
                    })
                    results.push({
                        image: image.name,
                        result: data
                    })
                })
                const url = window.URL.createObjectURL(new Blob([JSON.stringify(results)], {type: "application/json"}))
                const link = document.createElement('a')
                link.href = url
                link.setAttribute('download', 'result.json')
                document.body.appendChild(link)
                link.click()
            }
        }
    }
</script>

<style scoped>
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
