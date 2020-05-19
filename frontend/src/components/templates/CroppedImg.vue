<template>
    <div class="cropped-wrapper">
        <div
            :class="{'cropped-area': true, 'focused': $props.focused}"
            @click="showBoundingBox"
        >
            <div class="cropped">
                <img
                    :src="$props.boundingBox.image"
                    alt="Crop image"
                >
            </div>
        </div>
        <b-form-select
            v-model="selected"
            :options="options"
            class="mt-2 form-select"
            @change="updateType"
        />
    </div>
</template>

<script>
    export default {
        name: "CroppedImg",
        props: {
            boundingBox: {
                type: Object,
                required: true
            },
            focused: {
                type: Boolean,
                required: true
            }
        },
        data: function () {
            return {
                selected: 0,
                options: [
                    {
                        value: 0,
                        text: "English"
                    },
                    {
                        value: 1,
                        text: "Tiếng Việt"
                    },
                    {
                        value: 2,
                        text: "Checkbox"
                    }
                ]
            }
        },
        methods: {
            showBoundingBox: function () {
                this.$emit('showBoundingBox', this.boundingBox.data, this.boundingBox.id)
            },
            updateType: function () {
                this.$emit('updateType', this.boundingBox.id, this.selected)
            }
        }
    }
</script>

<style scoped>
    .cropped-wrapper {
        width: 98%;
        height: 380px;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 1px solid #1A73E8;
    }

    .cropped-area {
        width: 100%;
        height: 320px;
        margin: 0 auto;
        background-color: #BBBBBB;
    }

    .cropped {
        height: 320px;
        overflow: hidden;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .cropped > img {
        max-width: 100%;
        max-height: 320px;
        object-fit: contain;
    }

    .focused {
        background-color: #777777;
    }

    .form-select {
        width: 96%;
        margin-left: 1rem;
    }
</style>