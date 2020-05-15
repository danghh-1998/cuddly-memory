<template>
    <auth-layout>
        <vue-headful title="Reset password" />
        <template
            #form
            class="reset-password"
        >
            <div class="reset-password-title">
                <h1>Reset password</h1>
            </div>
            <div class="change-init-form">
                <b-form>
                    <b-form-group
                        label="Reset password token"
                        label-for="form-reset-password-token"
                    >
                        <b-form-input
                            id="form-reset-password-token"
                            v-model="$v.form.resetPasswordToken.$model"
                            :state="validateState('resetPasswordToken')"
                            placeholder="Reset password token"
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
                            @click="resetPassword"
                        >
                            Reset password
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
        name: "ResetPassword",
        components: {
            AuthLayout
        },
        mixins: [
            validationMixin
        ],
        data: function () {
            return {
                form: {
                    resetPasswordToken: null,
                    password: null,
                    passwordConfirmation: null
                }
            }
        },
        validations: {
            form: {
                resetPasswordToken: {
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
            this.makeToast('Reset password token sent to your email', 'info', 'Reset password')
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
            resetPassword: function () {
                this.$store.dispatch('auth/resetPassword', snakecaseKeys(this.form))
                .then(() => {
                    if (this.status === 'FAILED') {
                        this.makeToast('Incorrect token or password mismatch', 'danger',
                            'Reset password failed');
                        this.resetForm();
                        this.$store.dispatch('auth/resetStatus');
                    } else {
                        this.$router.push('/sign-in')
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