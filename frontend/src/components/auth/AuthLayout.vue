<template>
    <div class="pages">
        <div
            v-if="windowWidth > 850"
            class="auth-pages"
        >
            <b-container
                class="auth-pages-wrap"
                :fluid="true"
            >
                <b-row class="wrapper">
                    <b-col
                        v-if="windowWidth > 1300"
                        class="auth-image-wrapper"
                    >
                        <tilt class="auth-image">
                            <img
                                data-tilt
                                src="../../assets/images/auth-image.png"
                                alt="auth image"
                            >
                        </tilt>
                    </b-col>
                    <b-col>
                        <div class="auth-card-wrap">
                            <slot name="form" />
                        </div>
                        <div class="auth-navigate">
                            <slot name="navigate" />
                        </div>
                    </b-col>
                </b-row>
            </b-container>
        </div>
        <div
            v-else
            class="sm-form"
        >
            <div class="sm-auth-card-wrap">
                <slot name="form" />
            </div>
            <div class="sm-auth-navigate">
                <slot name="navigate" />
            </div>
        </div>
    </div>
</template>

<script>
    import Tilt from "@/components/auth/Tilt";

    export default {
        name: "AuthLayout",
        components: {Tilt},
        data: function () {
            return {
                windowWidth: window.innerWidth
            }
        },
        mounted() {
            window.onresize = () => {
                this.windowWidth = window.innerWidth
            }
        }
    }
</script>

<style scoped>
    .pages {
        width: 100%;
    }
    .auth-pages {
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        background: linear-gradient(-135deg, #c850c0, #4158d0);
    }

    .wrapper {
        height: 100%;
    }

    .auth-pages-wrap {
        position: relative;
        height: 90vh;
        width: 60%;
        background: white;
        padding: 70px;
        border-radius: 10px;
        overflow: hidden;
    }

    .auth-image-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
    }

    .auth-image {
        width: 300px;
        height: auto;
    }

    .auth-card-wrap {
        display: flex;
        flex-direction: column;
        justify-content: center;
        height: 100%;
        min-width: 200px;
    }

    .auth-navigate {
        text-align: center;
    }

    .sm-form {
        display: flex;
        justify-content: center;
        flex-direction: column;
        padding: 50px;
        height: 100vh;
    }

    .sm-auth-navigate {
        text-align: center;
        margin-top: 50px;
    }

</style>