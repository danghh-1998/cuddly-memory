<template>
    <div class="pages">
        <div
            class="d-flex pb-2 pt-2 pr-2 flex-butoon"
        >
            <b-button
                variant="primary"
                @click="$bvModal.show('create-user')"
            >
                Create new {{ $store.getters['auth/role'] === 'superadmin' ? "admin" : "user" }}
            </b-button>
        </div>
        <b-table
            hover
            :items="subUsers"
            :fields="fields"
            :tbody-tr-class="adminClass"
            outlined
            head-variant="light"
        >
            <template #cell(name)="data">
                <span>{{ data.item.name }}</span>
            </template>
            <template #cell(role)="data">
                <span>{{ convertRole(data.item.role) }}</span>
            </template>
            <template #cell(birthday)="data">
                <span>{{ convertDate(data.item.birthday) }}</span>
            </template>
            <template #cell(deleted)="data">
                <span>{{ data.item.deleted ? "No" : "Yes" }}</span>
            </template>
            <template #cell(createdAt)="data">
                <span>{{ convertDate(data.item.createdAt) }}</span>
            </template>
            <template #cell(actions)="row">
                <b-button
                    size="sm"
                    class="mr-1"
                    :variant="row.item.deleted ? 'primary': 'danger'"
                    @click="changeStatus(row.item)"
                >
                    {{ row.item.deleted ? 'Activate': 'Deactivate' }}
                </b-button>
            </template>
        </b-table>
        <b-modal
            id="create-user"
            hide-footer
            centered
        >
            <template
                #modal-title
            >
                Create new {{ $store.getters['auth/role'] === 'superadmin' ? 'admin' : 'user' }}
            </template>
            <div class="d-block">
                <b-form-group
                    label="Name"
                    label-for="form-name"
                >
                    <b-form-input
                        id="form-name"
                        v-model="$v.form.name.$model"
                        required
                        placeholder="Name"
                        :state="validateState('name')"
                    />
                </b-form-group>
                <b-form-group
                    label="Email"
                    label-for="form-email"
                >
                    <b-form-input
                        id="form-email"
                        v-model="$v.form.email.$model"
                        type="email"
                        required
                        placeholder="Email"
                        :state="validateState('email')"
                    />
                </b-form-group>
                <b-form-group
                    label="Telephone number"
                    label-for="form-tel"
                >
                    <b-form-input
                        id="form-tel"
                        v-model="$v.form.tel.$model"
                        required
                        placeholder="Telephone number"
                        :state="validateState('tel')"
                    />
                </b-form-group>
                <b-form-group
                    label="Date of birth"
                    label-for="form-birthday"
                >
                    <b-form-datepicker
                        id="form-birthday"
                        v-model="$v.form.birthday.$model"
                        required
                        :state="validateState('birthday')"
                    />
                </b-form-group>
            </div>
            <b-button
                class="mt-3 mr-3"
                variant="primary"
                :disabled="status === 'SUBMITTING'"
                @click="createUser"
            >
                OK
                <b-spinner
                    small
                    type="grow"
                    :class="{hidden: status !== 'SUBMITTING'}"
                />
            </b-button>
            <b-button
                class="mt-3"
                variant="light"
                @click="$bvModal.hide('create-user')"
            >
                Cancel
            </b-button>
        </b-modal>
    </div>
</template>

<script>
    import {email, maxLength, minLength, numeric, required} from "vuelidate/lib/validators";
    import snakecaseKeys from "snakecase-keys";
    import {validationMixin} from "vuelidate";

    export default {
        name: "UserManagement",
        mixins: {
            validationMixin
        },
        data: function () {
            return {
                subUsers: [],
                fields: [
                    {key: 'name', label: 'Name'},
                    {key: 'email', label: 'Email'},
                    {key: 'tel', label: 'Telephone number'},
                    {key: 'birthday', label: 'Birthday'},
                    {key: 'email', label: 'Email'},
                    {key: 'role', label: 'Role'},
                    {key: 'deleted', label: 'Active'},
                    {key: 'createdAt', label: 'Created at'},
                    {key: 'actions', label: 'Actions'}
                ],
                form: {
                    email: null,
                    name: null,
                    birthday: null,
                    tel: null
                }
            }
        },
        computed: {
            status: function () {
                return this.$store.getters['auth/submit']
            }
        },
        created: function () {
            this.$store.dispatch('auth/listSubUsers')
                .then(() => {
                    let subUsers = this.$store.getters['auth/subUsers']
                    if (this.$store.getters['auth/role'] === 'superadmin') {
                        subUsers.forEach(user => {
                            if (user.role === 1) {
                                this.subUsers.push(user)
                                this.subUsers = this.subUsers.concat(subUsers.filter(item => {
                                    return item.role === 0 && item.admin === user.id
                                }))
                            }
                        })
                    } else {
                        this.subUsers = this.subUsers.concat(subUsers)
                    }
                })
        },
        validations: {
            form: {
                name: {
                    required
                },
                email: {
                    required,
                    email
                },
                tel: {
                    required,
                    numeric,
                    minLength: minLength(10),
                    maxLength: maxLength(10)
                },
                birthday: {
                    required
                }
            }
        },
        methods: {
            convertRole: function (role) {
                switch (role) {
                    case 0:
                        return 'User'
                    case 1:
                        return 'Admin'
                    case 2:
                        return 'Super admin'
                    case 3:
                        return 'System admin'
                }
            },
            convertDate: function (date) {
                return new Date(date).toDateString()
            },
            changeStatus: function (item) {
                if (item.deleted === null) {
                    this.$store.dispatch('auth/deactivateUser', item.id)
                } else {
                    this.$store.dispatch('auth/activateUser', item.id)
                }
            },
            adminClass: function (item) {
                if (item.role === 1) {
                    return 'table-secondary'
                }
            },
            validateState: function (name) {
                const {$dirty, $error} = this.$v.form[name];
                return $dirty ? !$error : null;
            },
            makeToast: function () {
                this.$bvToast.toast('There were problems creating an account.', {
                    title: 'Create user failed',
                    autoHideDelay: 4000,
                    variant: 'danger'
                })
            },
            resetForm: function () {
                this.form = {
                    email: null,
                    name: null,
                    birthday: null,
                    tel: null
                }
            },
            createUser: function () {
                this.$v.form.$touch();
                if (this.$v.form.$anyError) {
                    this.makeToast();
                } else {
                    this.$store.dispatch('auth/createUser', snakecaseKeys(this.form))
                        .then(() => {
                            if (this.status === 'FAILED') {
                                this.makeToast();
                                this.resetForm();
                                this.$store.dispatch('auth/resetStatus');
                            } else {
                                this.$bvModal.hide('create-user')
                                let subUsers = this.$store.getters['auth/subUsers']
                                if (this.$store.getters['auth/role'] === 'superadmin') {
                                    subUsers.forEach(user => {
                                        if (user.role === 1) {
                                            this.subUsers.push(user)
                                            this.subUsers = this.subUsers.concat(subUsers.filter(item => {
                                                return item.role === 0 && item.admin === user.id
                                            }))
                                        }
                                    })
                                } else {
                                    this.subUsers = this.subUsers.concat(subUsers)
                                }
                            }
                        });
                }
            }
        }
    }
</script>

<style scoped>
    .flex-butoon {
        justify-content: flex-end;
    }

    .page {
        width: 99%;
    }

    .hidden {
        display: none;
    }
</style>