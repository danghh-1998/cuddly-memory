<template>
    <auth-layout>
        <template
            #form
            class="req-reset-pwd"
        >
            <div class="signin-title">
                <h1>Reset password</h1>
            </div>
            <div class="req-reset-pwd-form">
                <b-form>
                    <b-form-group
                        label="Email"
                        label-for="form-email"
                    >
                        <b-form-input
                            id="form-email"
                            v-model="$v.form.email.$model"
                            type="email"
                            :state="validateState('email')"
                            placeholder="Enter your email"
                        />
                    </b-form-group>
                    <div class="signin-form-button">
                        <b-button
                            variant="primary"
                            pill
                            block
                            :disabled="status === 'SUBMITTING'"
                            @click="requestResetPassword"
                        >
                            Send token
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
        <template
            #navigate
        >
            <span class="navigate-text">Have an account?</span>
            <router-link
                to="/sign-in"
                class="navigate-link"
            >
                Sign in
            </router-link>
        </template>
    </auth-layout>
</template>

<script>
    import AuthLayout from "@/components/auth/AuthLayout";
    import {validationMixin} from "vuelidate";
    import {required, email} from "vuelidate/lib/validators"
    import snakecaseKeys from 'snakecase-keys'

    export default {
        name: "RequestResetPassword",
        components: {
            AuthLayout
        },
        mixins: [validationMixin,],
        data: function () {
            return {
                form: {
                    email: null
                }
            }
        },
        validations: {
            form: {
                email: {
                    required,
                    email
                }
            }
        },
        computed: {
            status: function () {
                return this.$store.getters['auth/submit']
            }
        },
        methods: {
            validateState: function (name) {
                const {$dirty, $error} = this.$v.form[name];
                return $dirty ? !$error : null;
            },
            requestResetPassword: function () {
                this.$store.dispatch('auth/requestResetPassword', snakecaseKeys(this.form))
                    .then(() => {
                        this.$router.push('/reset-password')
                    })
            }
        }
    }
</script>

<style scoped>
    .navigate-text {
        color: #888888;
    }

    .navigate-link {
        color: #777777;
        text-decoration: none;
    }

    .navigate-link:hover {
        color: #5cb85c;
    }

    .hidden {
        display: none;
    }
</style>