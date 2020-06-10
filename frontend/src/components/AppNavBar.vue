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
                        :href="$route.path === '/folders/0' ? '#': '/folders/0'"
                    >
                        <span class="nav-text">Template</span>
                    </b-nav-item>
                    <b-nav-item
                        v-if="$store.getters['auth/role'] === 'user'"
                        :active="routeName==='tasks'"
                        :href="$route.path === '/tasks' ? '#': '/tasks'"
                    >
                        <span class="nav-text">Task</span>
                    </b-nav-item>
                    <b-nav-item
                        v-if="$store.getters['auth/role'] === 'admin'"
                        :active="routeName==='user-management'"
                        :href="$route.path === '/user-management' ? '#': '/user-management'"
                    >
                        <span class="nav-text">User</span>
                    </b-nav-item>
                </b-navbar-nav>
                <b-navbar-nav>
                    <b-nav-item-dropdown right>
                        <template
                            #button-content
                        >
                            <font-awesome-icon
                                :icon="['fas', 'cog']"
                                class="folder-icon-svg"
                            />
                        </template>
                        <b-dropdown-item href="/profile">
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
    import {faCog} from '@fortawesome/free-solid-svg-icons'
    import {library} from '@fortawesome/fontawesome-svg-core'

    library.add(faCog)

    export default {
        name: "AppNavBar",
        computed: {
            routeName: function () {
                return this.$route.name;
            },
        },
        methods: {
            signOut: function () {
                this.$store.dispatch('auth/signOut')
                    .then(() => {
                        this.$router.push({name: 'sign-in'})
                    })
            }
        }
    }
</script>

<style scoped>
    .app-nav {
    }

    .nav-text {
        font-size: 18px;
    }
</style>
