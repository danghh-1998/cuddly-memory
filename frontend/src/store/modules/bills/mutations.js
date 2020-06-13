export default {
    fetchBills: (state, payload) => {
        state.bills = payload.bills
    },
    checkout: (state, payload) => {
        state.payUrl = payload.payUrl
    }
}