<template>
    <div
        id="app"
        @contextmenu="handleContextMenu($event)"
    >
        <vuescroll :ops="ops">
            <router-view :key="$route.fullPath" />
        </vuescroll>
    </div>
</template>

<script>
    import 'bootstrap/dist/css/bootstrap.css'
    import 'bootstrap-vue/dist/bootstrap-vue.css'
    import vuescroll from 'vuescroll';

    export default {
        name: 'App',
        components: {vuescroll},
        data: function () {
            return {
                ops: {
                    vuescroll: {},
                    scrollPanel: {},
                    rail: {},
                    bar: {
                        background: '#888888',
                        keepShow: true,
                    }
                }
            }
        },
        methods: {
            handleContextMenu: function (e) {
                e.preventDefault()
            }
        }
    };
</script>

<style lang="scss">
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100;0,200;0,300;0,400;0,500;1,100;1,200;1,300;1,400;1,500&display=swap');

    #app {
        font-family: 'Montserrat', sans-serif;
        height: 100vh;
        user-select: none;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        color: #2c3e50;
    }
</style>
