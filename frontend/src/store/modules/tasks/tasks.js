import state from "@/store/modules/tasks/state";
import getters from "@/store/modules/tasks/getters";
import mutations from "@/store/modules/tasks/mutations";
import actions from "@/store/modules/tasks/actions";

export default {
    namespaced: true,
    state, getters, mutations, actions
}
