import Vue from 'vue'
import App from "@/App";
import Router from "vue-router";

import {store} from "@/store/store";
import router from "@/router";

Vue.config.productionTip = false;
const originalPush = Router.prototype.push;
Router.prototype.push = function push(location, onResolve, onReject) {
    if (onResolve || onReject) return originalPush.call(this, location, onResolve, onReject);
    return originalPush.call(this, location).catch(err => err)
};

Vue.use(Router);

new Vue({
    render: h => h(App),
    router,
    store: store
}).$mount('#app');
