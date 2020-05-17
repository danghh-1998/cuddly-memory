<template>
    <auth-layout>
        <template
            #form
            class="change-init"
        >
            <div class="signin-title">
                <h1>Change password</h1>
            </div>
            <div class="change-init-form">
                <b-form>
                    <b-form-group
                        label="Old password"
                        label-for="form-old-password"
                    >
                        <b-form-input
                            id="form-old-password"
                            v-model="$v.form.oldPassword.$model"
                            type="password"
                            :state="validateState('oldPassword')"
                            placeholder="Enter old password"
                        />
                    </b-form-group>
                    <b-form-group
                        label="Password"
                        label-for="form-password"
                    >
                        <b-form-input
                            id="form-password"
                            v-model="$v.form.password.$model"
                            type="password"
                            :state="validateState('password')"
                            placeholder="Enter your password"
                        />
                    </b-form-group>

                    <b-form-group
                        label="Confirm password"
                        label-for="form-confirm-password"
                    >
                        <b-form-input
                            id="form-confirm-password"
                            v-model="$v.form.passwordConfirmation.$model"
                            type="password"
                            :state="validateState('passwordConfirmation')"
                            placeholder="Confirm your password"
                        />
                    </b-form-group>

                    <div class="signin-form-button">
                        <b-button
                            variant="primary"
                            pill
                            block
                            :disabled="status === 'SUBMITTING'"
                            @click="changeInitPassword"
                        >
                            Change password
                            <b-spinner
                                small
                                type="grow"
                                :class="{hidden: status !== 'SUBMITTING'}"
                            />
                        </b-button>
                    </div>
                </b-form>
            </div>
        </template>
    </auth-layout>
</template>

<script>
    import AuthLayout from "@/components/auth/AuthLayout";
    import {validationMixin} from "vuelidate";
    import {required, minLength} from "vuelidate/lib/validators"
    import snakecaseKeys from 'snakecase-keys'

    export default {
        name: "ChangeInitPassword",
        components: {
            AuthLayout
        },
        mixins: [
            validationMixin
        ],
        data: function () {
            return {
                form: {
                    oldPassword: null,
                    password: null,
                    passwordConfirmation: null
                }
            }
        },
        validations: {
            form: {
                oldPassword: {
                    required,
                    minLength: minLength(6)
                },
                password: {
                    required,
                    minLength: minLength(6)
                },
                passwordConfirmation: {
                    required,
                    minLength: minLength(6)
                }
            }
        },
        computed: {
            status: function () {
                return this.$store.getters['auth/submit']
            }
        },
        mounted: function () {
            this.makeToast('You must change your password before logging on the first time.',
                'info', 'Change initial password')
        },
        methods: {
            validateState: function (name) {
                const {$dirty, $error} = this.$v.form[name];
                return $dirty ? !$error : null;
            },
            makeToast: function (message, variant, title) {
                this.$bvToast.toast(message, {
                    title: title,
                    autoHideDelay: 4000,
                    variant: variant
                })
            },
            resetForm: function () {
                this.form = {
                    oldPassword: null,
                    password: null,
                    passwordConfirmation: null
                }
            },
            changeInitPassword: function () {
                this.$store.dispatch('auth/changePassword', snakecaseKeys(this.form))
                .then(() => {
                    if (this.status === 'FAILED') {
                        this.makeToast('Incorrect password or password mismatch', 'danger',
                            'Change initial password failed');
                        this.resetForm();
                        this.$store.dispatch('auth/resetStatus');
                    } else {
                        this.$router.push('/')
                    }
                })
            }
        }
    }
</script>

<style scoped>
    .hidden {
        display: none;
    }
</style>