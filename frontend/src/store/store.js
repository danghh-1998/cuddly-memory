import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from "vuex-persistedstate";

import auth from "@/store/modules/auth/auth";
import folders from "@/store/modules/folders/folders";
import templates from "@/store/modules/templates/templates";

Vue.use(Vuex);

export const store = new Vuex.Store({
    modules: {
        auth,
        folders,
        templates
    },
    plugins: [createPersistedState()],
});
