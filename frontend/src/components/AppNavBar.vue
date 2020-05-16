<template>
    <div class="app-nav">
        <b-navbar
            toggleable="lg"
            type="dark"
            variant="dark"
            fixed="top"
        >
            <b-navbar-brand href="#">
                <img
                    src="../assets/logo.png"
                    alt="Logo"
                    style="width: 80%; height: 80%"
                    variant="faded"
                    type="light"
                >
            </b-navbar-brand>
            <b-navbar-toggle
                target="nav-collapse"
            />
            <b-collapse
                id="nav-collapse"
                is-nav
            >
                <b-navbar-nav class="m-auto">
                    <b-nav-item
                        :active="routeName==='folders'"
                        :href="routeName==='folders' ? '#' : '/folders/0'"
                    >
                        <span class="nav-text">Template</span>
                    </b-nav-item>
                    <b-nav-item
                        href="#"
                    >
                        <span class="nav-text">Task</span>
                    </b-nav-item>
                </b-navbar-nav>
                <b-navbar-nav>
                    <b-nav-item-dropdown right>
                        <template
                            #button-content
                        >
                            <span class="nav-text">User</span>
                        </template>
                        <b-dropdown-item href="#">
                            Profile
                        </b-dropdown-item>
                        <b-dropdown-item
                            href="#"
                            @click="signOut"
                        >
                            Sign Out
                        </b-dropdown-item>
                    </b-nav-item-dropdown>
                </b-navbar-nav>
            </b-collapse>
        </b-navbar>
    </div>
</template>

<script>
    export default {
        name: "AppNavBar",
        computed: {
            routeName: function () {
                return this.$route.name;
            }
        },
        methods: {
            signOut: function () {
                this.$store.dispatch('auth/signOut');
                this.$router.push({name: 'sign-in'})
            }
        }
    }
</script>

<style scoped>
    .app-nav {
        font-family: 'Montserrat', sans-serif;
    }

    .nav-text {
        font-size: 18px;
    }
</style>