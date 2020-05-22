import getters from "@/store/modules/templates/getters";
import mutations from "@/store/modules/templates/mutations";
import actions from "@/store/modules/templates/actions";
import state from "@/store/modules/templates/state";

export default {
    namespaced: true,
    state, getters, mutations, actions
}