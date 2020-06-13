<template>
    <div class="pages">
        <app-nav-bar />
        <div class="page-content">
            <b-table
                hover
                :items="bills"
                :fields="fields"
                head-variant="light"
            >
                <template #cell(paymentAt)="data">
                    <span>{{ data.item.paymentAt ? data.item.paymentAt : "---" }}</span>
                </template>
                <template #cell(actions)="row">
                    <b-button
                        size="sm"
                        class="mr-1"
                        variant="primary"
                        :disabled="row.item.paymentAt"
                        @click="checkout(row.item.id)"
                    >
                        Checkout
                    </b-button>
                </template>
            </b-table>
        </div>
    </div>
</template>

<script>
    import AppNavBar from "@/components/AppNavBar";

    export default {
        name: "Bill",
        components: {AppNavBar},
        data: function () {
            return {
                bills: [],
                fields: [
                    {key: 'id', label: 'Id'},
                    {key: 'month', label: 'Month'},
                    {key: 'year', label: 'Year'},
                    {key: 'amount', label: 'Amount (VNĐ)'},
                    {key: 'paymentAt', label: 'Payment at'},
                    {key: 'actions', label: 'Actions'}
                ],
            }
        },
        created: function () {
            this.$store.dispatch('bills/fetchBills')
                .then(() => {
                    this.bills = this.$store.getters['bills/bills'];
                })
        },
        methods: {
            checkout: function (id) {
                this.$store.dispatch('bills/checkout', id)
                    .then(() => {
                        window.location = this.$store.getters['bills/payUrl']
                    })
            }
        }
    }
</script>

<style scoped>
    .pages {
        height: 100vh;
    }

    .page-content {
        padding-top: 4.75rem;
    }
</style>