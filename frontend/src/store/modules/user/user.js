import getters from "@/store/modules/user/getters";
import mutations from "@/store/modules/user/mutations";
import actions from "@/store/modules/user/actions";
import state from "@/store/modules/user/state";

export default {
    namespaced: true,
    state, getters, mutations, actions
}