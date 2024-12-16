import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import vuetify from './plugins/vuetify'


import Flicking from "@egjs/vue3-flicking/dist/flicking.esm";
import "@egjs/vue3-flicking/dist/flicking.css";

const app = createApp(App)
const pinia = createPinia()

pinia.use(piniaPluginPersistedstate)

// app.use(createPinia())
app.use(pinia)
app.use(router)
app.use(vuetify)
// app.use(createPinia())

app.component("Flicking", Flicking);

app.mount('#app')
