import Vue from 'vue'
import VueRouter from "vue-router"
import VueResource from "vue-resource"
import App from './App.vue'
import routes from './router'
import VueQRCodeComponent from 'vue-qrcode-component'
import socketio from 'socket.io-client'
import VueSocketIO from 'vue-socket.io'
import VueCookies from 'vue-cookies'

// assets import
import '@fortawesome/fontawesome-free/css/all.css'
import '@fortawesome/fontawesome-free/js/all.js'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap-grid.css'
import 'bootstrap/dist/css/bootstrap-reboot.css'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap'
import 'bootstrap/dist/js/bootstrap.bundle'

// Vue.config.productionTip = false

export const socketInstance = socketio('https://terminus-back.herokuapp.com')

// plugin setup
Vue.use(VueRouter);
Vue.use(VueResource);
Vue.use(BootstrapVue);
Vue.use(new VueSocketIO({debug:true,connection: socketInstance}))
Vue.use(VueCookies)
Vue.component('qr-code', VueQRCodeComponent);

// set default config
VueCookies.config('1d')

// set global cookie
VueCookies.set('theme','default');
VueCookies.set('hover-time','1s');

const router = new VueRouter({
  mode: 'history',
  //base: process.env.BASE_URL,
  routes,
  linkActiveClass: 'active'
});

router.beforeEach(async (to, from, next) => {
    await Vue.nextTick();
  // This goes through the matched routes from last to first, finding the closest route with a title.
  // eg. if we have /some/deep/nested/route and /some, /deep, and /nested have titles, nested's will be chosen.
  const nearestWithTitle = to.matched.slice().reverse().find((r) => r.meta && r.meta.title);
  if (nearestWithTitle) {
    document.title = nearestWithTitle.meta.title;
  }

  if (to.matched.some((record) => record.meta.requiresAuth)) {
      // this route requires auth, check if logged in
      if(VueCookies.get('user') !== null) {
          next();
      } else {
          next("/terminus");
          app.disconnected = 'expired';
      }
  }

  if (to.matched.some((record) => record.meta.checkAuth)) {
      // check if logged in, if yes, redirect to home page
      if(VueCookies.get('user') !== null) {
          let cookieParts = JSON.parse(VueCookies.get('user'));
          app.id = cookieParts[0];
          app.username = cookieParts[1];
          app.pseudo = cookieParts[2];
          app.disconnected = "";
      } else {
          next();
      }
  }

  next();
});

export const app = new Vue({
    router,
    data: {
      username: "Inconnu",
      pseudo: "inconnu",
      avatar: "https://oasys.ch/wp-content/uploads/2019/03/photo-avatar-profil.png",
      id: null,
      disconnected: ""
    },
    render: h => h(App),
}).$mount('#app')
