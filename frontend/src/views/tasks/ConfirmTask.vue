<template>
    <div class="page">
        <app-nav-bar />
        <div class="page-header ml-2 pb-1">
            <div class="page-header-wrapper">
                <b-button
                    variant="primary"
                    class="d-inline-block mr-2 template-button"
                    :disabled="startImage"
                    @click="previousImage"
                >
                    Previous
                </b-button>
                <b-button
                    variant="primary"
                    class="d-inline-block mr-2 template-button"
                    :disabled="endImage"
                    @click="nextImage"
                >
                    Next
                </b-button>
            </div>
        </div>
        <task-confirm-image
            class="page-container"
            :img-src="imgSrc"
            :results="currentImage.results"
        />
    </div>
</template>

<script>
    import 'cropperjs/dist/cropper.css';
    import AppNavBar from "@/components/AppNavBar";
    import TaskConfirmImage from "@/components/tasks/TaskConfirmImage";


    export default {
        name: "ConfirmTask",
        components: {
            AppNavBar,
            TaskConfirmImage
        },
        data: function () {
            return {
                images: this.$store.getters['tasks/images']
            }
        },
        computed: {
            currentImageId: function () {
                return parseInt(this.$route.params.imageId)
            },
            currentImage: function () {
                return this.images.find(image => {
                    return image.id === this.currentImageId
                })
            },
            imgSrc: function () {
                let token = localStorage.getItem('token')
                return `http://localhost:8000/api/tasks/9/images/${this.currentImage.image}?token=${token}`
            },
            endImage: function () {
                return this.images.findIndex(image => {
                    return image.id === this.currentImageId
                }) === this.images.length - 1
            },
            startImage: function () {
                return this.images.findIndex(image => {
                    return image.id === this.currentImageId
                }) === 0
            }
        },
        methods: {
            nextImage: function () {
                let index = this.images.findIndex(image => {
                    return image.id === this.currentImageId
                })
                let nextImage = this.images[index + 1]
                this.$router.push({name: 'confirm-task', params: {imageId: nextImage.id}})
            },
            previousImage: function () {
                let index = this.images.findIndex(image => {
                    return image.id === this.currentImageId
                })
                let prevImage = this.images[index - 1]
                this.$router.push({name: 'confirm-task', params: {imageId: prevImage.id}})
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

    .page-header-wrapper {
        display: flex;
        justify-content: space-between;
    }

</style>
