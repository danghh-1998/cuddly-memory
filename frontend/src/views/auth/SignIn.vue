<template>
    <auth-layout>
        <template
            #form
            class="signin"
        >
            <div class="signin-title">
                <h1>Sign in</h1>
            </div>
            <div class="signin-form">
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

                    <div class="signin-form-button">
                        <b-button
                            variant="primary"
                            pill
                            block
                            :disabled="status === 'SUBMITTING'"
                            @click="signIn"
                        >
                            Sign in
                            <b-spinner
                                small
                                type="grow"
                                :class="{hidden: status !== 'SUBMITTING'}"
                            />
                        </b-button>
                    </div>

                    <div class="signin-form-forgot">
                        <span>Forgot</span>
                        <router-link
                            to="/req-reset-password"
                            class="signin-form-forgot-link"
                        >
                            Account / Password?
                        </router-link>
                    </div>
                </b-form>
            </div>
        </template>
        <template
            #navigate
        >
            <router-link
                to="/sign-up"
                class="signin-navigate"
            >
                Create your account
            </router-link>
        </template>
    </auth-layout>
</template>

<script>
    import AuthLayout from "@/components/auth/AuthLayout";
    import {validationMixin} from "vuelidate";
    import {required, email, minLength} from "vuelidate/lib/validators"
    import snakecaseKeys from 'snakecase-keys'

    export default {
        name: "SignIn",
        components: {
            AuthLayout
        },
        mixins: [validationMixin],
        data: function () {
            return {
                form: {
                    email: null,
                    password: null
                }
            }
        },
        validations: {
            form: {
                email: {
                    required,
                    email
                },
                password: {
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
        methods: {
            validateState: function (name) {
                const {$dirty, $error} = this.$v.form[name];
                return $dirty ? !$error : null;
            },
            makeToast: function () {
                this.$bvToast.toast('Incorrect email or password', {
                    title: 'Login failed',
                    autoHideDelay: 4000,
                    variant: 'danger'
                })
            },
            resetForm: function () {
                this.form = {
                    email: this.form.email,
                    password: null
                }
            },
            signIn: function () {
                this.$v.form.$touch();
                if (this.$v.form.$anyError) {
                    this.makeToast();
                } else {
                    this.$store.dispatch('auth/signIn', snakecaseKeys(this.form))
                        .then(() => {
                            if (this.status === 'FAILED') {
                                this.makeToast();
                                this.resetForm();
                                this.$store.dispatch('auth/resetStatus');
                            } else {
                                let user = this.$store.getters['auth/user'];
                                if (!user.changeInitPassword) {
                                    this.$router.push('/change-init-password')
                                } else {
                                    this.$router.push('/folders/0');
                                }
                            }
                        })
                }
            }
        }
    }
</script>

<style
    lang="scss"
    scoped
>
    .signin-navigate {
        color: #888888;
        text-decoration: none;
    }

    .signin-navigate:hover {
        color: #5cb85c;
    }

    .signin-form-forgot {
        margin-top: 10px;
        font-size: 14px;
        color: #888888;

        &-link {
            color: #777777;
            text-decoration: none;
        }

        &-link:hover {
            color: #5cb85c;
        }
    }

    .hidden {
        display: none;
    }
</style>