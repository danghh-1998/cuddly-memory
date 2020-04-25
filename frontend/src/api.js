import axios from 'axios'
import camelcaseKeys from "camelcase-keys";

let api = axios.create({
    baseURL: process.env.VUE_APP_BASE_API_URL,
    transformResponse: [data => {
        if (data) {
            return (camelcaseKeys(JSON.parse(data), {deep: true}))
        }
    }]
});

export default api
