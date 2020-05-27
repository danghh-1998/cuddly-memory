<template>
    <div class="cropped-wrapper">
        <div
            :class="{'cropped-area': true, 'focused': $props.focused}"
            @click="showBoundingBox"
            @mouseenter="overlayShow = true"
            @mouseleave="overlayShow = false"
        >
            <div class="cropped">
                <img
                    :src="$props.boundingBox.image"
                    alt="Crop image"
                >
            </div>
            <div class="overlay">
                <b-overlay
                    v-if="$store.getters['auth/role'] === 'admin'"
                    :id="overlayId"
                    :show="overlayShow"
                    variant="light"
                    :opacity="0.6"
                    blur="5px"
                    rounded="sm"
                    class="d-inline-block"
                >
                    <template #overlay>
                        <b-button
                            size="sm"
                            @click="deleteBoundingBox"
                        >
                            Delete
                        </b-button>
                    </template>
                </b-overlay>
            </div>
        </div>
        <b-form inline>
            <label
                class="mr-1 ml-3 cropped-title"
                :for="boundingBoxId"
            >
                Recognize type
            </label>
            <b-form-select
                :id="boundingBoxId"
                v-model="selected"
                :disabled="$store.getters['auth/role'] === 'user'"
                :options="options"
                class="mt-2 form-select"
                @change="updateType"
            />
        </b-form>
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
                selected: this.$props.boundingBox.type,
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
                        text: "English multiple line"
                    },
                    {
                        value: 3,
                        text: "Vietnam multiple line"
                    },
                    {
                        value: 4,
                        text: "Digit"
                    },
                    {
                        value: 5,
                        text: "Checkbox"
                    }
                ],
                overlayShow: false
            }
        },
        computed: {
            boundingBoxId: function () {
                return `inline-form-custom-select-pref-${this.$props.boundingBox.id}`
            },
            overlayId: function () {
                return `overlay-background-${this.$props.boundingBox.id}`
            }
        },
        methods: {
            showBoundingBox: function () {
                this.$emit('showBoundingBox', this.$props.boundingBox)
            },
            updateType: function () {
                this.$emit('updateType', this.boundingBox.id, this.selected)
            },
            deleteBoundingBox: function () {
                this.$emit('deleteBoundingBox', this.$props.boundingBox)
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
        border-radius: 10px;
        position: relative;
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
        width: calc(80% - 3.25rem);
        margin-left: 1rem;
    }

    .overlay {
        position: absolute;
        top: 5px;
        right: 40px;
    }

    .cropped-title {
        position: relative;
        top: 5px;
    }
</style>