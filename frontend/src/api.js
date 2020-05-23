import axios from 'axios'
import camelcaseKeys from "camelcase-keys";

export const api = axios.create({
    baseURL: 'http://localhost:8000/api',
    transformResponse: [data => {
        if (data) {
            return (camelcaseKeys(JSON.parse(data), {deep: true}))
        }
    }]
});

export const imageApi = axios.create({
    baseURL: 'http://localhost:8000/api',
    responseType: "blob"
});
