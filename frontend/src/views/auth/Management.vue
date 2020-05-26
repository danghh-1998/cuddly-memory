<template>
    <div class="page">
        <app-nav-bar />
        <user-management />
    </div>
</template>

<script>
    import AppNavBar from "@/components/AppNavBar";
    import UserManagement from "@/components/auth/UserManagement";

    export default {
        name: "Management",
        components: {AppNavBar, UserManagement}
    }
</script>

<style scoped>
    .page {
        padding-top: 4.75rem;
    }
</style>