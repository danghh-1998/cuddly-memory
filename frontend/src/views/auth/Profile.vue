<template>
    <div class="page">
        <app-nav-bar />
        <b-container class="page-wrapper">
            <b-row class="wrapper">
                <b-col>
                    <b-tabs
                        content-class="mt-5"
                        align="center"
                    >
                        <b-tab
                            title="Profile"
                            active
                        >
                            <b-form-group
                                label="Name"
                                label-for="form-name"
                            >
                                <b-form-input
                                    id="form-name"
                                    v-model="$v.profileForm.name.$model"
                                    required
                                    placeholder="Enter your name"
                                    :state="validateState('name', 0)"
                                />
                            </b-form-group>
                            <b-form-group
                                label="Telephone number"
                                label-for="form-tel"
                            >
                                <b-form-input
                                    id="form-tel"
                                    v-model="$v.profileForm.tel.$model"
                                    required
                                    placeholder="Enter your telephone number"
                                    :state="validateState('tel', 0)"
                                />
                            </b-form-group>
                            <b-form-group
                                label="Date of birth"
                                label-for="form-birthday"
                            >
                                <b-form-datepicker
                                    id="form-birthday"
                                    v-model="$v.profileForm.birthday.$model"
                                    required
                                    :state="validateState('birthday', 0)"
                                />
                            </b-form-group>
                            <b-button
                                variant="primary"
                                pill
                                :disabled="status === 'SUBMITTING'"
                                @click="updateProfile"
                            >
                                Update profile
                                <b-spinner
                                    small
                                    type="grow"
                                    :class="{hidden: status !== 'SUBMITTING'}"
                                />
                            </b-button>
                        </b-tab>
                        <b-tab title="Account">
                            <b-form-group
                                label="Old password"
                                label-for="form-old-password"
                            >
                                <b-form-input
                                    id="form-old-password"
                                    v-model="$v.accountForm.oldPassword.$model"
                                    required
                                    type="password"
                                    placeholder="Enter your password"
                                    :state="validateState('oldPassword', 1)"
                                />
                            </b-form-group>
                            <b-form-group
                                label="Password"
                                label-for="form-password"
                            >
                                <b-form-input
                                    id="form-password"
                                    v-model="$v.accountForm.password.$model"
                                    required
                                    type="password"
                                    placeholder="Enter your password"
                                    :state="validateState('password', 1)"
                                />
                            </b-form-group>
                            <b-form-group
                                label="Date of birth"
                                label-for="form-passowrd-conformation"
                            >
                                <b-form-input
                                    id="form-passowrd-conformation"
                                    v-model="$v.accountForm.passwordConfirmation.$model"
                                    required
                                    type="password"
                                    placeholder="Confirm password"
                                    :state="validateState('passwordConfirmation', 1)"
                                />
                            </b-form-group>
                            <b-button
                                variant="primary"
                                pill
                                :disabled="status === 'SUBMITTING'"
                                @click="changePassword"
                            >
                                Change password
                                <b-spinner
                                    small
                                    type="grow"
                                    :class="{hidden: status !== 'SUBMITTING'}"
                                />
                            </b-button>
                        </b-tab>
                    </b-tabs>
                </b-col>
            </b-row>
        </b-container>
    </div>
</template>

<script>
    import AppNavBar from "@/components/AppNavBar";
    import {maxLength, minLength, numeric, required} from "vuelidate/lib/validators";
    import {validationMixin} from "vuelidate";
    import snakecaseKeys from 'snakecase-keys'

    export default {
        name: "Profile",
        components: {AppNavBar},
        mixins: {
            validationMixin
        },
        data: function () {
            return {
                profileForm: {
                    name: null,
                    tel: null,
                    birthday: null
                },
                accountForm: {
                    oldPassword: null,
                    password: null,
                    passwordConfirmation: null
                }
            }
        },
        validations: {
            profileForm: {
                name: {
                    required
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
            },
            accountForm: {
                oldPassword: {
                    required,
                    minLength: minLength(6)
                },
                password: {
                    required,
                    minLength: minLength(6),
                },
                passwordConfirmation: {
                    required,
                    minLength: minLength(6),
                }
            }
        },
        computed: {
            status: function () {
                return this.$store.getters['auth/submit']
            }
        },
        methods: {
            validateState: function (name, type) {
                if (type === 0) {
                    const {$dirty, $error} = this.$v.profileForm[name];
                    return $dirty ? !$error : null;
                } else {
                    const {$dirty, $error} = this.$v.accountForm[name];
                    return $dirty ? !$error : null;
                }
            },
            makeToast: function (type, title, message) {
                this.$bvToast.toast(message, {
                    title: title,
                    autoHideDelay: 4000,
                    variant: type
                })
            },
            resetForm: function () {
                this.profileForm = {
                    name: null,
                    tel: null,
                    birthday: null
                }
                this.accountForm = {
                    oldPassword: null,
                    password: null,
                    passwordConfirmation: null
                }
            },
            updateProfile: function () {
                this.$v.profileForm.$touch();
                if (this.$v.profileForm.$anyError) {
                    this.makeToast('danger', 'Update profile failed', 'There were problems updateing your profile.');
                } else {
                    this.$store.dispatch('auth/updateProfile', snakecaseKeys(this.profileForm))
                        .then(() => {
                            this.makeToast('info', 'Update profile success', 'Update profile success');
                            this.$store.dispatch('auth/resetStatus');
                            setTimeout(() => {
                                this.$router.push('/folders/0')
                            }, 1000)
                        })
                }
            },
            changePassword: function () {
                this.$store.dispatch('auth/changePassword', snakecaseKeys(this.accountForm))
                    .then(() => {
                        if (this.status === 'FAILED') {
                            this.makeToast('danger',
                                'Change password failed', 'Incorrect password or password mismatch');
                            this.resetForm();
                            this.$store.dispatch('auth/resetStatus');
                        } else {
                            setTimeout(() => {
                                this.$router.push('/folders/0')
                            }, 1000)
                        }
                    })
            }
        }
    }
</script>

<style scoped>
    .page-wrapper {
        margin-top: 100px;
        width: 100vw;
        height: 100vh;
    }

    .content-tabs {
        width: 100%;
        border: none;
    }

    .hidden {
        display: none;
    }
</style>