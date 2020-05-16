import Vue from 'vue'
import App from "@/App";
import Router from "vue-router";
import {BootstrapVue, IconsPlugin} from 'bootstrap-vue'
import responsive from 'vue-responsive';
import Vuelidate from 'vuelidate'
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'
import contentmenu from 'v-contextmenu'
import 'v-contextmenu/dist/index.css'

import {store} from "@/store/store";
import router from "@/router";

Vue.config.productionTip = false;
const originalPush = Router.prototype.push;
Router.prototype.push = function push(location, onResolve, onReject) {
    if (onResolve || onReject) return originalPush.call(this, location, onResolve, onReject);
    return originalPush.call(this, location).catch(err => err)
};

Vue.component('FontAwesomeIcon', FontAwesomeIcon)

Vue.use(Router);
Vue.use(BootstrapVue);
Vue.use(IconsPlugin);
Vue.use(responsive);
Vue.use(Vuelidate);
Vue.use(contentmenu);


new Vue({
    render: h => h(App),
    router,
    store: store
}).$mount('#app');
