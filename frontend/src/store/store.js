import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from "vuex-persistedstate";

import auth from "@/store/modules/auth/auth";
import folders from "@/store/modules/folders/folders";
import templates from "@/store/modules/templates/templates";
import tasks from "@/store/modules/tasks/tasks";
import bills from "@/store/modules/bills/bills";

Vue.use(Vuex);

export const store = new Vuex.Store({
    modules: {
        auth,
        folders,
        templates,
        tasks,
        bills
    },
    plugins: [createPersistedState({
        key: 'vuex',
        reducer(val) {
            if (localStorage.getItem('token') === null) {
                return null
            }
            return val
        }
    })],
});
