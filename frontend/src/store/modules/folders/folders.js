import getters from "@/store/modules/folders/getters";
import mutations from "@/store/modules/folders/mutations";
import actions from "@/store/modules/folders/actions";
import state from "@/store/modules/folders/state";

export default {
    namespaced: true,
    state, getters, mutations, actions
}