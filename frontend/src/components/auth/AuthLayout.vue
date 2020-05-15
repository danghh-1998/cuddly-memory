<template>
    <div class="auth-pages">
        <div class="auth-pages-wrap">
            <div class="auth-pages-wrap-flex">
                <div
                    v-responsive.lg.xl
                    class="auth-image"
                >
                    <tilt class="auth-image-grid">
                        <img
                            data-tilt
                            src="../../assets/images/auth-image.png"
                            alt="auth image"
                        >
                    </tilt>
                </div>
                <div class="auth-card-wrap">
                    <div class="auth-card">
                        <slot name="form" />
                    </div>
                    <div class="auth-navigate">
                        <slot name="navigate" />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import Tilt from "@/components/auth/Tilt";
    export default {
        name: "AuthLayout",
        components: {Tilt}
    }
</script>

<style lang="scss" scoped>
    .auth-pages {
        font-family: 'Montserrat', sans-serif;
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        background: linear-gradient(-135deg, #c850c0, #4158d0);

        &-wrap {
            position: relative;
            height: 90vh;
            width: 960px;
            background: white;
            padding: 70px;
            border-radius: 10px;
            min-height: 683px;
            overflow: hidden;

            &-flex {
                height: 100%;
                width: 100%;
                display: flex;
                justify-content: space-between;
                align-items: center;
                .auth-image {
                    &-grid {
                        width: 300px;
                        height: auto;
                    }
                }
                .auth-card-wrap {
                    width: 400px;
                    display: flex;
                    flex-direction: column;
                    justify-content: space-around;
                    height: 500px;

                    .auth-card {
                    }
                    .auth-navigate {
                        display: block;
                        text-align: center;
                        bottom: 20px;
                        right: 200px;
                        position: absolute;
                    }
                }
            }
        }
    }
</style>