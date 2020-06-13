<template>
    <div class="page">
        <app-nav-bar />
        <div class="table-content">
            <b-table
                hover
                head-variant="light"
                :items="tasks"
                :fields="fields"
            >
                <template #cell(createdAt)="data">
                    <span>{{ convertDate(data.item.createdAt) }}</span>
                </template>
                <template #cell(status)="data">
                    <span>{{ convertStatus(data.item.status) }}</span>
                </template>
                <template #cell(template)="data">
                    <router-link :to="{name: 'templates', params: {templateId: data.item.template.id}}">
                        {{ data.item.template.displayName }}
                    </router-link>
                </template>
                <template #cell(actions)="data">
                    <b-button
                        v-if="data.item.status === 0"
                        variant="danger"
                        size="sm"
                        class="mr-1 task-button"
                        @click="cancelTask(data.item.id)"
                    >
                        Cancel
                    </b-button>
                    <b-button
                        v-if="data.item.status === 1"
                        variant="danger"
                        size="sm"
                        class="mr-1 task-button"
                        @click="stopTask(data.item.id)"
                    >
                        Stop
                    </b-button>
                    <b-button
                        v-if="data.item.status === 2"
                        variant="success"
                        size="sm"
                        class="mr-1 task-button"
                        @click="viewResult(data.item)"
                    >
                        View result
                    </b-button>
                    <b-button
                        v-if="data.item.status === 3"
                        variant="primary"
                        size="sm"
                        class="mr-1 task-button"
                        @click="startTask(data.item.id)"
                    >
                        Start
                    </b-button>
                </template>
            </b-table>
        </div>
    </div>
</template>

<script>
    import AppNavBar from "@/components/AppNavBar";

    export default {
        name: "Task",
        components: {AppNavBar},
        data: function () {
            return {
                tasks: [],
                fields: [
                    {key: 'id', label: "Task ID"},
                    {key: 'status', label: "Status"},
                    {key: 'template', label: "Template"},
                    {key: 'createdAt', label: "Created at"},
                    {key: 'actions', label: 'Actions'}
                ],
                timer: null
            }
        },
        created: function () {
            this.fetchTasks()
            this.timer = setInterval(this.fetchTasks, 1000)
        },
        beforeDestroy() {
            clearInterval(this.timer)
        },
        methods: {
            fetchTasks: function () {
                this.$store.dispatch('tasks/fetchTasks')
                    .then(() => {
                        this.tasks = this.$store.getters['tasks/tasks']
                    })
            },
            convertDate: function (date) {
                return new Date(date).toDateString()
            },
            convertStatus: function (status) {
                switch (status) {
                    case 0:
                        return 'Queued'
                    case 1:
                        return 'Processing'
                    case 2:
                        return 'Done'
                    case 3:
                        return 'Failed'
                }
            },
            cancelTask: function (payload) {
                this.$store.dispatch('tasks/cancelTask', payload)
                    .then(() => {
                        this.tasks = this.$store.getters['tasks/tasks']
                    })
            },
            stopTask: function (payload) {
                this.$store.dispatch('tasks/updateTask', {
                    id: payload,
                    status: '0'
                })
            },
            startTask: function (payload) {
                this.$store.dispatch('tasks/updateTask', {
                    id: payload,
                    status: '0'
                })
            },
            viewResult: function (payload) {
                this.$store.dispatch('tasks/fetchTask', payload)
                .then(() => {
                    this.$store.dispatch('templates/fetchTemplate', payload.template.id)
                        .then(() => {
                            this.$store.dispatch('tasks/fetchImages', payload.id)
                                .then(() => {
                                    let firstImage = this.$store.getters['tasks/images'][0].id
                                    this.$router.push({name: 'confirm-task', params: {imageId: firstImage}})
                                })
                        })
                })
            }
        }
    }
</script>

<style scoped>
    .page {
        height: 100%;
        padding-top: 4.75rem;
    }

    .table-content {
        padding-right: 4rem;
        padding-left: 4rem;
    }

    .task-button {
        min-width: 100px;
    }
</style>
