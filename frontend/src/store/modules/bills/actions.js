import {api} from "@/api";

export default {
    fetchBills: context => {
        api.defaults.headers.common.Authorization = `Token ${localStorage.getItem('token')}`;
        return api.get('bills')
            .then(response => {
                context.commit('fetchBills', response.data)
            })
    },
    checkout: (context, payload) => {
        api.defaults.headers.common.Authorization = `Token ${localStorage.getItem('token')}`;
        return api.post(`bills/${payload}/make_payment`)
            .then(response => {
                console.log(response.data)
                context.commit('checkout', response.data)
            })
    }
}