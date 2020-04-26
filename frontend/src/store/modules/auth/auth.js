import getters from "@/store/modules/auth/getters";
import mutations from "@/store/modules/auth/mutations";
import actions from "@/store/modules/auth/actions";
import state from "@/store/modules/auth/state";

export default {
    namespaced: true,
    state, getters, mutations, actions
}