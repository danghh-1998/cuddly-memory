<template>
    <div>
        <p class="preview-title">
            Preview
        </p>
        <div class="preview-wrapper">
            <section class="preview-area">
                <div class="preview" />
            </section>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Preview",
        props: {
            cropper: {
                required: true,
                type: Object,
            }
        },
        data: function () {
            return {
                data: null,
                cropImg: null
            }
        },
        methods: {}
    }
</script>

<style scoped>
    .preview-wrapper {
        width: 100%;
        height: 400px;
        background-color: #888888;
    }

    .preview-area {
        width: 100%;
        margin: 0 auto;
        text-align: center;
    }

    .preview {
        width: 100%;
        height: 400px;
        overflow: hidden;
        display: inline-block;
        max-width: 900px;
    }

    .button-add {
        margin-top: 20px;
        width: 98%;
    }

    .preview-title {
        margin-top: 1rem;
    }

    .preview > img {
        width: 20px;
        height: auto;
    }
</style>