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
        <div class="form-table-wrapper">
            <div class="form-table">
                <div class="form-table-row">
                    <p class="form-table-cell form-table-cell-left">
                        Result
                    </p>
                    <div
                        class="form-table-cell form-table-cell-right"
                    >
                        <b-form-input
                            :value="boundingBox.result.result"
                        />
                    </div>
                </div>
                <div class="form-table-row">
                    <p class="form-table-cell form-table-cell-left">
                        Confirm result
                    </p>
                    <div
                        class="form-table-cell form-table-cell-right"
                    >
                        <b-form-input
                            v-model="newResult"
                            placeholder="Confirm result (Optional)"
                        />
                    </div>
                </div>
            </div>
            <b-button
                variant="primary"
                :disabled="newResult.trim() === ''"
                @click="confirmResult"
            >
                Confirm
            </b-button>
        </div>
    </div>
</template>

<script>
    export default {
        name: "TaskConfirmItem",
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
                newResult: ''
            }
        },
        computed: {
            boundingBoxId: function () {
                return `inline-form-custom-select-pref-${this.$props.boundingBox.id}`
            },
        },
        methods: {
            showBoundingBox: function () {
                this.$emit('show-bounding-box', this.$props.boundingBox)
            },
            confirmResult: function () {
                this.$store.dispatch('tasks/confirmResult', {
                    payload: {
                        image_id: this.$route.params.imageId,
                        result_id: this.boundingBox.result.id,
                        confirm_result: this.newResult
                    },
                    id: this.$store.getters['tasks/id']
                })
                    .then(() => {
                        this.newResult = ''
                    })
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
        height: 220px;
        margin: 0 auto;
        background-color: #BBBBBB;
        border-radius: 10px;
        position: relative;
    }

    .cropped {
        height: 220px;
        overflow: hidden;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .cropped > img {
        max-width: 100%;
        max-height: 220px;
        object-fit: contain;
    }

    .focused {
        background-color: #777777;
    }

    .form-select {
        width: calc(80% - 3.25rem);
        margin-left: 1rem;
    }

    .form-table-wrapper {
        width: calc(99% - 1rem);
        padding-top: 1rem;
        padding-left: 1rem;
    }

    .form-table {
        display: table;
        table-layout: fixed;
        width: 100%;
    }

    .form-table-row {
        display: table-row;
    }

    .form-table-cell {
        display: table-cell;
        text-align: left;
        height: 2.5rem;
    }

    .form-table-cell-left {
        width: 8rem;
    }

    .form-table-cell-right {
        width: calc(100% - 8rem);
    }

</style>
