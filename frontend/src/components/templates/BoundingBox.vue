<template>
    <div class="wrapper">
        <div class="area">
            <div
                v-if="boundingType==='PREVIEW'"
                class="preview"
            />
            <div
                v-else
                class="crop-img"
            >
                <img
                    :src="cropImg"
                    alt="Cropped image"
                >
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "BoundingBox",
        props: {
            cropper: {
                type: Object,
                required: true
            },
            boundingType: {
                type: String,
                required: true
            }
        },
        data: function () {
            return {
                data: null,
                cropImg: null
            }
        },
        methods: {
            cropImage() {
                this.cropImg = this.$props.cropper.getCroppedCanvas().toDataURL();
            },
            getData() {
                this.data = JSON.stringify(this.$props.cropper.getData(), null, 4);
            },
        }
    }
</script>

<style scoped>
    .wrapper {
        width: 98%;
        height: 200px;
        background-color: #888888;
        border: 1px solid #1A73E8;
        border-radius: 10px;
        margin-bottom: 20px;
    }

    .area {
        width: 100%;
        margin: 0 auto;
        text-align: center;
    }

    .preview {
        width: 100%;
        height: 200px;
        overflow: hidden;
        display: inline-block;
    }

    .crop-img {
        width: 100%;
        height: 200px;
        overflow: hidden;
        display: inline-block;
    }
</style>