import getters from "@/store/modules/bills/getters";
import mutations from "@/store/modules/bills/mutations";
import state from "@/store/modules/bills/state";
import actions from "@/store/modules/bills/actions";

export default {
    namespaced: true,
    state, getters, mutations, actions
}
