<template>
    <auth-layout>
        <vue-headful title="Sign up" />
        <template
            #form
            class="signup"
        >
            <div class="signup-title">
                <h1>Sign up</h1>
            </div>
            <div class="signup-form">
                <b-form>
                    <div
                        v-if="tab==='prev'"
                        class="signup-form-tab"
                    >
                        <p class="signup-form-tab-helper">
                            Company Information
                        </p>
                        <b-form-group
                            label="Business name"
                            label-for="form-client-name"
                        >
                            <b-form-input
                                id="form-client-name"
                                v-model="$v.form.clientName.$model"
                                required
                                placeholder="Business name"
                                :state="validateState('clientName')"
                            />
                        </b-form-group>
                        <b-form-group
                            label="Business email"
                            label-for="form-email"
                        >
                            <b-form-input
                                id="form-email"
                                v-model="$v.form.email.$model"
                                type="email"
                                required
                                placeholder="Business email"
                                :state="validateState('email')"
                            />
                        </b-form-group>
                        <b-form-group
                            label="Address"
                            label-for="form-address"
                        >
                            <b-form-input
                                id="form-address"
                                v-model="$v.form.address.$model"
                                required
                                placeholder="Address"
                                :state="validateState('address')"
                            />
                        </b-form-group>
                        <b-button
                            block
                            variant="primary"
                            pill
                            @click="nextTab"
                        >
                            Continue
                        </b-button>
                    </div>
                    <div
                        v-else
                        class="signup-form-tab"
                    >
                        <p class="signup-form-tab-helper">
                            Your information
                        </p>
                        <b-form-group
                            label="Name"
                            label-for="form-name"
                        >
                            <b-form-input
                                id="form-name"
                                v-model="$v.form.name.$model"
                                required
                                placeholder="Enter your name"
                                :state="validateState('name')"
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
                                placeholder="Enter your telephone number"
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
                        <div class="signup-form-group-button">
                            <b-button
                                variant="primary"
                                pill
                                @click="prevTab"
                            >
                                Previous
                            </b-button>
                            <b-button
                                variant="primary"
                                pill
                                :disabled="status === 'SUBMITTING'"
                                @click="signUp"
                            >
                                Sign up
                                <b-spinner
                                    small
                                    type="grow"
                                    :class="{hidden: status !== 'SUBMITTING'}"
                                />
                            </b-button>
                        </div>
                    </div>
                </b-form>
            </div>
        </template>
        <template
            #navigate
            class="signup-navigate"
        >
            <span class="signup-navigate-text">Have an account?</span>
            <router-link
                to="/sign-in"
                class="signup-navigate-link"
            >
                Sign in
            </router-link>
        </template>
    </auth-layout>
</template>

<script>
    import AuthLayout from "@/components/auth/AuthLayout";
    import {validationMixin} from "vuelidate";
    import {required, email, minLength, numeric, maxLength} from "vuelidate/lib/validators"
    import snakecaseKeys from 'snakecase-keys'

    export default {
        name: "Signup",
        components: {
            AuthLayout
        },
        mixins: {
            validationMixin
        },
        data: function () {
            return {
                tab: 'prev',
                form: {
                    name: null,
                    email: null,
                    tel: null,
                    clientName: null,
                    address: null,
                    birthday: null
                }
            }
        },
        computed: {
            status: function () {
                return this.$store.getters['auth/submit']
            }
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
                clientName: {
                    required
                },
                address: {
                    required
                },
                birthday: {
                    required
                }
            }
        },
        methods: {
            nextTab: function () {
                this.tab = 'next';
            },
            prevTab: function () {
                this.tab = 'prev'
            },
            validateState: function (name) {
                const {$dirty, $error} = this.$v.form[name];
                return $dirty ? !$error : null;
            },
            makeToast: function () {
                this.$bvToast.toast('There were problems creating your account.', {
                    title: 'Sign up failed',
                    autoHideDelay: 4000,
                    variant: 'danger'
                })
            },
            signUp: function () {
                this.$v.form.$touch();
                if (this.$v.form.$anyError) {
                    this.makeToast();
                } else {
                    this.$store.dispatch('auth/signUp', snakecaseKeys(this.form))
                    .then(() => {
                        if (this.status === 'FAILED') {
                            this.makeToast();
                            this.resetForm();
                            this.$store.dispatch('auth/resetStatus');
                        } else {
                            this.$router.push('/sign-in');
                        }
                    });
                }
            }
        }
    }
</script>

<style lang="scss" scoped>
    .signup-form {
        &-tab {
            &-helper {
                font-size: 14px;
                font-weight: lighter;
            }
        }
        &-group-button {
            display: flex;
            justify-content: space-around;
            button {
                width: 180px;
            }
        }
    }
    .signup-navigate {
        &-text {
            color: #888888;
        }
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