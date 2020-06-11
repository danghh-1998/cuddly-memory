import axios from 'axios'
import camelcaseKeys from "camelcase-keys";

export const api = axios.create({
    baseURL: process.env.VUE_APP_BASE_URL,
    transformResponse: [data => {
        if (data) {
            return (camelcaseKeys(JSON.parse(data), {deep: true}))
        }
    }]
});

export const imageApi = axios.create({
    baseURL: process.env.VUE_APP_BASE_URL,
    responseType: "blob"
});
